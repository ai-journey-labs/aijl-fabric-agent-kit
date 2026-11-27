# Enhancement briefs

An enhancement brief asks the agent to add or improve something in the development environment: a new table, column, measure, notebook or pipeline, or a change to how existing logic works.

## How to give an enhancement

1. Copy [_template/enhancement_brief.md](_template/enhancement_brief.md) to this folder as `YYYY-MM-DD_short_description.md`.
2. Fill in every section you can. Write "Unknown" rather than leaving a section blank.
3. Commit and push, then ask the agent to review the brief.
4. The agent allocates a `CHG-###` ID in `agent_output/change_log.md`, records the ID at the top of the brief, and writes a review record, then a plan for approval.

The change log is the register of briefs and their status; this folder holds the briefs themselves.

A brief that comes from a business requirement links to its `R#####` folder in [../requirements/](../requirements/README.md).
