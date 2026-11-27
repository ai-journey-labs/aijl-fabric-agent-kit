# Bug briefs

A bug brief reports something that is wrong: a failing job, an incorrect number in a report, missing data, or behaviour that differs from what was agreed.

## How to report a bug

1. Copy [_template/bug_brief.md](_template/bug_brief.md) to this folder as `YYYY-MM-DD_short_description.md`.
2. Describe what you saw and what you expected, with evidence (screenshots, the report and filter used, the job run time).
3. Commit and push, then ask the agent to review the brief.
4. The agent allocates a `CHG-###` ID, investigates read-only and writes a review record. A data or logic defect also gets a permanent `DF-###` in `agent_output/findings_register.md`; an architecture or platform defect is recorded as `F#` in `agent_context/context/05_known_defects.md`.
5. Any fix follows the normal workflow: plan, approval, implementation in development.

The change log and the findings register track status; this folder holds the briefs themselves.
