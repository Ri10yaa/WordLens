"""Command line interface for testing the dictionary agent."""

import argparse

from agent.runtime import run_agent


def main():
    parser = argparse.ArgumentParser(description="AI Dictionary Agent CLI")
    parser.add_argument("prompt", help="User prompt to send to the agent")
    args = parser.parse_args()

    result = run_agent(args.prompt)
    print(result)


if __name__ == "__main__":
    main()
