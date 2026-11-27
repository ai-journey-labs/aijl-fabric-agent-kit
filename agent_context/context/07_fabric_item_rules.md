# 07 Fabric item rules

Last reviewed: [TODO: date]

The organisation's own rules for particular Fabric item types, and its standards for code and documentation. The kit's general guidance for each item type is in [../fabric_item_guides/](../fabric_item_guides/README.md).

The rules here take precedence over a guide, but never over the rules in `AGENTS.md`. Where a rule here relaxes something a guide advises, the agent follows the rule here and says so in the review.

How to fill this file:

- Write "None" in a section when the organisation has no rule; the guide then applies. Do not delete a section.
- Where a rule already exists in a formal document (a coding standard, an AI policy), add the document to `../organisation/reference/` and link its summary here instead of repeating it (one fact, one home).
- Date each rule and record who set it, so a reader can judge whether it is current.

## Code and documentation standards (all items)

These apply to code in any item: notebooks, Spark job definitions, user data functions, warehouse and SQL database scripts, semantic models, dataflows and KQL.

### Languages and formatting

| Language | Standard | How it is checked | Set by and date |
|---|---|---|---|
| Python and PySpark | [TODO: e.g. PEP 8, line length 120, formatted as `ruff format` would format it] | [TODO: e.g. reviewer, `ruff` in the Fabric environment repo's pipeline, none] | [TODO] |
| Spark SQL | [TODO: e.g. keywords in upper case, one column per line in SELECT] | [TODO] | [TODO] |
| T-SQL | [TODO] | [TODO] | [TODO] |
| DAX | [TODO: e.g. as formatted by DAX Formatter] | [TODO] | [TODO] |
| Power Query M | [TODO] | [TODO] | [TODO] |
| KQL | [TODO] | [TODO] | [TODO] |

### Comments and documentation

- What every item must record about itself (purpose, owner, inputs, outputs): [TODO: or "Use the kit default in each guide"]
- Comment style, and what comments must explain: [TODO: e.g. explain why, not what; business rules referenced to their source]
- Language of comments and documentation: [TODO: e.g. the English variant set in the organisation profile]
- Where longer documentation lives: [TODO: e.g. in the item, in `docs/processes/`, in a wiki]

## Notebooks

Guide: [../fabric_item_guides/notebook.md](../fabric_item_guides/notebook.md)

- Notebook structure (header cell, sections, order of cells): [TODO: or "Use the kit default"]
- Parameters: [TODO: e.g. one parameter cell, directly after the header, every parameter with a comment]
- Shared code: [TODO: e.g. a shared library notebook called with `%run`, Python files in an environment, or no shared code]
- Default lakehouse and environment: [TODO: e.g. every notebook names its default lakehouse; one environment per workspace]
- Logging and error handling: [TODO: e.g. log row counts per step to a control table; fail on unexpected schema]
- Anything the agent must not do in a notebook: [TODO: or None]

## Data agents

Guide: [../fabric_item_guides/data_agent.md](../fabric_item_guides/data_agent.md)

- Data sources an agent may use: [TODO: e.g. contract tables only, never landing or bronze]
- Standards for agent and data source instructions: [TODO]
- Who reviews example questions and answers before publishing: [TODO]
- Who may publish a data agent (the guide's default: a person, not the agent), and who it is shared with: [TODO]
- Where published agents may be consumed: [TODO: e.g. Microsoft 365 Copilot, Copilot Studio, Foundry, none outside Fabric]

## Fabric apps

Guide: [../fabric_item_guides/fabric_app.md](../fabric_item_guides/fabric_app.md)

- Whether the organisation uses them, and for what: [TODO]
- Who may build, approve and deploy them (the guide's default: a person deploys, not the agent): [TODO]
- Connector authentication (application or delegated): [TODO: e.g. delegated only]
- Whether public (anonymous) apps are allowed: [TODO: e.g. never]
- Audience and sharing rules: [TODO]

## Other item types

Rules for item types without their own section. Add a section above when an item type gathers more than two or three rules.

| Item type | Rule | Set by and date |
|---|---|---|
| [TODO] | [TODO] | [TODO] |
