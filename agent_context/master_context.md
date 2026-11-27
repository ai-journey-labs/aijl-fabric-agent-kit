# Master context

Read this file at the start of every session, then `setup_status.md`, the organisation profile and data strategy summary, then the topic files relevant to the task.

## Setup

| File | Covers | Read when |
|---|---|---|
| [setup_status.md](setup_status.md) | Progress of the agent's setup for the organisation, and each operator's workstation and connection check | Every session; until organisation setup is complete, the agent works on setup only |

## Organisation

| File | Covers | Read when |
|---|---|---|
| [organisation/profile.md](organisation/profile.md) | Who the organisation is, sectors, regions, regulation, data domains, how it uses Fabric, workloads in scope, team, constraints, writing conventions | Every session |
| [organisation/data_strategy.md](organisation/data_strategy.md) | Summary of the data strategy, with references to the source document | Every session |
| [organisation/reference/index.md](organisation/reference/index.md) | Other organisation documents (policies, standards, glossaries) and their summaries | Any task a listed document covers; before proposing a new approach |

## Topic files

These describe the Fabric environment.

| File | Covers | Read when |
|---|---|---|
| [context/01_environment_overview.md](context/01_environment_overview.md) | Key facts, architecture, environments, capacity, roles and approvers, access model, tooling | Every session; before any approval check or elevated request |
| [context/02_workspace_inventory.md](context/02_workspace_inventory.md) | Capacities, workspaces, lakehouses, notebooks, pipelines, semantic models and their bindings, git status | Any task that touches a Fabric item |
| [context/03_schema_contracts.md](context/03_schema_contracts.md) | Contract tables (the schema contract), control tables, source schema contracts, contract table registry | Any task that reads or changes a table schema |
| [context/04_naming_conventions.md](context/04_naming_conventions.md) | Names for items, tables, columns, branches, change records | Creating or naming anything |
| [context/05_known_defects.md](context/05_known_defects.md) | Open architecture and platform findings (F#), remediation sequence, rejected approaches | Every review; before proposing an approach |
| [context/06_platform_gotchas.md](context/06_platform_gotchas.md) | Direct Lake, capacity, deployment, security, tenant and MCP tooling lessons | Every plan; when a tool behaves unexpectedly |
| [context/07_fabric_item_rules.md](context/07_fabric_item_rules.md) | The organisation's rules for particular item types, and its code and documentation standards | Any task that creates or changes an item or its code |

## Fabric item guides

General guidance for particular item types, supplied by the kit. The organisation's rules in `07_fabric_item_rules.md` take precedence over a guide; the rules in `AGENTS.md` take precedence over both.

| File | Covers | Read when |
|---|---|---|
| [fabric_item_guides/README.md](fabric_item_guides/README.md) | The list of guides, how to apply them, and how far each can be trusted | Any task that touches a Fabric item |
| `fabric_item_guides/<item>.md` | One item type each: what it is, prerequisites, how to read and change it, security, lifecycle, verification, traps | Any task that touches an item of that type |

## Other sources

- Task briefs: [enhancements/](enhancements/README.md) and [bug_fixes/](bug_fixes/README.md).
- Business requirements: [requirements/register.md](requirements/register.md), one folder per `R#####`.
- Change register: [../agent_output/change_log.md](../agent_output/change_log.md).
- Data and logic findings: [../agent_output/findings_register.md](../agent_output/findings_register.md).
- Item-level enumeration (every item, table and column at a point in time) lives in `agent_output/baselines/`, not in the topic files. The topic files summarise and link to the latest baseline.

## Maintenance rules

1. **One fact, one home.** Each fact lives in exactly one file. Elsewhere, link to it; do not repeat it.
2. **Date significant facts**, for example "confirmed 15 Aug 2026", so a reader can judge whether a fact is stale.
3. **Placeholders are `[TODO: ...]`.** Resolving one is a valid task in its own right; record the source of the answer.
4. **Keep files readable.** When a topic file passes about 300 lines, propose a split rather than letting it grow.
5. **Stale context is a defect.** Update these files as part of every implemented change (AGENTS.md rule 8).
6. **Organisation facts live in organisation files.** This index is a kit file and holds no facts about the organisation.
