# 06 Platform gotchas

Last reviewed: [TODO: date]

Lessons about Fabric and the tooling that affect how work is planned. Entries marked "carried over, re-verify in this environment" come from earlier engagements; once verified here, replace the marker with "confirmed [date]".

## Direct Lake

These entries apply where semantic models use Direct Lake (see the Key facts in [01_environment_overview.md](01_environment_overview.md)).

- Direct Lake models bind by table name, column name and type; views over Direct Lake fall back to DirectQuery or are unsupported. (Carried over, re-verify in this environment.)
- `mode("overwrite")` on a Direct Lake Delta table rewrites the log, defeats incremental framing and forces cold reloads. (Carried over, re-verify in this environment.)

## Capacity

- [TODO: capacity behaviour observed in this environment, such as throttling thresholds, Spark session limits, peak periods.]

## Deployment and git

- Deployment pipelines do not automatically rebind Direct Lake models to the target stage's lakehouse; check every model's binding after a deployment. (Carried over, re-verify in this environment.)
- Contract tables built from OneLake shortcuts can silently read another stage's storage; check shortcut targets. (Carried over, re-verify in this environment.)
- Connecting a workspace to git needs the workspace Admin role, so it is always a human step. Microsoft documents that a service principal can commit and update through the git APIs using a stored connection (checked 27 Nov 2026), but this is not verified here: until it is, workspace commit and Update all are human steps. (Re-verify in this environment.)

## Security

- Contributor bypasses OneLake security and semantic model RLS, so the agent's own access proves nothing about security. Use a Viewer-only test principal. (Carried over, re-verify in this environment.)

## Tenant prerequisites

- [TODO: tenant settings the agent depends on, such as service principals allowed to use Fabric APIs, XMLA endpoint read and write, and who confirmed each one and when.]

## MCP tooling

- `get_notebook_driver_logs` is the way to read a notebook's printed output and traceback after a job; the job API gives only a generic failure reason. (Carried over, re-verify in this environment.)
- Large `list_items` results spill to a file; read the file rather than assuming the result is empty or truncated. (Carried over, re-verify in this environment.)
- The Execute Queries API (`execute_dax_query`) returns 401 for a service principal on Direct Lake models (single sign-on) and on models with RLS; it works on import models without RLS. A person runs DAX for Direct Lake in the DAX query view. (Carried over, re-verify in this environment.)
- Fallback via `az rest` on the project Azure CLI profile covers: git connection state, job status polling, lakehouse table listing, `getDefinition`, and OneLake DFS reads (resource `https://storage.azure.com`). (Carried over, re-verify in this environment.)
