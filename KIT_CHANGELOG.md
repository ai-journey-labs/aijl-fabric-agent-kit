# Kit changelog

Changes to the AIJL Agent Kit for Microsoft Fabric. This file is about the kit itself; changes to an organisation's environment are recorded in `agent_output/change_log.md`.

The current version is in `KIT_VERSION`. Each version is tagged in the kit repository with a `v` and its number, for example `v0.1.0`.

From the second version onwards, each entry has a section "Upgrading from the previous version". It lists the kit files added, removed and renamed, changes to the starting versions of organisation files, and anything operators must repeat on their workstations. How to upgrade is in `README.md`.

## 0.1.0 (27 Nov 2026)

First public version, published as a GitHub template repository under the Apache License 2.0.

### Included

- **Operating rules** in `AGENTS.md`, shared by Claude Code and GitHub Copilot and imported by `CLAUDE.md`:
  - Ten non-negotiable rules. The agent works in development workspaces only and on workloads in scope only, and implements nothing without a plan approved by a named person. Schema changes on contract tables are additive only, and the agent never deletes. It raises conflicts with the organisation's strategy, reference documents and regulation.
  - Rule 3 protects contract tables, the tables that models, reports, downstream loads or external consumers depend on (in a medallion layout, usually the gold tables). Other objects that something refers to by name, such as items, measures and pipeline activities, may be renamed only as a step of an approved plan that covers every reference, verification and rollback. Rules 4 and 5 apply wherever Direct Lake is used. Defaults are conservative: an unrecorded table is treated as a contract table, and Direct Lake is assumed until the storage mode is recorded.
  - Setup and readiness: until setup is complete the agent works on setup only, Fabric calls during setup are read-only, each operator needs a passed connection check, and a failed check stops Fabric work.
  - A review, plan, approve, implement, document and update-context workflow, with permanent records.
- **Organisation context** in `agent_context/organisation/`: an organisation profile (sectors, regions, regulation, AI tools and data, data domains, how Fabric is used, workloads in scope, people, constraints, writing conventions), a data strategy summary, and a place for reference documents in Markdown or PDF with their summaries.
- **Environment context:** an index and seven topic files, briefs and requirements folders, output registers, and templates for reviews, plans, change records and the access request. `07_fabric_item_rules.md` holds the organisation's rules for particular item types and its code and documentation standards, such as how notebooks are laid out and how code is formatted.
- **Fabric item guides** in `agent_context/fabric_item_guides/`: general guidance for notebooks, data agents and Fabric apps, from a common template. Each guide records when it was last checked against Microsoft's documentation and whether it has been verified in a live environment. The organisation's item rules take precedence over the guides, never over `AGENTS.md`.
- **Skills**, with `.claude/skills/` as the source and a generated copy in `.github/skills/` for GitHub Copilot:
  - `fabric-setup`: agent-led setup in six organisation stages (profile, reference documents, roles and approvers, environment outline, access request, initial discovery) and two operator stages (workstation, connection check), recorded in `agent_context/setup_status.md`.
  - `fabric-summarise-reference`: summaries of the data strategy and other reference documents.
  - `fabric-assess-requirement`: read-only assessments of business requirements.
- **Identity options** for the agent, compared in the Identity section of `docs/security_and_access.md`: one service principal with a certificate per operator (option A, the default), a service principal per operator (B), a dedicated agent user account per operator (D), or a managed identity on an Azure virtual machine (E). The operator's own account (C) is not supported. Each operator sets the matching identity mode, `FABRIC_AGENT_IDENTITY`. No option uses client secrets.
- **Setup for Windows, macOS and Linux:**
  - `scripts/kit_setup.py` sets up and checks an operator workstation. It uses only the Python standard library, and its output contains no credential values.
  - It generates `.mcp.json` for the workstation's platform from `scripts/mcp_servers.json`, and pins each MCP server to the identity mode's single credential, so neither can fall back to another sign-in on the workstation. `.mcp.json` is not committed.
  - `SETUP.md` is the workstation checklist, with a path for each identity option.
- **Microsoft's EULA for the `powerbi-modeling` server is never accepted automatically.** The lead operator decides at setup, and the decision is recorded under Tooling in `01_environment_overview.md`. Each operator sets `FABRIC_AGENT_PBI_EULA` to match, and the server is configured only when it is `accepted`. The agent cannot call the server's `accept_eula` tool.
- **Permissions for Claude Code** in `.claude/settings.json`:
  - reads run freely;
  - writes, notebook jobs, Livy sessions and statements, SQL statements, renames, and removing part of an item (a semantic model table, measure or relationship, or a pipeline activity) ask the operator first;
  - deleting an item, a folder or landed data, deletes through `az rest`, force pushes, the `accept_eula` tool, and reads of credential folders are denied;
  - an `az rest` get call that names a method a second time asks, because the Azure CLI uses the last `--method` given;
  - the PowerShell tool is denied, so the agent runs commands through the Bash tool (Git Bash on Windows), which the command rules are written for.
- **GitHub Copilot in VS Code**, based on the VS Code documentation as of 25 Nov 2026:
  - The Fabric Developer custom agent in `.github/agents/`.
  - Terminal rules in `scripts/copilot_terminal_rules.json`, applied with `kit_setup.py --apply-copilot-rules`.
  - A comparison of the two tools' controls in `docs/security_and_access.md`.
- **Guides for people** in `docs/`: an overview, an operator guide, a records guide, security and access, troubleshooting, a glossary, and FAQs for data and technology leadership and for the Fabric administrator.
- **Separation of kit files and organisation files:** kit files are replaced on upgrade, and organisation files are never overwritten (see `README.md`). An upgrade is a recorded change, and each change record lists the kit files the change touched, so they can be reapplied afterwards.
- **Workflows:**
  - `check-skills` fails a pull request when the Copilot copy of the skills is out of date.
  - `check-setup` runs the setup script on Windows, macOS and Linux, once for each identity mode.
- **Line endings:** `.gitattributes` keeps LF line endings on every platform.
- **Security policy** in `SECURITY.md`: how to report a security problem in the kit.
- **MCP servers** pinned on 16 Nov 2026: `ms-fabric-mcp-server` 0.8.7 and `@microsoft/powerbi-modeling-mcp` 1.0.0. Check for newer releases; an upgrade is a new kit version.

### Known limitations and items under review

- **Identity options not all tested.** Identity mode `certificate` (options A and B) has been tested on Windows. Modes `user` (option D) and `managed-identity` (option E) have not yet been tested end to end. Microsoft Entra Agent ID is under review; Fabric documentation does not yet describe support for it.
- **Setup on macOS and Linux not yet tested by an operator.** The `check-setup` workflow runs `kit_setup.py` on all three platforms and in every identity mode, but the `SETUP.md` commands for macOS and Linux (certificate, Azure CLI profile, Copilot credentials) have not yet been followed end to end.
- **The `fabric` MCP server.** The kit uses `ms-fabric-mcp-server`, a community project published from an individual's GitHub account, marked Beta, whose README says it is for development environments only. Microsoft now publishes its own Fabric MCP server (`@microsoft/fabric-mcp`, from `github.com/microsoft/mcp`). Whether it should replace the community server is under review. A change of server changes the tool names, so the permission rules, the Copilot agent file and the item guides would change with it.
- **The `powerbi-modeling` MCP server.**
  - It has no separate delete tools, so its deletes cannot be denied by name; they ask the operator like every other call to it.
  - The pinned version 1.0.0 has no release for Intel Macs.
  - Version 1.0.1 was assessed on 27 Nov 2026 and not adopted: it removes macOS from the supported platforms, and adds permission features for semantic models that the kit has not reviewed.
- **Rules for terminal commands are not a security boundary.** In Claude Code and in GitHub Copilot, the rules for `az rest` and `git push` match the text of the command.
  - A delete or force push written in a form the rules do not name asks the operator instead of being denied.
  - `az rest --method get` runs without asking whatever host `--url` names and whatever token `--resource` attaches, and it can write its result to a local file with `--output-file`. To assess: a wrapper script or a Claude Code hook that allows only get calls to Fabric and OneLake hosts.
  - The rules for a repeated `--method` and the denial of the PowerShell tool were tested in Claude Code on Windows on 27 Nov 2026. The matching GitHub Copilot terminal rule follows the VS Code documentation of 25 Nov 2026 and has not yet been tested in a live session.
  - The agent's identity remains the first fence.
- **Fabric item guides not yet verified in a live environment.** Each guide says which statements depend on this.
- **GitHub Copilot not yet tested in a live session.** To confirm: the agent's `tools` list loads both MCP servers, with the `powerbi-modeling` server only when the EULA is accepted; the three skills appear as slash commands; the agent refuses the forbidden tools; and the terminal rules behave as documented.
- **GitHub Copilot cannot block tools.** It has no deny list, so the delete tools and the `accept_eula` tool are forbidden by instruction only. Options to assess, each needing a live Copilot session: the per-server `tools` field in `.mcp.json`, generated by `kit_setup.py`, which can hide tools from Copilot (and needs a check that Claude Code ignores it); or listing the allowed tools individually in the agent file instead of `fabric/*`, for which VS Code's documentation (25 Nov 2026) does not yet confirm the syntax.
- **GitHub Copilot credentials.** Copilot does not read `.claude/settings.local.json`, so the identity mode and credential variables must also be in the environment VS Code starts from. That affects every Azure tool started from that environment. The identity options do not change this.
- **GitHub Copilot terminal rules.** `kit_setup.py --apply-copilot-rules` adds them only when the User settings file is plain JSON; a file with comments or trailing commas must be edited by hand. For a VS Code profile other than the default, pass that profile's file with `--vscode-settings`.
