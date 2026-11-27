# 04 Naming conventions

Last reviewed: [TODO: date]

Follow existing names when they conflict with this file, and record the conflict as a finding rather than renaming (renames on contract tables are not allowed, see [03_schema_contracts.md](03_schema_contracts.md)).

## Items

[TODO: patterns for workspaces, lakehouses, notebooks, pipelines, semantic models and reports, with examples.]

## Tables

[TODO: layer prefixes or schemas, singular or plural, fact and dimension naming, control table naming.]

## Columns

[TODO: case convention, key and surrogate key suffixes, date and timestamp naming, audit columns.]

## Branches

[TODO: branch naming in the Fabric environment repo and in this repo, e.g. a branch per change named after its CHG-### ID.]

## Change records

- Change IDs: `CHG-###`, sequential, never reused, allocated in `agent_output/change_log.md`.
- Review, plan and change record files: `CHG-###_short_description.md`, in `agent_output/reviews/`, `agent_output/plans/` and `agent_output/change_records/`.
- Recommendations without a change ID: `REC_YYYY-MM-DD_short_description.md`, in `agent_output/recommendations/`.
- Data and logic findings: `DF-###` in `agent_output/findings_register.md`.
- Architecture and platform findings: `F#` in [05_known_defects.md](05_known_defects.md).
- Requirements: `R#####`, allocated in `agent_context/requirements/register.md`, one folder each in `agent_context/requirements/`.
- `short_description` is lower case words joined by underscores, at most about six words.
