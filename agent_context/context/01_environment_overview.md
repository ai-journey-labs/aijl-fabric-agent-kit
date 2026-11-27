# 01 Environment overview

Last reviewed: [TODO: date]

## Key facts

Facts already established about this environment. The agent does not re-derive them. Each links to its home for detail.

- Semantic model storage mode: [TODO: Direct Lake, Import, DirectQuery or a mix, by model; e.g. Direct Lake on OneLake for all models]. Until this is recorded, the agent assumes Direct Lake (AGENTS.md rules 4 and 5). Detail in [02_workspace_inventory.md](02_workspace_inventory.md).
- Data layout: [TODO: medallion (lakehouse per layer, where gold lives) or another layout; where the contract tables live]. Detail in Architecture below.
- Source systems and how they land: [TODO]. Detail in [03_schema_contracts.md](03_schema_contracts.md).
- Most important open defects: [TODO: top F# and DF-### IDs]. Detail in [05_known_defects.md](05_known_defects.md) and [findings_register.md](../../agent_output/findings_register.md).
- Notebook parameterisation state: [TODO]. Detail in [02_workspace_inventory.md](02_workspace_inventory.md).

The organisation itself (what it does, sectors, regulation, how it uses Fabric and which workloads are in scope) is described in [../organisation/profile.md](../organisation/profile.md). This file covers the technical environment only.

## Architecture

[TODO: the data layout (for example a medallion layout of bronze, silver and gold), which lakehouse or warehouse holds each layer, and how data flows from source systems to semantic models and reports. Item names belong in [02_workspace_inventory.md](02_workspace_inventory.md).]

## Environments and deployment

The agent works in the development workspaces only. They are marked Development in the Workspaces table of [02_workspace_inventory.md](02_workspace_inventory.md). Promotion to test and production is a human step.

- Development: [TODO: workspace names]
- Test: [TODO: workspace names]
- Production: [TODO: workspace names]
- Promotion method: [TODO: deployment pipelines, git branches, or manual; who performs it]
- Fabric environment repo: [TODO: URL, default branch, which workspaces are connected]

## Capacity and tenancy

- Tenant: [TODO: tenant name and ID]
- Capacity: [TODO: SKU, region, which workspaces sit on it]
- Capacity administrator: [TODO]
- Known constraints: [TODO: throttling history, smoothing, peak periods to avoid]

## Roles and approvers

Only people marked "Yes" in the last column may approve plans (AGENTS.md rule 2). The Fabric administrator receives every request that needs more than the agent's own access.

| Person | Role | May approve plans | Since |
|---|---|---|---|
| [TODO: name] | Lead operator | Yes | [TODO: date] |
| [TODO: name] | Fabric administrator | [TODO] | [TODO: date] |

Role values: Lead operator, Operator, Fabric administrator, IT contact, Business owner.

## Access model

Identifiers only: never a key, password or secret. Options are compared in the Identity section of `docs/security_and_access.md`.

- Identity option: [TODO: A, B, D or E; option A unless decided otherwise]
- Identity mode: [TODO: `certificate` (A, B), `user` (D) or `managed-identity` (E)]
- Tenant ID: [TODO]
- Workspace role: Contributor on the development workspaces only, and no role on any test or production workspace. Confirmed: [TODO: date and by whom]
- Security group used in the Fabric tenant setting: [TODO: name]

### Identities

One row per identity the agent signs in as. Option A has one row; options B and D have one row per operator; option E has one row per virtual machine.

| Identity | Type | Client ID or account | Operator | Credential | Expires | Since |
|---|---|---|---|---|---|---|
| [TODO: name] | [TODO: service principal, agent user account, managed identity] | [TODO] | [TODO: operator name, or all operators] | [TODO: certificate thumbprint (A, B); none recorded (D, E)] | [TODO: certificate expiry (A, B)] | [TODO: date] |

For option E, also record the virtual machine's name and who may sign in to it: [TODO].

### Viewer-only test principal

Status: [TODO: not requested, requested on date, or available since date]. Used to verify OneLake security and RLS (AGENTS.md rule 9).

## Tooling

| Tool | Version | Purpose |
|---|---|---|
| `fabric` MCP server (`ms-fabric-mcp-server`) | As pinned in `scripts/mcp_servers.json` | Workspaces, items, notebooks, pipelines, jobs, Livy sessions |
| `powerbi-modeling` MCP server (`@microsoft/powerbi-modeling-mcp`) | As pinned in `scripts/mcp_servers.json` | Semantic model inspection and changes |
| Azure CLI (`az rest`) | [TODO] | Fabric REST fallback on the project profile |

Pinned versions and the date they were pinned are recorded in `KIT_CHANGELOG.md`.

- Microsoft's EULA for the `powerbi-modeling` server (https://go.microsoft.com/fwlink/?LinkId=2381247): [TODO: accepted by the lead operator, name and date; or declined]. Decided at setup stage 5; each operator sets `FABRIC_AGENT_PBI_EULA` to match (`SETUP.md` step 7).
