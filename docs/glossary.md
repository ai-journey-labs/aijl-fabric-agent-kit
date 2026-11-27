# Glossary

Terms used across the repository. Terms the organisation uses with a specific business meaning are in Business terms in `agent_context/organisation/profile.md`.

## Fabric and Power BI terms

| Term | Meaning |
|---|---|
| Capacity | The pool of compute a Fabric tenant buys (an F SKU) and assigns to workspaces. Notebook runs, Spark sessions, queries and refreshes all consume it |
| Contributor | A workspace role that can create, edit, run and delete items, but cannot manage access to the workspace, connect it to git or delete it. The agent's identity holds this role on the development workspaces only |
| Data agent | A Fabric item that answers questions in natural language by querying the data sources it is given. See `agent_context/fabric_item_guides/data_agent.md` |
| Delta table | The table format Fabric lakehouses use, stored in OneLake with a transaction log |
| Deployment pipeline | Fabric's way of promoting items from one stage (development, test, production) to the next. The agent never deploys beyond development |
| Direct Lake | A semantic model storage mode that reads Delta tables in OneLake directly. Rules 4 and 5 in `AGENTS.md` protect it |
| DirectQuery, Import | Other semantic model storage modes: DirectQuery sends each query to the source; Import loads a copy of the data into the model |
| Fabric app | A Fabric item (`AppBackend`) for building and hosting data-driven web applications. Not the same as an org app or a workspace app. See `agent_context/fabric_item_guides/fabric_app.md` |
| Item | Anything inside a workspace: a lakehouse, notebook, pipeline, semantic model, report and so on |
| Item definition | The source of an item (for example a notebook's code and metadata), read and written through the Fabric APIs and stored in workspace git |
| Lakehouse | A Fabric item that stores files and Delta tables in OneLake, with an SQL analytics endpoint for reading the tables |
| Livy | The API for running Spark code in a session outside a notebook. The agent's Livy calls ask the operator, because they use capacity and can run any code |
| Managed identity | An identity Azure manages for a resource such as a virtual machine, with no credential to hold. Identity option E |
| Materialized Lake View | A Fabric construct that stores the result of a query as a table. The only view-like construct allowed under Direct Lake (rule 4) |
| Medallion layout | A common way of arranging data in layers: bronze (raw), silver (cleaned) and gold (ready for reporting) |
| Microsoft Entra ID | Microsoft's identity service, where users, service principals and security groups are managed |
| Notebook | A Fabric item holding code and text cells, run on Spark or a Python runtime. See `agent_context/fabric_item_guides/notebook.md` |
| OneLake | The single data lake behind every Fabric tenant, where lakehouse files and tables are stored |
| OneLake security | Data access roles that restrict what Viewers can read in a lakehouse. They do not apply to Admin, Member or Contributor |
| Pipeline | A Fabric item that orchestrates activities, such as copying data and running notebooks |
| RLS (row-level security) | Rules in a semantic model that limit which rows a user can see. They apply to Viewers only, not to Admin, Member or Contributor |
| Semantic model | The model reports read from: tables, relationships, measures and security. Formerly called a dataset |
| Service principal | An identity for an application rather than a person, created as an app registration in Microsoft Entra ID. Identity options A and B |
| SQL analytics endpoint | The read-only SQL interface over a lakehouse's tables |
| Tenant setting | A setting the Fabric administrator controls for the whole organisation, such as whether service principals can call Fabric APIs |
| Viewer | The workspace role that can only read. The role a security test principal holds |
| Warehouse | A Fabric item that stores tables and is read and written with T-SQL |
| Workspace | A container for items, with its own access and capacity. Each is marked Development, Test or Production in `02_workspace_inventory.md` |
| Workspace git integration | Connecting a workspace to a git repository so item definitions can be committed and updated. Connecting needs the Admin role |
| XMLA endpoint | The interface tools use to read and change semantic models. Read-write access is set on the capacity |

## Project terms

| Term | Meaning |
|---|---|
| Access model | The record of the organisation's identity option, identities and workspace role, in `01_environment_overview.md` |
| Access request | The request to IT and the Fabric administrator for the agent's identity and access, written by the agent during setup |
| Agent | The AI agent configured by the kit, running in Claude Code or GitHub Copilot, acting as a supervised senior Fabric developer |
| Approver | A person marked "May approve plans" in Roles and approvers. Only approvers and the lead operator can approve plans |
| Baseline | A point-in-time list of every item, table and column in scope, in `agent_output/baselines/` |
| Brief | A request for work: an enhancement brief (something new or improved) or a bug brief (something wrong) |
| Connection check | The check, run for each operator, that the agent's identity sees exactly the development workspaces and nothing else |
| Context | The files in `agent_context/` that describe the organisation and its Fabric environment, which the agent reads before proposing anything |
| Contract table | A table that semantic models, reports, downstream loads or external consumers depend on. Never renamed, retyped or dropped without a migration plan (rule 3). Listed in `03_schema_contracts.md` |
| Control table | A table that drives loads, such as watermarks, run logs and configuration |
| Fence | A layer that keeps the agent inside its scope. The first fence is its identity; the second is its tool permissions |
| Fabric environment repo | The organisation's own git repository holding its Fabric item definitions, separate from this repository |
| Human step | A step in a plan that a person must carry out, written as exact instructions |
| Identity mode | The setting each operator makes for the organisation's identity option: `certificate` (A, B), `user` (D) or `managed-identity` (E) |
| Identity option | How the agent signs in: A, B, D or E (C, the operator's own account, is not supported). Compared in `security_and_access.md` |
| Item guide | The kit's general guidance for a Fabric item type, in `agent_context/fabric_item_guides/` |
| Item rules | The organisation's own rules for item types, and its code and documentation standards, in `07_fabric_item_rules.md` |
| Key facts | Facts already established about the environment, at the top of `01_environment_overview.md`. The agent does not re-derive them |
| Kit file | A file supplied by the kit and replaced when the kit is upgraded. Holds no facts about the organisation |
| Lead operator | The operator who sets the agent up for the organisation, can approve plans, and is accountable for its use |
| MCP server | A program that gives the agent tools, here for Fabric (`fabric`) and semantic models (`powerbi-modeling`). MCP is the Model Context Protocol |
| Migration plan | A separate plan, with explicit sign-off, for a breaking change to a contract table |
| Operator | A member of the data team who runs the agent in their own sessions |
| Organisation file | A file holding the organisation's own content. The kit supplies a starting version and never overwrites it |
| Plan | The numbered steps of a change, with schema impact, rollback and verification, that must be approved before anything is implemented |
| Reference document | An organisation document the agent must follow, such as the data strategy or a policy, held in `agent_context/organisation/reference/` with its summary |
| Review | The agent's read-only analysis of a brief: what exists, what the change touches, risks and open questions |
| Skill | A packaged procedure the agent follows, such as setup or requirement assessment, in `.claude/skills/` |
| Topic file | One of the numbered files in `agent_context/context/` that describe the environment |
| Viewer-only test principal | A separate identity holding only the Viewer role, used to check what a reader can see (rule 9) |

## Record IDs

| ID | Meaning | Where |
|---|---|---|
| `CHG-###` | A change, from review to close | `agent_output/change_log.md` |
| `DF-###` | A data or logic defect | `agent_output/findings_register.md` |
| `F#` | An architecture or platform defect | `agent_context/context/05_known_defects.md` |
| `R#####` | A business requirement | `agent_context/requirements/register.md` |
| `REC_YYYY-MM-DD` | A recommendation for a person, without a change ID | `agent_output/recommendations/` |

How IDs are allocated is described in [records_guide.md](records_guide.md).
