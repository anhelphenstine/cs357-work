# OpenCode Studio Search — MVP Specification

## Feature summary

A Python 3 command-line program that searches a fixed local knowledge base of plain UTF-8 `.txt` files. It performs a case-insensitive whole-query substring search, aggregates matches per file, ranks files by a deterministic normalized match count, and prints JSON to stdout.

The MVP:

- Uses only the Python standard library.
- Reads only `artifact/knowledge_base/` [GUESS: resolved relative to `search.py`].
- Indexes only regular `.txt` files directly inside that directory [GUESS: non-recursive].
- Ignores non-`.txt` files, directories, and symlinks.
- Does not access files outside the knowledge base directory.
- Returns one JSON object per matching file.
- Supports a caller-supplied result limit.
- Is deterministic: the same knowledge base, query, and options produce byte-identical stdout and the same exit code.
- Performs no network access and writes no knowledge-base files during a normal search.

Out of scope for this MVP: GUI, server, configuration file, persistent index, fuzzy matching, stemming, ranking beyond the score defined below, and recursive directory traversal.

## Entry point

```text
python artifact/search.py "<query>" [--max-results N]
```

- `"<query>"` is the first positional argument and is required.
- `--max-results N` is optional, defaults to `10`, and accepts positive integers only.
- `--max-results=N` is also accepted [GUESS].
- A literal `--` ends option parsing so a query may begin with `-` [GUESS].
- No other flags are part of the MVP; `-h` and `--help` are treated as unknown options [GUESS].
- Run from the repository root or any working directory; the knowledge base is resolved from the location of `search.py` [GUESS].

Examples:

```text
python artifact/search.py "installation"
python artifact/search.py "installation" --max-results 5
```

## Inputs table

| Input | Provided by | Required | Default | Contract |
|---|---|---|---|---|
| Query | first positional argument | yes | none | Non-empty; used as provided; empty or whitespace-only is a usage error [GUESS] |
| Max results | `--max-results N` | no | `10` | Integer `N >= 1`; zero, negatives, non-integers, and missing values are usage errors |
| Knowledge base directory | fixed path `artifact/knowledge_base/` | yes | none | Must exist, be a directory, and be readable; missing or unreadable is exit 3; never created by `search.py` |
| Candidate documents | `.txt` files directly inside the knowledge base | yes | none | Plain UTF-8; regular files only; symlinks skipped; non-`.txt` ignored; no recursion [GUESS] |

## Outputs

On exit 0, stdout is a JSON array containing one object per matching file:

```json
[{"title": "notes", "score": 1.0, "source": "notes.txt"}]
```

Each object has exactly these fields:

| Field | Type | Meaning |
|---|---|---|
| `title` | string | File name with the exact `.txt` suffix removed [GUESS] |
| `score` | float | Relevance from `0.0` to `1.0`, rounded to four decimal places |
| `source` | string | Path relative to the knowledge base root, using `/` separators [GUESS] |

Score calculation:

1. Convert the query and full file text to case-insensitive form with Python `str.casefold()` [GUESS].
2. Count non-overlapping occurrences of the query within the file text using `str.count()` [GUESS].
3. Let `top` be the highest occurrence count among all candidate files.
4. `score = round(count / top, 4)`.
5. No Unicode normalization is applied [GUESS]; matches may span line boundaries [GUESS].

Ordering and limiting:

- Sort by `score` descending.
- Break ties by `source` ascending [GUESS].
- Apply `--max-results` after sorting.
- Emit JSON as one line followed by a newline, using UTF-8 and `ensure_ascii=False` [GUESS].
- stdout contains only the JSON result; warnings and errors go to stderr.
- With no matches, stdout is exactly `[]` and the exit code is 1.

## Error behavior with exit codes

| Exit code | Condition | stdout | stderr |
|---:|---|---|---|
| 0 | At least one match found | JSON array, non-empty after limiting | Empty, except optional per-file warnings [GUESS] |
| 1 | No matches found | `[]` | Empty, except optional per-file warnings [GUESS] |
| 2 | Usage error | Empty | Plain-text error message |
| 3 | Knowledge base missing, not a directory, or unreadable | Empty | Plain-text error message |
| 4 | Unexpected internal error | Empty | Plain-text error message; no traceback [GUESS] |

Additional rules:

- A missing knowledge base is exit 3; the program must not create it.
- A knowledge base containing zero `.txt` files produces `[]` and exit 1.
- An individual `.txt` file that cannot be read or decoded is skipped with a warning to stderr; it does not change the exit code [GUESS].
- Usage errors include: missing query, extra positional arguments, unknown options, empty/whitespace-only query, and invalid `--max-results` values.
- Unexpected exceptions are caught and reported as exit 4 [GUESS].

## Testing criteria

1. **Deterministic happy path.** Given known `.txt` fixtures, a matching query returns exit 0 and valid JSON with the expected titles, scores, and sources; two identical runs produce byte-identical stdout.
2. **Case-insensitivity and scoring.** Queries differing only by case return the same files and scores; known occurrence counts produce the specified normalized scores; ordering and `source` tie-breaking are correct.
3. **Filtering and isolation.** Non-`.txt` files, symlinks, subdirectories [GUESS], and files outside the knowledge base are ignored; only regular `.txt` files directly inside the knowledge base are read.
4. **CLI validation and limiting.** Missing query, extra arguments, unknown options, and invalid `--max-results` values return exit 2 with empty stdout; the default limit is 10; explicit limits truncate after sorting.
5. **Error paths and cleanup.** Missing or unreadable knowledge base returns exit 3 without creating it; no matches returns `[]` with exit 1; unreadable/undecodable files are skipped with warnings [GUESS]; unexpected internal failure returns exit 4 [GUESS]; all temporary test fixtures are removed afterward.

Test execution [GUESS]:

```text
python artifact/test_search.py
```

Tests use the standard-library `unittest` framework and must be deterministic.

## Files the agent may create or modify
artifact/search.py, artifact/test_search.py

No other repository file is authorized by this specification. `spec.md` is created once with user approval; implementation agents may not modify it.

## Files the agent must NOT touch
spec.md, AGENTS.md, CHARTER.md, .ai/, docs/, transcripts/

