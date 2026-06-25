import argparse

import store
import graph
import session


def main():
    # Make sure the database + corpus exist (safe to run every launch), then
    # build the orchestrator once for this run.
    store.init_db()
    app = graph.build()

    # Define the commands the user can type and what options each one takes.
    parser = argparse.ArgumentParser(prog="companion",
                                     description="Learning Companion v0")
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Log a build decision in your own words.")
    p_log.add_argument("text", help="Your note describing the decision.")

    p_query = sub.add_parser("query", help="Show past decisions.")
    p_query.add_argument("--tag", help="Only decisions carrying this tag.")
    p_query.add_argument("--since", help="Only decisions on/after this date (YYYY-MM-DD).")
    p_query.add_argument("--find", help="Semantic search by meaning (natural language).")

    sub.add_parser("check", help="Run an interactive BS-check review session.")

    args = parser.parse_args()

    # The interactive review runs at the command layer, not through the routing
    # graph -- a back-and-forth conversation doesn't fit a single-shot flowchart.
    if args.command == "check":
        session.run_check()
        return

    # Translate the typed command into the 'working note' the orchestrator routes.
    if args.command == "log":
        state = {"mode": "log", "text": args.text}
    else:  # query
        state = {"mode": "query", "tag": args.tag, "since": args.since, "find": args.find}

    # One trip through the flowchart; print whatever it hands back.
    print(app.invoke(state)["result"])


if __name__ == "__main__":
    main()
