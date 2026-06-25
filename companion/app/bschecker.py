import config
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic


# --- Structured output: we want exactly one clean question, no preamble. ---
class _Question(BaseModel):
    question: str = Field(description="Exactly one probing question, plain English.")


# The calibration-critical instruction. This encodes the methodology's
# vocabulary/probe calibration directly into the prompt: operator middle-band,
# architecture-level -- never dev trivia.
_GEN_INSTRUCTION = """You generate ONE probing question to test whether a person \
genuinely understands a decision they made and a claim they are standing behind.

Context you must respect: this person uses a personal, single-user build-to-learn \
companion. They personally made the decision below while building their own software, \
and "the claim" is something THEY claim to understand or have learned from it. "Claim" \
and "review" are internal terms of this learning tool -- NOT insurance/compliance/ \
business terms -- and there are NO other users or reviewers. Your question must ask \
THEM to defend THEIR OWN reasoning about THEIR decision -- why they made it, what it \
trades off, what they learned -- never to solve a hypothetical scenario in another domain.

Audience (critical): the person is an operator/leader -- AI Workflow Lead, AI PM, \
or COO-type -- NOT a software developer. Probe at the level a CTO would probe in a \
meeting: reasoning, tradeoffs, consequences.
- Ask things like: Why this choice over the alternative? What does this tradeoff \
reveal? What breaks first if X? How would you deploy/apply this? What would you \
change at 10x scale?
- Never ask them to name a function or method, recite syntax, explain what a line \
of code does, or recall exact API/library details.

Always probe the reasoning behind the decision they ACTUALLY made -- never invent a \
new, adjacent design problem they did not address.

Ask exactly ONE question, specific to THIS claim and decision (not generic). Plain English."""


# Difficulty ladder -- mirrors the judge's rigor ladder so question difficulty rises
# with the tier (gentle recall at spot -> cold interview at long).
_TIER_GUIDANCE = {
    "spot":   "TIER = spot (gentlest): ask them to explain THEIR OWN core reasoning for "
              "this decision in their own words -- 'why did you choose this?'",
    "short":  "TIER = short: ask them to articulate their core reasoning cleanly and "
              "completely -- still about the decision they actually made.",
    "medium": "TIER = medium (harder): probe the KEY SUPPORTING DETAILS and tradeoffs -- "
              "why this over the alternative, what it trades off, what it assumes.",
    "long":   "TIER = long (hardest): frame as a cold interview question -- what breaks "
              "at scale, what would you change, defend the decision under pressure.",
}

_gen_llm = ChatAnthropic(model=config.MODEL, max_tokens=512, max_retries=5).with_structured_output(_Question)


def generate_question(claim_text, decision_summary, kind, tier):
    """Produce one calibrated probing question, with difficulty scaled to the tier."""
    guidance = _TIER_GUIDANCE.get(tier, _TIER_GUIDANCE["spot"])
    prompt = (
        f"{_GEN_INSTRUCTION}\n\n{guidance}\n\n"
        f"Decision: {decision_summary}\n"
        f"The claim to probe ({kind}): {claim_text}"
    )
    return _gen_llm.invoke(prompt).question


# --- The judge (uncalibrated v1) ----------------------------------------------
class _Judgment(BaseModel):
    score: int = Field(description="1-5: how well the answer meets the rigor required at its tier.")
    verdict: str = Field(description="Exactly one of: solid, partial, wrong.")
    rationale: str = Field(description="Plain-English reason for the score: what was strong or missing.")
    ambiguous_question: bool = Field(description="True if the QUESTION was vague; if so, don't penalize the user for it.")
    complete_answer: str = Field(description="What a complete answer includes -- especially key supporting details the user did not mention. For learning, shown after scoring.")


_JUDGE_INSTRUCTION = """You are an UNCALIBRATED judge evaluating whether a person \
genuinely understands a decision THEY made. Judge their ANSWER to the QUESTION about \
their CLAIM. The person is an operator/leader, NOT a developer.

Sort answer content into three levels:
- CORE REASONING (the 'why') -- required at every tier.
- KEY SUPPORTING DETAILS -- the substantive ideas that make the reasoning complete.
- LOOKUP MINUTIAE (exact numbers, names, mechanics) -- NEVER required; never penalize a miss here.
Catch genuine misunderstandings even when they sound like small details (a wrong 'why' \
dressed as a detail). Do NOT penalize fuzzy or missing minutiae.

RISING RIGOR BY TIER -- what it takes to earn 'solid' rises with the tier:
- spot:   core reasoning present, even if supporting details are thin -> solid.
- short:  core reasoning, articulated cleanly.
- medium: core reasoning AND the key supporting details -> solid; thin-but-right is only 'partial'.
- long:   complete and interview-defensible (reasoning + key details, cold) -> solid.

Judge RELATIVE TO THE QUESTION asked. If the question was vague/ambiguous, set \
ambiguous_question true and do NOT penalize the user for it.

verdict: 'solid' = meets this tier's bar (pass); 'partial' = reasoning present but short \
of this tier's bar; 'wrong' = reasoning incorrect or absent. score: 5 = fully meets the \
bar, 3 = partial, 1 = wrong/absent.

ALWAYS fill complete_answer with what a full answer includes -- especially the key \
supporting details the user did not mention -- for their learning."""

_judge_llm = ChatAnthropic(model=config.MODEL, max_tokens=1024, temperature=0, max_retries=5).with_structured_output(_Judgment)


def judge_answer(claim_text, decision_summary, question, answer, tier):
    """Judge the user's answer at the rigor required for this tier. Returns a dict
    with score, verdict, rationale, ambiguous_question, complete_answer.
    UNCALIBRATED -- scores are not yet trustworthy (see Week 4 calibration)."""
    prompt = (
        f"{_JUDGE_INSTRUCTION}\n\n"
        f"Decision: {decision_summary}\n"
        f"Claim: {claim_text}\n"
        f"Current tier (sets the rigor bar): {tier}\n"
        f"Question asked: {question}\n"
        f"The person's answer: {answer}"
    )
    return _judge_llm.invoke(prompt).model_dump()


# --- The tension-detector (Week 6): rigorous, additive-only, conservative. ---
class _Tension(BaseModel):
    has_tension: bool = Field(description="True ONLY if there is genuine tension to reconcile.")
    statement: str = Field(description="If has_tension: one sentence stating the tension to reconcile. Else empty.")


_TENSION_INSTRUCTION = """You judge whether two of a person's OWN past decisions are in \
GENUINE TENSION -- a real contradiction, inconsistency, or conflicting application of a \
principle that the person would need to reconcile and defend.

Be RIGOROUS and CONSERVATIVE. This is ADDITIVE-ONLY: only flag tension that genuinely \
exists and is worth the person's effort to resolve. The DEFAULT answer is NO tension.
- NOT tension: the two claims are merely on a similar topic; they AGREE; they apply the \
same principle consistently to different cases; they are simply unrelated.
- TENSION: the two claims pull in opposite directions, rest on conflicting assumptions, \
or apply a principle inconsistently in a way the person would have to defend.

When uncertain, answer NO tension -- a false tension is worse than a missed one. If and \
only if there is genuine tension, state it in one sentence the person could reconcile."""

_tension_llm = ChatAnthropic(model=config.MODEL, max_tokens=512, temperature=0, max_retries=5).with_structured_output(_Tension)


def detect_tension(claim_a, claim_b):
    """Conservative check for GENUINE tension between two of the user's own claims.
    Additive-only: the default is no tension. Returns {has_tension, statement}."""
    prompt = f"{_TENSION_INSTRUCTION}\n\nClaim A: {claim_a}\nClaim B: {claim_b}"
    return _tension_llm.invoke(prompt).model_dump()


# --- One follow-up for a PARTIAL answer (deferred from Week 3; judge now calibrated). ---
class _Followup(BaseModel):
    question: str = Field(description="One focused follow-up targeting the specific missing piece.")


_FOLLOWUP_INSTRUCTION = """The person gave a PARTIAL answer -- the core reasoning is there \
but something the tier requires is missing. Ask ONE focused follow-up that gives them a \
chance to supply the SPECIFIC missing piece (per the judge's note). Operator-level, plain \
English, exactly one question. Do not re-ask the whole thing and do not hint at the answer."""

_followup_llm = ChatAnthropic(model=config.MODEL, max_tokens=256, temperature=0, max_retries=5).with_structured_output(_Followup)


def followup_question(claim_text, original_question, answer, judge_rationale):
    """One targeted follow-up aimed at the gap the judge identified in a partial answer."""
    prompt = (f"{_FOLLOWUP_INSTRUCTION}\n\nClaim: {claim_text}\n"
              f"Original question: {original_question}\nTheir answer: {answer}\n"
              f"What's missing (judge's note): {judge_rationale}")
    return _followup_llm.invoke(prompt).question
