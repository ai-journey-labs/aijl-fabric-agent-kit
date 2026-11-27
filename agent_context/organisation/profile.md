# Organisation profile

Last reviewed: [TODO: date] by [TODO: name]

This profile tells the agent who it works for. It shapes every review, plan and recommendation: what matters to the business, which regulations apply, which Fabric workloads are in scope and how documents should be written. Write in plain language; a short accurate answer is better than a long one. Write "Not applicable" rather than deleting a section.

## Organisation

| Field | Value |
|---|---|
| Legal name | [TODO] |
| Name used in documents | [TODO: e.g. a short name or abbreviation] |
| Type | [TODO: listed company, private company, public sector body, charity, partnership, other] |
| Headquarters | [TODO: city, country] |
| Size | [TODO: approximate number of employees, and revenue or budget band if useful] |
| Website | [TODO] |

## What the organisation does

[TODO: two or three paragraphs. What the organisation provides, to whom, and how it makes money or delivers its mission. Mention the parts of the business that depend most on data.]

## Sectors and markets

| Sector or market | Importance | Notes |
|---|---|---|
| [TODO: e.g. retail banking, healthcare, manufacturing] | [TODO: primary, secondary, minor] | [TODO] |

## Regions and operating countries

[TODO: where the organisation operates, and where its data and users are. Note any country whose rules affect where data may be stored or processed.]

## Regulation and compliance

| Regulation, standard or obligation | Applies to | Effect on data work |
|---|---|---|
| [TODO: e.g. UK GDPR, sector regulator rules, ISO 27001, internal audit requirements] | [TODO: which data or processes] | [TODO: e.g. personal data must stay in the UK region; finance data needs dual sign-off] |

- Data classification scheme: [TODO: name, or link to it in `reference/`; or None]
- Data residency requirements: [TODO: e.g. tenant and capacity regions allowed]
- Personal or sensitive data in Fabric: [TODO: yes or no, which domains]
- AI tools and data: [TODO: which AI tool the agent runs in (Claude Code, GitHub Copilot or both), which AI provider and agreement that uses, who approved it, and whether the development workspaces hold real personal or confidential data or masked or synthetic copies]

## Data domains and key business processes

| Domain or process | Business owner | Key source systems | Notes |
|---|---|---|---|
| [TODO: e.g. sales, finance, customers, supply chain] | [TODO: name or role] | [TODO] | [TODO] |

## How the organisation uses Microsoft Fabric

Why the organisation has Fabric and what it expects from it. This is vital context: the agent weighs every proposal against these purposes.

| Purpose or use case | Who benefits | Outcome expected | Status |
|---|---|---|---|
| [TODO: e.g. monthly management reporting, self-service analytics, regulatory returns, forecasting] | [TODO: teams or roles] | [TODO: decision or result it supports] | [TODO: live, in build, planned] |

- Started using Fabric: [TODO: date]
- Platforms Fabric replaces or works alongside: [TODO: e.g. on-premises SQL Server, Azure Synapse, Databricks, Excel reporting]
- Main pain points the organisation wants solved: [TODO]

## Fabric workloads in scope

The agent works only on workloads marked "Yes" in the last column (AGENTS.md rule 1). For a workload marked "No", it may read and describe items but proposes changes only as recommendations for a person.

| Workload | In use | Agent may work on this | Notes |
|---|---|---|---|
| Lakehouse and notebooks (Data Engineering) | [TODO] | [TODO] | |
| Pipelines and Dataflows Gen2 (Data Factory) | [TODO] | [TODO] | |
| Warehouse | [TODO] | [TODO] | |
| Semantic models and reports (Power BI) | [TODO] | [TODO] | |
| Real-Time Intelligence (eventhouses, eventstreams) | [TODO] | [TODO] | |
| Data Science (experiments, ML models) | [TODO] | [TODO] | |
| SQL database | [TODO] | [TODO] | |
| Mirroring | [TODO] | [TODO] | |
| Data agents | [TODO] | [TODO] | |
| Fabric apps | [TODO] | [TODO] | |
| Other: [TODO] | [TODO] | [TODO] | |

Kit note: the kit's rules and platform gotchas cover lakehouses, notebooks, pipelines and semantic models most fully, and `agent_context/fabric_item_guides/` has guides for particular item types. For an item type without a guide, the agent says in each review that kit guidance is limited.

## Data and analytics team

- Team size and roles: [TODO: e.g. one data engineer, two report developers]
- Skills the team is comfortable maintaining: [TODO: e.g. PySpark, T-SQL, DAX, Power Query]
- Who supports the platform out of hours: [TODO: or None]

The agent prefers solutions the team can maintain without it.

## Stakeholders

| Name or role | Interest | How they want to be kept informed |
|---|---|---|
| [TODO] | [TODO: e.g. sponsor, report consumer, data owner] | [TODO] |

## Business terms

Terms the organisation uses with a specific meaning. Longer glossaries belong in `reference/`.

| Term | Meaning |
|---|---|
| [TODO] | [TODO] |

## Constraints

- Budget and capacity: [TODO: e.g. capacity size is fixed until a date; no new paid services]
- Change freeze periods: [TODO: e.g. month end, year end close]
- Other: [TODO]

## Writing conventions

| Setting | Value |
|---|---|
| English variant | [TODO: UK English or US English. If not set, the agent uses UK English.] |
| Main audience for documents | [TODO: e.g. IT leadership, finance director] |
| Other conventions | [TODO: e.g. terms to avoid, document headers] |

Dates are always written as "20 Oct 2026", whatever the English variant, so they cannot be misread.
