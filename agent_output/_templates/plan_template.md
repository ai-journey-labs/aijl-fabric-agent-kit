# Plan: CHG-### [short title]

| Field | Value |
|---|---|
| Change ID | CHG-### |
| Review | [link to the review record] |
| Date | [e.g. 20 Oct 2026] |
| Status | Awaiting approval |

Status becomes "Approved by [name] on [date]" only when a person marked "May approve plans" in Roles and approvers (`01_environment_overview.md`) approves it.

> **Nothing in this plan starts until the status reads Approved.**

## Objective

[What will be true when this change is complete.]

## Scope

**In scope:**
- [Item or behaviour]

**Out of scope:**
- [Item or behaviour, including anything in test or production]

## Schema contract statement

[Additive only: list each new table or column. Or: invokes rule 3, see the separate migration plan [link].]

Renames: [None. Or, for each object renamed (never a contract table or column): its old and new name, every reference to the old name and how each is updated, and how the rename is verified and rolled back (rule 3).]

## Implementation steps

All steps run in development (the workspaces marked Development in `02_workspace_inventory.md`).

| # | Action | Tool | Verification |
|---|---|---|---|
| 1 | [action] | [MCP tool, `az rest` call, or Human] | [how success is checked] |

## Human steps

[Steps the agent cannot perform, with exact instructions and who performs them. Elevated steps are a numbered command list for the Fabric administrator. Write "None" if there are none.]

## Rollback

| Step | How to reverse it | Reversible |
|---|---|---|
| 1 | [action] | Yes / No |

Any step marked "No" needs individual sign-off, recorded here: [name, date, step].

## Verification and acceptance

[How the change as a whole is shown to work, including any Viewer-only test principal checks for security changes, and the acceptance criteria from the brief.]

## Context and docs updates required on completion

- [ ] `agent_context/context/[file]`: [what changes]
- [ ] `agent_output/change_log.md`: status
- [ ] `agent_output/findings_register.md`: [DF-### IDs closed, if any]
- [ ] `docs/`: [documents made out of date, or None]
- [ ] Fabric environment repo: workspace commit [agent or human step]
