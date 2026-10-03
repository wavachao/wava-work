"""Validate single-line Conventional Commit messages in reachable Git history."""
import argparse
import re
import subprocess

PATTERN = re.compile(r"(?:feat|fix|docs|refactor|perf|test|build|ci|chore|revert)(?:\([a-z0-9][a-z0-9._/-]*\))?!?: \S[^\r\n]*")


def valid_message(message):
    # Git normally terminates the message with one newline; it is not a body.
    if message.endswith("\n"):
        message = message[:-1]
    return bool(PATTERN.fullmatch(message)) and message == message.rstrip()


def check(ref="HEAD"):
    commits = subprocess.check_output(["git", "rev-list", ref], text=True).splitlines()
    failures = []
    for sha in commits:
        raw = subprocess.check_output(["git", "cat-file", "commit", sha])
        message = raw.split(b"\n\n", 1)[1].decode("utf-8")
        if not valid_message(message):
            failures.append(sha)
    return commits, failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Commit or revision range (default: all HEAD history)")
    args = parser.parse_args()
    try:
        commits, failures = check(args.ref)
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        parser.exit(1, f"Could not inspect Git history: {exc}\n")
    for sha in failures:
        print(f"Invalid commit message: {sha}")
    if failures:
        parser.exit(1, "Expected a single-line Conventional Commit without body or trailers.\n")
    print(f"Validated {len(commits)} single-line Conventional Commits.")


if __name__ == "__main__":
    main()
