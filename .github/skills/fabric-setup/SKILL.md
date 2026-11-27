---
name: fabric-setup
description: Set the agent up for this organisation, or continue setup, by walking the operator through it stage by stage and recording progress in agent_context/setup_status.md. Covers the organisation profile, reference documents, roles and approvers, the environment outline, the access request for IT, each operator's workstation and connection check, and the initial read-only discovery. Use when an operator asks the agent to set itself up, to start or continue setup or onboarding, when a new operator joins, or when setup_status.md shows setup is not complete.
---

# Set up the agent

Walk the operator through setup one stage at a time and record progress in `agent_context/setup_status.md`. Setup changes nothing in Fabric. Every stage before the connection check writes only to this repository; the connection check and discovery make read-only calls.

## Before you start

1. Read `AGENTS.md`, `agent_context/master_context.md`, `agent_context/setup_status.md`, `agent_context/organisation/profile.md` and `agent_context/context/01_environment_overview.md`.
2. Ask the operator's name and whether they are the lead operator setting up the organisation, or an operator joining an organisation that is already set up. A joining operator does only the two operator stages (see "An operator joining" below).
3. Tell the operator which stages are complete, which comes next, and roughly what you will ask. They can stop at any point; the next session resumes from `setup_status.md`.
4. If the Setup change field in `setup_status.md` is empty, allocate the next `CHG-###` in `agent_output/change_log.md` with the title "Agent setup and initial discovery" and status Implementing, and record it in `setup_status.md`. In the same edit, fill the Kit version at setup field with the version in `KIT_VERSION`. Pull `main` first and push the allocation if several operators share the repository. No plan is needed, because setup writes only organisation files in this repository and changes nothing in Fabric; the lead operator accepts the change record at the end.

## How to run the interview

- Ask a short group of questions at a time (no more than five), with an example answer for each.
- Accept "I don't know" and "skip". Record `[TODO: ...]` with who can answer, and move on. Never invent a fact or fill a gap from general knowledge or the web.
- Record each answer in the file that owns it (one fact, one home; see `master_context.md`). Show the operator what you wrote and ask them to confirm it before you mark a stage Complete.
- After each stage, update its row in `setup_status.md`: status, date, who confirmed it and any open TODOs. Suggest the operator commits at that point.
- Never ask for, accept, write or repeat a secret: private keys, certificate files, client secrets, passwords or tokens. If the operator pastes one, tell them not to, do not record it, and suggest they treat it as exposed. Tenant IDs, client IDs and certificate thumbprints are identifiers, not secrets.
- A stage the organisation does not need can be marked "Not applicable" only by the lead operator, with the reason.

## Organisation stages

The lead operator completes these once for the organisation.

### 1. Organisation profile

Interview the operator through the sections of `agent_context/organisation/profile.md`. If they have an existing description (an annual report extract, an "about us" page, a strategy deck), they can paste it or add it to `reference/`; extract what fits and confirm it with them.

Complete when these are filled: Organisation, What the organisation does, How the organisation uses Microsoft Fabric, Fabric workloads in scope (with "Agent may work on this" for each), and Writing conventions (including the English variant). Other sections may stay `[TODO]` with a named owner.

### 2. Reference documents

1. Ask whether the organisation has a written data strategy, and any policies, standards or glossaries the agent should follow.
2. Explain how to add them, from `agent_context/organisation/reference/README.md`: Markdown or PDF, the size limit, and the confidentiality check, because they are committed to the repository.
3. For each document added, use the `fabric-summarise-reference` skill.
4. If there is no written strategy, set the status in `data_strategy.md` as that file describes.

Complete when every document listed in `reference/index.md` has a summary at Draft or later, or the operator confirms there are none. Note in `setup_status.md` which summaries are still Draft and who must confirm them.

### 3. Roles and approvers

Fill the Roles and approvers table in `01_environment_overview.md`: the lead operator, other operators, everyone who may approve plans, the Fabric administrator, and the IT contact who manages app registrations or user accounts. Record names exactly as they will appear in approvals, because AGENTS.md rule 2 matches them.

Complete when there is a lead operator, at least one person who may approve plans, and a named Fabric administrator.

### 4. Environment outline

From what the operator knows, without calling Fabric yet:

- `02_workspace_inventory.md`, Workspaces table: each workspace's name and stage (Development, Test, Production). IDs, items and bindings come at discovery.
- `01_environment_overview.md`: Environments and deployment (including the Fabric environment repo), Capacity and tenancy, an outline of the Architecture, and any Key facts the operator can state with confidence.

Then ask whether the organisation has its own rules for particular item types, or standards for code and documentation, for example how notebooks are laid out and documented and how code is formatted. Record them in `07_fabric_item_rules.md`, or add a formal standard to `organisation/reference/` and link it from there. Where there are none yet, write "None" and tell the operator the defaults in `agent_context/fabric_item_guides/` apply. This question does not hold up the stage.

Complete when the development workspaces are named. Everything else may stay `[TODO]` for discovery.

### 5. Access request

1. Ask the lead operator which identity option the organisation will use: A, B, D or E. Point them to the Identity section of `docs/security_and_access.md`, and recommend option A unless they have a reason for another. Option C is not supported; if they ask for it, explain why from that section. Record the option and its identity mode in the Access model of `01_environment_overview.md`.
2. Write the request from `agent_output/_templates/access_request_template.md` as `agent_output/recommendations/REC_YYYY-MM-DD_access_request.md`, addressed to the Fabric administrator and IT contact from stage 3. Keep the identity requests for the chosen option only. List the development workspaces from stage 4 and nothing else, and, for options B, D and E, the operators from stage 3.
3. Ask the lead operator to decide whether the organisation accepts Microsoft's EULA for the `powerbi-modeling` server (the Power BI Authoring MCP server), at https://go.microsoft.com/fwlink/?LinkId=2381247. Do not accept it for them, and never call the server's `accept_eula` tool. Suggest they read it, and check with whoever approves software licences if the organisation's policy requires that. Record the decision under Tooling in `01_environment_overview.md`: accepted, by whom and on what date, or declined. If declined, the agent works without that server: semantic model changes go through `az rest` or a person, and request 3 in the access request (XMLA read-write) can be removed.
4. Ask the lead operator to review the access request and send it. Record the date sent in `setup_status.md` and set the stage to In progress.
5. When IT and the Fabric administrator confirm, record the identifiers they return in the Access model (tenant ID, and each identity's name and client ID or account name; never a key, password or secret), and set the stage to Complete. The stage cannot be complete until the EULA decision is recorded.

Workstation setup can start while the request is in progress, but the connection check cannot pass until access is granted.

### 6. Initial discovery

Needs a passed connection check by the lead operator (see the operator stages). All calls are read-only.

1. For each development workspace, list its items and folders. For each semantic model, read its definition: storage mode, what it is bound to, tables and RLS roles. Read notebook and pipeline definitions only far enough to record their purpose, what they read and write, and their schedule. Note each item type in use that has no guide in `agent_context/fabric_item_guides/`.
2. Do not create Livy sessions or run jobs: they consume capacity. Where a fact needs one (for example, a table's columns), record `[TODO]` and suggest a later review.
3. Write the full enumeration as `agent_output/baselines/YYYY-MM-DD_baseline_development.md`. Summarise it in `02_workspace_inventory.md` with IDs and a link to the baseline, and add what you can confirm to the Key facts and Architecture in `01_environment_overview.md`, dated.
4. Where what you find differs from what the operator said at stage 4, show the difference and ask. Do not silently correct either side.
5. Do not fix anything. Defects you notice are listed in the change record's follow-ups as proposed findings for the lead operator to confirm (`DF-###` or `F#`), in line with AGENTS.md rule 7.

Test and production workspaces are not visible to the agent; leave them as the operator described them.

## Operator stages

Each operator completes these on their own workstation. Record them in the Operators table of `setup_status.md`. The operator must already be listed in Roles and approvers.

### Workstation

1. Tell the operator the identity option and mode from the Access model, and the EULA decision for the `powerbi-modeling` server from Tooling in `01_environment_overview.md`. They follow `SETUP.md` steps 5 to 8 for that option (credential, access, local settings with `FABRIC_AGENT_IDENTITY` and `FABRIC_AGENT_PBI_EULA`, and the project Azure CLI profile), and step 9.1 if they use GitHub Copilot. For option E, all of this happens on the virtual machine. Steps 5 and 6 wait on the access request for the first operator.
2. Ask them to run `python scripts/kit_setup.py --check` in their own terminal (`python3` on macOS and Linux; add `--copilot` for GitHub Copilot) and paste the output. Do not run the script yourself, and never open `.claude/settings.local.json` or the key and Azure CLI profile folders.
3. Help with each FAIL or TODO line, using `SETUP.md` and `docs/troubleshooting.md`.

Complete when the output says "Result: ready." and reports the identity mode recorded in the Access model. It must also report the EULA decision recorded in `01`. If it reports a different mode or decision, the operator corrects `FABRIC_AGENT_IDENTITY` or `FABRIC_AGENT_PBI_EULA` first. Record the agent (Claude Code or GitHub Copilot), the platform from the first line of the output, the identity mode, and the date.

### Connection check

The operator must have fully restarted VS Code since their last change to local settings (`SETUP.md` step 9).

1. Ask the operator to confirm both MCP servers are connected, or only the `fabric` server if the EULA was declined (`/mcp` in Claude Code; MCP: List Servers in VS Code for Copilot).
2. Call `list_workspaces`. The result must show exactly the workspaces marked Development in `02_workspace_inventory.md`.
   - If it shows a test or production workspace, or any workspace not in the inventory, stop. Tell the lead operator that the agent's identity has more access than the access model allows. Record it in the Operators table as Failed, and make no further Fabric calls until the lead operator confirms access has been corrected.
   - If a development workspace is missing, access is not complete yet. Record it and follow up through the access request.
3. Run `az rest --method get --url https://api.fabric.microsoft.com/v1/workspaces --resource https://api.fabric.microsoft.com`. In Claude Code it should run without a permission prompt. Its result must match step 2.
4. Check the `powerbi-modeling` server's identity, which `list_workspaces` does not cover. It asks permission before each connection. Read only.
   - Connect it to a semantic model in a development workspace. It must connect. For option D, the operator chooses their agent account in the sign-in window that opens, never their personal account.
   - Try to connect it to a test or production workspace from `02_workspace_inventory.md`. It must be refused. If it connects, treat it as a failed check, as in step 2: stop, disconnect, and tell the lead operator.
   - If the EULA was declined, record this part as Not applicable.
   - If there is no development semantic model yet, or no test or production workspace is recorded, record this part as Not possible and repeat it once one exists.

Record the date, the number of workspaces seen, the result of the `powerbi-modeling` check, and Passed or Failed. The lead operator's first check also goes in the setup change record's verification results, listing the workspace names seen.

## Finishing setup

When stages 1 to 6 are Complete or Not applicable:

1. Complete the change record for the setup change in `agent_output/change_records/`, from the template. Steps are the stages, with who confirmed each. Verification is the lead operator's connection check and a link to the discovery baseline. Follow-ups are open TODOs, Draft summaries awaiting confirmation and proposed findings.
2. Set the change to Implemented in `change_log.md`, and set "Organisation setup complete" in `setup_status.md` to Yes, with the date.
3. Ask the lead operator to review the change record and close the change.
4. Tell the operator what comes next: give work as a brief in `agent_context/enhancements/` or `agent_context/bug_fixes/`, or as a requirement in `agent_context/requirements/` (see `docs/operator_guide.md`).

## An operator joining

1. Check that the person is listed in Roles and approvers. If not, the lead operator adds them first (stage 3).
2. Run the two operator stages, and add their row to the Operators table.
3. No change ID is needed. If their connection check fails, follow the stop rule above.
