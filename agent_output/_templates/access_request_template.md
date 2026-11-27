# Access request: Fabric agent

| Field | Value |
|---|---|
| Date | [date] |
| To | [Fabric administrator], [IT contact] (Roles and approvers in `01_environment_overview.md`) |
| From | [lead operator] |
| Setup change | [CHG-###] |
| Status | Draft / Sent [date] / Confirmed [date] |

> Identity option: [A, B, D or E] (from the Access model in `01_environment_overview.md`; options are compared in the Identity section of `docs/security_and_access.md`). Keep the identity requests for that option only, and delete the others.

## Purpose

[One paragraph for a reader outside the data team: the organisation is setting up an AI agent that acts as a supervised Microsoft Fabric developer. It works only in the development workspaces listed below, implements nothing without a plan approved by a named person, and records everything it does. This request asks for the identity it works under.]

## Requests

### Identity requests: keep the set for the chosen option

**Option A: one service principal, one certificate per operator**

| # | Request | Why | Performed by |
|---|---|---|---|
| I1 | Create an app registration and service principal for the agent, named `[sp-name]`, single-tenant, with no API permissions. Certificate authentication only: no client secret. | The agent's own identity, separate from any person | IT |
| I2 | Upload each operator's public certificate to the app registration, and confirm the thumbprint with the operator. Certificates are sent separately, one per operator. | Each operator signs in as the service principal with their own certificate; the Entra sign-in logs tell them apart by certificate | IT |

**Option B: one service principal per operator**

| # | Request | Why | Performed by |
|---|---|---|---|
| I1 | For each operator listed below, create an app registration and service principal named `[sp-name]-[initials]`, single-tenant, with no API permissions. Certificate authentication only: no client secret. | Each operator's activity is recorded under their own identity | IT |
| I2 | Upload each operator's public certificate to their own app registration, and confirm the thumbprint with the operator. | Each operator signs in with their own certificate | IT |

**Option D: a dedicated agent user account for each operator**

| # | Request | Why | Performed by |
|---|---|---|---|
| I1 | For each operator listed below, create a cloud-only user account for the agent, named `[agent-account-name]`, separate from the operator's personal account. Never shared between operators. | Service principal limitations (see `06_platform_gotchas.md`) rule out options A and B; one account per operator keeps activity attributable | IT |
| I2 | Give each agent account the Fabric or Power BI licence it needs to hold the Contributor role on the development workspaces below. | Without a licence, the account cannot work in the workspaces | IT |
| I3 | Apply the organisation's sign-in controls to the agent accounts: multifactor authentication registered on the operator's own device, and any Conditional Access policy. No mailbox or other services are needed. | A non-personal account needs the same protection as a personal one | IT |

**Option E: managed identity on an Azure virtual machine**

| # | Request | Why | Performed by |
|---|---|---|---|
| I1 | Create an Azure virtual machine for the agent, `[vm-name]`, with a system-assigned managed identity. | The agent works on this machine; its managed identity is the agent's identity, with no credential to hold | IT |
| I2 | Allow only the operators listed below to sign in to the machine, each with their own account. | Every process on the machine can use its identity, so sign-in to the machine decides who can act as the agent | IT |
| I3 | Install on the machine the tools in `SETUP.md` step 1. | Operators work on the machine rather than their own workstations | IT |

### Requests for every option

"Agent identities" means the identities from the identity requests above.

| # | Request | Why | Performed by |
|---|---|---|---|
| 1 | Add the agent identities to a security group, `[group-name]`. For options A, B and E, include that group in the tenant setting that lets service principals call Fabric public APIs, and limit that setting to specific security groups. | Without this, a service principal or managed identity cannot reach Fabric | IT and Fabric administrator |
| 2 | Give the security group the Contributor role on each development workspace below, and no role on any other workspace. | This is the agent's first fence: Fabric refuses anything outside these workspaces | Fabric administrator or workspace admin |
| 3 | [Optional] Set the XMLA endpoint to Read Write on the development capacity. | Needed only if the agent is to change semantic models | Fabric administrator |
| 4 | [Optional] Create a Viewer-only test principal for the development workspaces. | Security checks must not rely on the agent's own access (AGENTS.md rule 9) | IT and Fabric administrator |

### Operators

From Roles and approvers in `01_environment_overview.md`.

| Operator | Certificate thumbprint (options A, B) |
|---|---|
| [name] | [thumbprint, sent separately] |

## Development workspaces

From `02_workspace_inventory.md`.

| Workspace | Capacity |
|---|---|
| [name] | [capacity] |

## What the agent will not have

- No role on any test or production workspace.
- No tenant, capacity or workspace administration rights.
- No client secret. For options A and B, each operator's private key stays on that operator's workstation and is never shared or committed.

## Please return to the lead operator

- The tenant ID and, for each agent identity, its name and client ID (options A, B and E) or account name (option D). These are identifiers, not secrets.
- Confirmation of each request above, with the date it was done.
- Options A and B: the thumbprint of each certificate uploaded. Option E: the name of the virtual machine.

The lead operator records these in the Access model in `01_environment_overview.md`. Any output that contains tenant detail goes in `agent_output/it_returns/` or `agent_output/admin_returns/`, which are not committed.
