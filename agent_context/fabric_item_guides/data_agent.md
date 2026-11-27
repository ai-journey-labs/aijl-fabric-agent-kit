# Item guide: Data agent

| Field | Value |
|---|---|
| Item type in the Fabric REST API | `DataAgent` |
| Workload row in the organisation profile | Data agents |
| Status in Fabric | Data agents are generally available. In preview: git integration and deployment pipelines, the publish API, the SDK, evaluation, querying by a service principal, Copilot Studio, the Fabric IQ tool in Foundry, and the graph, ontology and Azure AI Search sources. |
| Checked against Microsoft documentation | 27 Nov 2026 |
| Verified in a live environment | Not yet |

General guidance for every organisation. Organisation rules for data agents are in `../context/07_fabric_item_rules.md` and take precedence over this guide; the rules in `AGENTS.md` take precedence over both.

## What it is

A data agent answers questions in natural language about an organisation's data. It turns a question into a read-only SQL, DAX or KQL query against the data sources it has been given, runs the query as the person asking, and returns the answer. It runs on a Microsoft-managed Azure OpenAI model that cannot be changed.

It is configured with:

- **data sources:** up to five, from lakehouse tables, warehouses, SQL databases, mirrored databases, semantic models and KQL databases (plus preview sources);
- **table selection:** per table; columns can be chosen only on semantic models prepared for AI;
- **agent instructions:** up to 15,000 characters, on how to answer and which source to use;
- **data source instructions and example queries:** up to 100 question and query pairs per source. Semantic models take neither here: their instructions come from the model's Prep for AI settings, and they use verified answers instead of example queries.

A data agent has a **draft**, which is edited, and a **published** version, which is read-only and is what consumers query. Publishing replaces what consumers see.

A data agent is a consumer of the tables it uses, as much as a semantic model is. Its example queries name tables and columns, so a schema change can break them.

## Before working on it

- The workload must be marked "Agent may work on this: Yes" in the organisation profile.
- Capacity: paid F2 or higher, or P1 or higher with Fabric enabled. The data sources must be on capacity in the same region as the agent.
- Tenant settings: "Users can use Copilot and other features powered by Azure OpenAI", and, outside the EU Data Boundary and the US, the two settings that allow data sent to Azure OpenAI to be processed and stored outside the capacity's region. For a service principal: "Service principals can call Fabric public APIs" (Developer settings; it was called "Service principals can use Fabric APIs" before Microsoft split it in 2025). Record in `06_platform_gotchas.md` which are on and who confirmed it.
- The data agent's tables and columns are treated as contract tables (rule 3). Record the agent as a consumer in the Contract table registry in `03_schema_contracts.md`.
- Check the organisation's AI policy and data strategy (rule 10). Answers leave Fabric when an agent is consumed elsewhere, and conversation history is kept for up to 28 days.

## How the agent reads it

- The pinned `fabric` MCP server has no data agent tools. `list_items` and `get_item` show that an agent exists. (Not yet verified live.)
- Read the configuration with Get Item Definition through `az rest`. It is a POST call, so the operator is asked even though it only reads.
- The definition's parts are `Files/Config/data_agent.json`, `Files/Config/draft/stage_config.json` (the agent instructions), one folder per data source under `draft/` holding `datasource.json` (selected tables and the source's instructions) and `fewshots.json` (example queries), and, once published, `publish_info.json` and the same files under `published/`.

## How the agent changes it

- Change the draft only, through Update Definition (`az rest`, POST, asks first), as part of an approved plan. Read the current definition first and keep everything the plan does not change.
- Never edit the `published/` parts.
- **Publishing is a separate, named step in the plan,** because it changes what every consumer sees at once. Unless the organisation's rules say otherwise, publishing is a human step: the agent prepares the draft, a person tests it and publishes it.
- Do not change how a data agent is consumed (Copilot Studio, Microsoft 365 Copilot, Foundry, its MCP endpoint). Those connections reach users outside Fabric; write a recommendation for a person.
- Write instructions and example queries to the organisation's standards in `07_fabric_item_rules.md`. Each example query must run and must use only selected tables.

## Security

- Queries run as the person asking. RLS and column-level security apply to them, and so do Purview data loss prevention and access restriction policies. Sharing the agent does not give anyone access to the data: each user needs Read on the semantic model, Read on the lakehouse, SELECT on the warehouse or Reader on the KQL database.
- Sharing has three levels: query the published version only (the default), view details, and edit and view details.
- In Copilot Studio, "Agent author authentication" runs every query as the person who built the Copilot Studio agent, so every user sees what the author sees. Flag it as a risk wherever it is proposed.
- Test what a user can see with a Viewer-only test principal holding only Read on the sources (rule 9). The agent's own access proves nothing.
- Whether a service principal can manage data agents is not settled in Microsoft's documentation. The REST reference lists service principals as supported for Create, Update Definition and Publish, while the source control page says service principals are supported only in ALM scenarios. Querying by a service principal is in preview and does not support KQL sources. Confirm in development before relying on any of it.

## Lifecycle

- Git integration and deployment pipelines are supported in preview. Both pipeline stages must be in the same tenant.
- How a deployment pipeline rebinds the agent's data sources to the next stage's items is not documented. Check every data source after a deployment.

## Verification

- Read the definition back and confirm only the planned parts changed.
- Ask the draft the questions in the plan, including at least one the agent should decline, and record the generated queries and answers.
- For larger changes, use Microsoft's evaluation library (preview, `fabric.dataagent.evaluation`) in a notebook with a set of questions and expected answers agreed with the data owner. It runs on Spark, so it asks first. Evaluation runs against a published stage.
- Repeat the checks as a Viewer-only test principal before the agent is shared further.

## Known limitations and traps

- Queries are read-only. Answers are limited to 25 rows by 25 columns.
- Lakehouse sources cover tables only, not files.
- Questions and answers are in English only.
- Not suited to "why" or root-cause questions.
- Data agents in Copilot in Power BI were reported retired on 26 Aug 2026; Microsoft's page now returns an error. (Not confirmed by Microsoft.)
- The older "Microsoft Fabric tool" in Foundry stopped being supported on 6 Nov 2026; its replacement, the Fabric IQ tool, is in preview.
- Microsoft's Update Definition example uses a part path that differs from the definition article. Follow the definition article.

## Sources

Checked 27 Nov 2026:

- Concepts: https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent
- Create and configure: https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent and https://learn.microsoft.com/en-us/fabric/data-science/data-agent-add-datasources
- Tenant settings: https://learn.microsoft.com/en-us/fabric/data-science/data-agent-tenant-settings
- Sharing and permissions: https://learn.microsoft.com/en-us/fabric/data-science/data-agent-sharing
- Service principals: https://learn.microsoft.com/en-us/fabric/data-science/data-agent-service-principal
- Source control and deployment: https://learn.microsoft.com/en-us/fabric/data-science/data-agent-source-control
- Definition: https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/data-agent-definition
- REST API: https://learn.microsoft.com/en-us/rest/api/fabric/dataagent/items
- SDK: https://learn.microsoft.com/en-us/fabric/data-science/fabric-data-agent-sdk
- Evaluation: https://learn.microsoft.com/en-us/fabric/data-science/evaluate-data-agent
- Consumption: https://learn.microsoft.com/en-us/fabric/data-science/data-agent-mcp-server, https://learn.microsoft.com/en-us/fabric/data-science/data-agent-microsoft-copilot-studio, https://learn.microsoft.com/en-us/fabric/data-science/data-agent-microsoft-365-copilot, https://learn.microsoft.com/en-us/fabric/data-science/data-agent-foundry-fabric-iq
- Tool names: the `ms-fabric-mcp-server` 0.8.7 description on PyPI.
