#!/usr/bin/env python3
"""Search a fixed local knowledge base of plain UTF-8 text files."""

import json
import os
import sys
from pathlib import Path


DEFAULT_MAX_RESULTS = 10

EXIT_MATCH = 0
EXIT_NO_MATCH = 1
EXIT_USAGE = 2
EXIT_KNOWLEDGE_BASE = 3
EXIT_INTERNAL = 4


class UsageError(Exception):
    """Raised when the command line is invalid."""


class KnowledgeBaseError(Exception):
    """Raised when the knowledge base cannot be read."""


def knowledge_base_dir():
    """Return the fixed knowledge base directory next to this script."""
    return Path(__file__).resolve().parent / "knowledge_base"


def parse_max_results(value):
    try:
        number = int(value, 10)
    except (TypeError, ValueError):
        raise UsageError("--max-results must be a positive integer")
    if number < 1:
        raise UsageError("--max-results must be a positive integer")
    return number


def parse_args(argv):
    max_results = DEFAULT_MAX_RESULTS
    positionals = []
    end_of_options = False

    index = 0
    while index < len(argv):
        argument = argv[index]
        if end_of_options:
            positionals.append(argument)
        elif argument == "--":
            end_of_options = True
        elif argument == "--max-results":
            if index + 1 >= len(argv):
                raise UsageError("--max-results requires a value")
            index += 1
            max_results = parse_max_results(argv[index])
        elif argument.startswith("--max-results="):
            max_results = parse_max_results(argument.split("=", 1)[1])
        elif argument.startswith("-") and argument != "-":
            raise UsageError("unknown option: {}".format(argument))
        else:
            positionals.append(argument)
        index += 1

    if not positionals:
        raise UsageError("missing query")
    if len(positionals) > 1:
        raise UsageError("too many positional arguments")

    query = positionals[0]
    if query.strip() == "":
        raise UsageError("query must not be empty or whitespace-only")

    return query, max_results


def candidate_files(knowledge_base):
    try:
        with os.scandir(knowledge_base) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
    except OSError as error:
        raise KnowledgeBaseError(
            "cannot read knowledge base: {}".format(error)
        )

    for entry in ordered:
        if not entry.name.endswith(".txt"):
            continue
        if entry.is_symlink():
            continue
        if not entry.is_file(follow_symlinks=False):
            continue
        yield entry


def search(knowledge_base, query, max_results):
    folded_query = query.casefold()
    matches = []
    top = 0

    for entry in candidate_files(knowledge_base):
        try:
            with open(entry.path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except (OSError, UnicodeError) as error:
            print(
                "warning: skipping {}: {}".format(entry.name, error),
                file=sys.stderr,
            )
            continue

        count = text.casefold().count(folded_query)
        if count > top:
            top = count
        if count > 0:
            matches.append((entry.name[:-4], count, entry.name))

    if top == 0 or not matches:
        return []

    results = [
        {
            "title": title,
            "score": round(count / top, 4),
            "source": source,
        }
        for title, count, source in matches
    ]
    results.sort(key=lambda item: (-item["score"], item["source"]))
    return results[:max_results]


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    try:
        query, max_results = parse_args(argv)
    except UsageError as error:
        print("error: {}".format(error), file=sys.stderr)
        return EXIT_USAGE

    knowledge_base = knowledge_base_dir()
    if not knowledge_base.exists() or not knowledge_base.is_dir():
        print(
            "error: knowledge base is missing or not a directory: {}".format(
                knowledge_base
            ),
            file=sys.stderr,
        )
        return EXIT_KNOWLEDGE_BASE
    if not os.access(str(knowledge_base), os.R_OK):
        print(
            "error: knowledge base is not readable: {}".format(knowledge_base),
            file=sys.stderr,
        )
        return EXIT_KNOWLEDGE_BASE

    try:
        results = search(knowledge_base, query, max_results)
    except KnowledgeBaseError as error:
        print("error: {}".format(error), file=sys.stderr)
        return EXIT_KNOWLEDGE_BASE

    if results:
        sys.stdout.write(json.dumps(results, ensure_ascii=False) + "\n")
        return EXIT_MATCH

    sys.stdout.write("[]\n")
    return EXIT_NO_MATCH


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(
            "error: unexpected internal error: {}".format(error),
            file=sys.stderr,
        )
        sys.exit(EXIT_INTERNAL)
