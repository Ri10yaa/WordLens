"""Command line interface for testing the dictionary agent."""

import argparse

from agent.runtime import run_agent


def main():
    parser = argparse.ArgumentParser(description="AI Dictionary Agent CLI")
    parser.add_argument("word", help="Word to analyze")
    parser.add_argument("sentence", help="Sentence providing context")
    args = parser.parse_args()

    result = run_agent(args.word, args.sentence)
    print(result)


if __name__ == "__main__":
    main()
