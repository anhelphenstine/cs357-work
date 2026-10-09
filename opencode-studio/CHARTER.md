# OpenCode Studio

## Master Project Charter, Engineering Workflow, and Autonomous Development Plan

<!-- The constitution.  Written once at project start, amended deliberately and rarely.
     Every agent session begins by (re)reading this document. Everything an agent is
     allowed or forbidden to do should trace back to a section here. -->

# Project Mission

The mission of this project is to create a reliable search program where the user can search from a local knowledge base. The program should give consistent and accurate results and should be simple to use. The program should handle errors appropriately. 

# Engineering Philosophy

Every engineering decision should prioritize, in order:

1.  Accuracy over speed
2.  Reproducibility over automation
3.  Ask for consent over assuming permission
4.  Small, reversible steps over large ones
5.  Simplicity over complexity

<!-- The ranking matters more than the list.  When two values conflict mid-task,
     the agent resolves the conflict by rank instead of asking or guessing. -->

# Definition of Success

A classmate could clone the repository and repeat all actions. They would come up with the same results. 

# Repository Layout

```
OpenCode Studio/
|-- START_HERE.md          # entry funnel: the fixed read order for any new agent
|-- CHARTER.md             # the constitution: the mission, philosophy, rules, milestones guardrails
|-- .ai/                   # agent handoff state (see .ai/ templates)
|-- docs/                  # roadmap, decisions, rfcs, build/test guides
|-- sources/               # IMMUTABLE inputs - never edited, only read
`-- work/                  # all development happens here
```

Everything under `sources/` is immutable.  Development occurs only inside `work/`.

# Git Policy

Git is the only version history.  Never create `*_new`, `*_old`, `*_backup`, `*_fixed`, or duplicate edited files.  Overwrite files normally.  Commit frequently.  Each commit should represent one logical enAgineering change.  Documentation is committed alongside implementation.

# Documentation Authority Rule

The agent shall never work from memory when project documentation exists.  Before every engineering session, the agent shall reread the charter, roadmap, current task, and session log.

If project documentation conflicts with remembered context, prior chat context, historical notes, or assumptions, the project documentation wins.  If the documentation is incomplete, update it rather than relying on memory.  This rule exists to prevent context drift across long-running autonomous sessions.

# Development Workflow

Every task follows this loop:

1.  Investigate.
2.  Read existing documentation.
3.  Read historical notes.
4.  Document findings.
5.  Produce a short implementation plan.
6.  Implement the smallest useful change.
7.  Automatically build.
8.  Automatically test.
9.  Automatically collect logs.
10.  Update documentation.
11.  Commit a single logical change.

# Project Milestones

<!-- Milestone 0 is always initialization: scaffolding, docs, and inventory only.
     No feature work. This gate is what makes everything else recoverable. -->

## Milestone 0: Project Initialization

Objectives:
- Create the repository scaffolding, documentation set, and input inventory.
- Establish the build and test baseline.  No feature work.

Deliverable: a repository in which every later milestone can be executed by a fresh agent using only these documents.

Success Criteria: a new agent reading only this repository can state the mission, the current task, and the next safe action.

**Stop after Milestone 0 is complete.  Do not begin Milestone 1 until explicitly directed.**

## Milestone 1: <Name>

Objectives:
- <objective>

Deliverable: <deliverable>

Success Criteria: <observable criteria>

<!-- ...repeat per milestone... -->

# Decision Logging

Every architectural decision should be recorded in `docs/DECISION_LOG.md`.  Include: decision, rationale, alternatives considered, long-term implications.  Future contributors should understand why the project evolved as it did.

# Guiding Principle

Every completed task should improve at least one of: correctness, reproducibility, documentation, test coverage, logging, observability, maintainability, or autonomous verification.  The repository should become easier for the next contributor than it was for the current contributor.









