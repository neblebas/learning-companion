import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve the canonical .env relative to THIS file, not the current working
# directory — so it loads correctly no matter where you run python from.
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)

# A stray empty ANTHROPIC_API_KEY in the shell would silently shadow the real
# one from .env; override=True above forces the .env value to win.

# The sandbox injects an empty ANTHROPIC_AUTH_TOKEN. The Anthropic SDK reads
# AUTH_TOKEN before API_KEY; an empty value makes a malformed "Bearer " header
# and fails with a misleading "Connection error". Remove it.
os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

# LangGraph/LangChain auto-init LangSmith tracing on import. Disable it here,
# before any langchain module is imported, so the setting takes effect.
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# Fail loud and early if the key didn't load — beats a confusing API error later.
if not os.environ.get("ANTHROPIC_API_KEY"):
    raise RuntimeError(f"ANTHROPIC_API_KEY not found. Looked in {_ENV_PATH}")

# Explicit choices, visible in code rather than buried in env.
MODEL = "claude-sonnet-4-6"

# Durable-data locations (the corpus store uses these).
APP_DIR = Path(__file__).resolve().parent
CORPUS_DIR = APP_DIR / "corpus"
DB_PATH = APP_DIR / "companion.db"
