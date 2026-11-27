# Item guide: [item type]

| Field | Value |
|---|---|
| Item type in the Fabric REST API | [e.g. `Notebook`] |
| Workload row in the organisation profile | [the row in "Fabric workloads in scope" this item belongs to] |
| Status in Fabric | [Preview or Generally available, per feature where they differ, as of a date] |
| Checked against Microsoft documentation | [date] |
| Verified in a live environment | [Not yet, or date and what was verified] |

General guidance for every organisation. Organisation rules for this item type are in `../context/07_fabric_item_rules.md` and take precedence over this guide; the rules in `AGENTS.md` take precedence over both.

## What it is

[What the item does, what it is built from, and who uses it. Two or three short paragraphs.]

## Before working on it

[Prerequisites: capacity, tenant settings by their exact admin portal names, licences, other items it depends on.]

## How the agent reads it

[Which MCP tools work for this item, the `az rest` fallback, and what needs a person. Mark anything not yet verified live.]

## How the agent changes it

[How a change is made (item definition, API, portal), what can be changed as part of an approved plan, what must stay a human step, and anything that is hard to reverse.]

## Security

[Whose identity it runs under, how permissions to the underlying data apply, who can see or use it, and what a Viewer-only test principal should check (AGENTS.md rule 9).]

## Lifecycle

[Git integration, deployment pipelines, and anything that does not carry across stages.]

## Verification

[How to check a change worked, in development.]

## Known limitations and traps

- [Each with its source.]

## Sources

- [Microsoft documentation pages relied on, with the date checked.]
