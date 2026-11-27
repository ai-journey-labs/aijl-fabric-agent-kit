---
name: fabric-assess-requirement
description: Assess a business requirement held in agent_context/requirements/R#####_*/ against the Fabric environment context, and write a read-only assessment (feasibility, affected items, schema contract impact, defects, risks, open questions, proposed changes). Use when an operator asks to assess, size, triage or scope a requirement, or names an R##### ID.
---

# Assess a business requirement

An assessment turns a business requirement into a proposal an operator can accept or reject. It is read-only: it changes nothing in Fabric and allocates no change IDs. All rules in `AGENTS.md` apply.

## Inputs

- The requirement ID (`R#####`) or folder name. If the operator gives neither, list the folders in `agent_context/requirements/` with status New and ask which one.

## Steps

1. **Locate.** Open `agent_context/requirements/R#####_*/requirement.md`. If the folder or file does not exist, stop and say so.
2. **Read the context.** Read `agent_context/master_context.md`, the organisation profile, the data strategy summary and any reference summaries that cover the requirement's subject, then `03_schema_contracts.md`, `05_known_defects.md` and `06_platform_gotchas.md`, plus `01` and `02` as the requirement needs. For each item type the requirement would create or change, read its guide in `agent_context/fabric_item_guides/` and its section of `07_fabric_item_rules.md`, and note any item type that has no guide. Read `agent_output/findings_register.md` and `agent_output/change_log.md` for related findings and changes in progress.
3. **Check the current state, read-only.** Where the context is missing or may be stale, inspect development with read-only tools only: `list_workspaces`, `list_items`, `list_folders`, the `get_*_definition` tools, and `az rest --method get`. Do not create Livy sessions, run statements or start jobs during an assessment. Record each tool call you relied on.
4. **Map the requirement.** For each piece of data the requirement needs, find where it comes from (source, landing, each layer such as silver and gold, model). Mark each piece Available, Partly available or Not available.
5. **Assess.** Work through every section of [assessment_template.md](assessment_template.md). State schema impact against the schema contract in `03_schema_contracts.md`: additive only, or breaking (rule 3). Flag any conflict with a rejected approach in `05_known_defects.md`, with the data strategy or a reference document (rule 10), or with the workloads in scope in the organisation profile.
6. **Propose changes.** Split the work into the smallest independently verifiable changes, in delivery order. Give each a working title and a size (Small, Medium, Large) with the reason. Do not allocate `CHG` IDs; that happens when the operator accepts the assessment.
7. **Write.** Save the assessment as `assessment.md` in the requirement folder. Set the requirement's status to Assessed, link the assessment, and update the row in `agent_context/requirements/register.md`.
8. **Report.** Tell the operator the recommendation, the open questions that block progress and who should answer them, and the proposed changes.

## Rules

- Questions for the business go in Open questions with the person who should answer. Do not guess business definitions.
- New data or logic defects found during the assessment are listed with a proposed `DF-###` entry for the operator to confirm; do not fix them.
- If the requirement needs anything outside development or above Contributor, say so and describe the human step for the Fabric administrator.
- Follow the writing style in `AGENTS.md`.
