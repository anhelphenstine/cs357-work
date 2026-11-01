Decision Log 

Decision: Add a gate tool restriction in opencode.json to deny rm commands. 

Alternative: Rely only on the written rules in AGENTS.md to tell the agent to never use rm -rf and to ask before it deletes files. 

Reason: Relying on the written instructions in AGENTS.md relies on the model correctly interpreting and following the instructions laid out in the AGENTS.md. The gate tool provides additional protextion by rejected commands before the AGENTS.md is read. This decision was made in part 3 of the assignment.
