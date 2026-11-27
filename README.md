# AIJL Agent Kit for Microsoft Fabric

From AI Journey Labs Pty Ltd. The kit sets up an AI coding agent (Claude Code, or GitHub Copilot in VS Code) to act as a supervised senior Microsoft Fabric Developer for your organisation. It gives the agent operating rules, a structured place for context about your organisation and its Fabric environment, a review, plan and approve workflow, and permanent records of everything it does.

The repository holds no credentials and no Fabric items. Fabric items live in your Fabric environment repo and in Fabric itself.

All agent output must be reviewed by a person before it is acted on. The agent works in development workspaces only and implements nothing without a plan approved by a named person.

## Workflow

Review, then plan, then approval by a named person, then implementation in development only, then documentation and a context update.

## Creating your organisation's repository

This repository is a GitHub template. Do not fork it or work in it directly.

1. On the kit's GitHub page, choose **Use this template**, then **Create a new repository**.
2. Create the repository in your organisation's GitHub account and make it **private**. It will hold your organisation profile, strategy summaries and records of your Fabric environment.
3. Decide how changes reach `main`. Branch protection is not copied from a template, so your repository starts without it. If your organisation requires pull requests on `main`, add that rule yourself; ID allocations and plan approvals then go through pull requests too (see "Working alongside other operators" in `docs/operator_guide.md`).
4. Keep `KIT_VERSION` as it is. It records the kit version your repository is on, and you need it when you upgrade.

A repository created from a template has no link back to the kit. You receive kit updates only by upgrading (see "Upgrading the kit" below).

## Getting started

Setup works on Windows, macOS and Linux.

1. Install the tools and clone your organisation's repository (`SETUP.md` steps 1 and 2).
2. Run `python scripts/kit_setup.py` from the repository root (`python3` on macOS and Linux). It checks your tools and generates the agent's MCP configuration for your platform.
3. Open the folder in VS Code, start Claude Code, or select the Fabric Developer agent in GitHub Copilot Chat, and say "Set yourself up".

The agent then walks you through setup one stage at a time: your organisation profile, data strategy and other reference documents, roles and approvers, an outline of your Fabric environment, the access request for your IT team, each operator's workstation and connection check, and a read-only discovery of the development workspaces. Progress is recorded in `agent_context/setup_status.md`, so you can stop and resume. Until setup is complete, the agent works on setup only.

`SETUP.md` has the full workstation checklist, and `docs/README.md` the reading order for everything else.

## Layout

| Path | Contents |
|---|---|
| `AGENTS.md` | Operating rules, shared by Claude Code and GitHub Copilot |
| `CLAUDE.md` | Imports `AGENTS.md`, plus notes specific to Claude Code |
| `SETUP.md` | Workstation setup checklist |
| `KIT_VERSION`, `KIT_CHANGELOG.md` | Kit version and the changes in each version |
| `LICENSE`, `NOTICE` | Apache License 2.0, and the copyright notice |
| `SECURITY.md` | How to report a security problem in the kit |
| `.mcp.json` | MCP servers used by the agent, generated for your platform by `scripts/kit_setup.py` (git-ignored) |
| `.claude/settings.json` | Permission rules: what runs freely, what asks, what is denied |
| `.claude/settings.local.json.example` | Names of the local credential variables (no values) |
| `.claude/skills/` | Packaged agent procedures: setup, requirement assessment, reference document summaries (the source) |
| `.github/agents/fabric-developer.agent.md` | The Fabric Developer agent for GitHub Copilot: Copilot specifics and its tool list |
| `.github/skills/` | Generated copy of `.claude/skills/` for GitHub Copilot |
| `.github/workflows/check-skills.yml` | Fails a pull request if the Copilot copy of the skills is out of date |
| `.github/workflows/check-setup.yml` | Runs the setup script on Windows, macOS and Linux when it changes |
| `.gitattributes` | Keeps line endings the same on every platform |
| `scripts/kit_setup.py` | Sets up and checks an operator workstation |
| `scripts/mcp_servers.json` | The MCP servers and their pinned versions, from which `.mcp.json` is generated |
| `scripts/copilot_terminal_rules.json` | Terminal rules for GitHub Copilot, added to each operator's VS Code User settings |
| `scripts/sync_skills.py` | Updates `.github/skills/` from `.claude/skills/` |
| `.vscode/extensions.json` | Recommends the Claude Code and GitHub Copilot Chat extensions |
| `agent_context/master_context.md` | Index to the context |
| `agent_context/setup_status.md` | Progress of the agent's setup and each operator's connection check |
| `agent_context/organisation/` | Your organisation profile, data strategy summary, and reference documents (Markdown or PDF) |
| `agent_context/context/` | Topic files about your Fabric environment, including your rules for particular item types and your code and documentation standards |
| `agent_context/fabric_item_guides/` | The kit's general guidance for particular Fabric item types, such as notebooks and data agents |
| `agent_context/enhancements/`, `bug_fixes/` | Briefs from operators |
| `agent_context/requirements/` | Business requirements, one folder per `R#####`, and their register |
| `agent_output/` | Reviews, plans, change records, recommendations, baselines and the registers |
| `docs/` | Guides for people: overview, FAQs for leadership and the Fabric administrator, operator guide, security, records, troubleshooting |

## Kit files and organisation files

The kit separates the files it owns from the files your organisation fills in, so that a new kit version can be applied without losing your content.

**Kit files** are replaced when you upgrade. Do not record anything about your organisation in them:

- `AGENTS.md`, `CLAUDE.md`, `README.md`, `SETUP.md`, `KIT_VERSION`, `KIT_CHANGELOG.md`, `LICENSE`, `NOTICE`, `SECURITY.md`
- `.gitignore`, `.gitattributes`, `.claude/settings.json`, `.claude/settings.local.json.example`, `.claude/skills/`
- `.github/agents/`, `.github/skills/`, `.github/workflows/check-skills.yml`, `.github/workflows/check-setup.yml`, `scripts/`, `.vscode/extensions.json`
- `agent_context/master_context.md`
- `agent_context/fabric_item_guides/`
- every `README.md`, `_template/` and `_templates/` folder under `agent_context/`, `agent_output/` and `docs/` (including `agent_context/organisation/reference/README.md`)
- every other file in `docs/`, except your own process documents and their index (`index.md`) in `docs/processes/`

**Organisation files** are yours. The kit supplies a starting version and never overwrites them:

- `agent_context/setup_status.md`
- `agent_context/organisation/profile.md` and `data_strategy.md`
- `agent_context/organisation/reference/index.md`, your reference documents and their summaries
- `agent_context/context/01` to `07`
- `agent_context/requirements/register.md` and the `R#####` folders
- your briefs in `agent_context/enhancements/` and `agent_context/bug_fixes/`
- everything in `agent_output/` except its `README.md` and `_templates/`
- your process documents in `docs/processes/`, and their index, `docs/processes/index.md`
- `.claude/settings.local.json` and `.mcp.json` (local to each workstation, never committed; `.mcp.json` is regenerated by `scripts/kit_setup.py`)

If you need to change a kit file, record it as a change (`CHG-###`) and list the file in the change record's "Kit files changed" field, so it can be carried forward at the next upgrade.

## Upgrading the kit

An upgrade replaces the agent's rules, permission settings and MCP server versions. Treat it as a change to the agent: record it, do it on a branch, and have it reviewed before it reaches `main`.

1. Read `KIT_CHANGELOG.md` in the kit repository for every version after the one in your `KIT_VERSION`. Each entry's "Upgrading from the previous version" section lists the kit files added, removed and renamed, and any changes to the starting versions of organisation files.
2. Allocate a `CHG-###` for the upgrade in `agent_output/change_log.md`, and create a branch for it.
3. Download the release for the new version from the kit repository into a separate folder. Releases are tagged with the version, for example `v0.2.0`. Do not unzip or copy the whole download over your repository: it holds blank starting versions of your organisation files, and would replace your content.
4. Copy only the kit files, as listed above, from the download into your repository.
5. Delete each kit file the changelog lists as removed or renamed. A retired skill, guide or script that is left in place is still read and used by the agent.
6. Reapply the changes your organisation made to kit files. Each is listed in the "Kit files changed" field of its change record.
7. Merge any new starting content (for example, new platform gotchas) into your organisation files by hand, and copy in any organisation file the new version adds that you do not have yet. `KIT_CHANGELOG.md` lists them.
8. Check the result before you commit. `git status` and `git diff` should show changes to kit files only, apart from what you merged in step 7. Run `python scripts/sync_skills.py --check`.
9. Commit with the kit version in the commit message, complete the change record, and merge the branch.
10. On each workstation, after pulling the upgrade, run `python scripts/kit_setup.py` so that `.mcp.json` matches the new version, then fully restart VS Code. Until an operator does this, their MCP servers are still the previous version's.

## Disclaimer

The kit is provided "as is", without warranties or conditions of any kind, and to the extent permitted by law AI Journey Labs Pty Ltd accepts no liability arising from its use. See sections 7 and 8 of the Apache License 2.0.

The kit configures an AI agent, and AI agents make mistakes. Every plan and record the agent produces must be reviewed by a person before it is acted on. The kit's rules and permission settings reduce risk; they do not remove it, and they do not replace your organisation's own access controls.

Your organisation remains responsible for changes to its Fabric environment, for its data, and for compliance with its own policies and the regulation that applies to it. This includes deciding what data the agent can access and which AI model providers it sends that data to, and complying with those providers' terms and with your privacy and data-handling obligations.

Microsoft, Microsoft Fabric, Power BI, GitHub, GitHub Copilot, Visual Studio Code, Claude and Claude Code are trademarks of their respective owners. AI Journey Labs Pty Ltd is not affiliated with or endorsed by them. The MCP servers and AI services the kit works with are third-party software and services, provided under their own licences and terms, and are not controlled or warranted by AI Journey Labs. The names "AI Journey Labs" and "AIJL" are not licensed under the Apache License.

## Licence

Copyright 2026 AI Journey Labs Pty Ltd. Licensed under the Apache License, Version 2.0; see `LICENSE` and `NOTICE`. The licence covers the kit itself. AI Journey Labs claims no rights in content your organisation adds to its own repository, such as its profile, reference documents, context and records.