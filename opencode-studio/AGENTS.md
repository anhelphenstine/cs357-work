# Agent Contract

## What this project is
OpenCode Studio is a Python 3 command-line search program over a fixed local
knowledge base of plain UTF-8 `.txt` files; it returns deterministic,
case-insensitive whole-query substring matches as JSON, with accurate scoring
and clean error handling.

## Read first, every session
Read these paths, in this order:
1. `START_HERE.md`
2. `CHARTER.md`
3. `spec.md`
4. `.ai/MEMORY.md`
5. `AGENTS.md`

Then run `git log --oneline -5`. Before proposing any action, state the project
mission in one sentence. If `AGENTS.md` and `CHARTER.md` disagree, `CHARTER.md`
wins.

## Zones
### May edit without asking
- `artifact/search.py`
- `artifact/test_search.py`

Read any repository path. Do not treat reading as authorization to write.

### May not edit without a confirmation gate
- `CHARTER.md`
- `AGENTS.md`
- `spec.md`
- `.ai/CONTEXT.md`
- `.ai/CURRENT_TASK.md`
- `.ai/SESSION.md`
- `.ai/MEMORY.md`
- `docs/`
- `transcripts/`
- `artifact/` paths other than `artifact/search.py` and
  `artifact/test_search.py`

`transcripts/` is append-only evidence. Create a new file or append only when
asked to save a transcript. Never rewrite or delete an existing transcript.

## Confirmation gates
1. Before any git push, stop and request approval.
   Show the branch and remote first.

2. Before deleting any file in artifact/,
   stop and request approval.
   Show the exact target path before proceeding.

3. Ask before each of these named operations:
- `edit CHARTER.md`
- `edit AGENTS.md`
- `edit spec.md`
- `edit .ai/CONTEXT.md`
- `write .ai/CURRENT_TASK.md`
- `edit .ai/CURRENT_TASK.md`
- `write .ai/SESSION.md`
- `edit .ai/SESSION.md`
- `edit .ai/MEMORY.md`
- `delete .ai/MEMORY.md`
- `write docs/`
- `edit docs/`
- `delete docs/`
- `write transcripts/` (new path only)
- `write artifact/` (any path other than `artifact/search.py` and
  `artifact/test_search.py`)
- `delete artifact/`
- `git commit`
- `git push`
- `git reset --hard`
- `git clean -fd`
- `git push --force`
- `gh repo create`
- `gh issue create`
- `gh pr create`
- `gh pr review`

When a gate applies, name the operation, name the path or command, explain why,
and wait for an explicit yes. Silence is not consent.

4. Never run `rm -rf`. Ask before deleting anything.

## Durable memory
When you learn something about this project that would be useful to a session
that has never seen it, append it to `.ai/MEMORY.md` under a dated heading.
Append only. Never rewrite or delete an existing entry. `append .ai/MEMORY.md`
is pre-authorized; `edit .ai/MEMORY.md` and `delete .ai/MEMORY.md` require a
confirmation gate.

## Escalation rule
Stop and ask when a confirmation gate applies, when `CHARTER.md`, `spec.md`, and
`AGENTS.md` conflict, when a command prompts for a password or returns 401 or
403, or when the next step requires writing a path not listed under "May edit
without asking." In that message, name the operation, name the path or command,
quote the failure, and propose the smallest safe next step. Do not retry in a
loop.

## GitHub: try gh, fall back to git, then ask
1. Reach for `gh` first for anything GitHub-side: creating and cloning
   repositories, issues, pull requests, reviews. Confirm once per session
   with `gh auth status`.
2. Fall back to `git` for what it does on its own: pull, add, commit, push,
   log, change. Say in your next message that you fell back, and why.
3. If both fail, stop and ask me. A push that prompts for a password, or a
   401 or 403 from either tool, means there is no working credential here.
   Tell me which command failed and quote what it said. Do not switch the
   remote between HTTPS and SSH, do not ask me to paste a token into a
   file, and do not retry in a loop.

## Credentials
Never ask me to paste a token, key, or password into this conversation, and
never print one into your output. If a task needs a secret, stop and tell me
which environment variable should hold it, then assume it is set. If you find
a credential in a file, do not repeat it back to me: say where it is and that
it should be moved and rotated.
