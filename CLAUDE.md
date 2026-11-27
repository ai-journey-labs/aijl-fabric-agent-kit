# Claude Code instructions

The operating rules are in `AGENTS.md`, shared with GitHub Copilot. They apply in full.

@AGENTS.md

## Claude Code specifics

- Permission rules are in `.claude/settings.json`: reads run freely, anything that writes or consumes capacity asks, destructive operations are denied. Do not try to work around a denied or refused tool call; raise it.
- Run commands with the Bash tool (Git Bash on Windows). The PowerShell tool is denied, because the command rules are written for Bash.
- Skills in `.claude/skills/`: `fabric-setup` for setting the agent up and onboarding operators, `fabric-assess-requirement` for requirement assessments, `fabric-summarise-reference` for summarising the data strategy and other reference documents. This folder is the source; after changing a skill, run `python scripts/sync_skills.py` to update the Copilot copy.
- Credentials are set in the git-ignored `.claude/settings.local.json`. Never read, print or copy credential files or values.
