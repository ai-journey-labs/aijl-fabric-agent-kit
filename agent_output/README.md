# Agent output

Everything the agent produces lives here. Records are permanent: they are corrected by dated notes, not rewritten.

| Path | Contents | Named |
|---|---|---|
| `change_log.md` | Register of every change and its status | |
| `findings_register.md` | Register of data and logic findings (`DF-###`) and their status | |
| `reviews/` | Review records (workflow step 1) | `CHG-###_short_description.md` |
| `plans/` | Plans awaiting or holding approval (step 2) | `CHG-###_short_description.md` |
| `change_records/` | What was done, deviations, verification (step 4) | `CHG-###_short_description.md` |
| `recommendations/` | Advice without a change ID, such as a deletion for a human to perform | `REC_YYYY-MM-DD_short_description.md` |
| `baselines/` | Point-in-time enumerations of items, tables and columns | `YYYY-MM-DD_baseline_scope.md` |
| `_templates/` | Templates for reviews, plans, change records and the access request | |
| `admin_returns/` | Output returned by the Fabric administrator from human steps (git-ignored) | |
| `it_returns/` | Output returned by the organisation's IT team (git-ignored) | |
| `business_sme_returns/` | Answers from business subject matter experts (git-ignored) | |

The three returns folders are git-ignored because they can contain tenant detail or business data. The agent summarises what it needs from them in the relevant record, without copying sensitive values.

## Lifecycle of a change

1. Allocate the next `CHG-###` in `change_log.md` (pull `main` first, push the allocation before starting).
2. Review record in `reviews/`.
3. Plan in `plans/`, status "Awaiting approval" until approved by a named approver.
4. Implementation in development.
5. Change record in `change_records/`.
6. Context update, change log status set to Implemented, then Closed once the lead operator accepts it.
