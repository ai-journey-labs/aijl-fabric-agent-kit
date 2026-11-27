# Item guide: Notebook

| Field | Value |
|---|---|
| Item type in the Fabric REST API | `Notebook` |
| Workload row in the organisation profile | Lakehouse and notebooks (Data Engineering) |
| Status in Fabric | Generally available. Notebook version history and `notebookutils.data` in Python notebooks are in preview. |
| Checked against Microsoft documentation | 27 Nov 2026 |
| Verified in a live environment | Not yet |

General guidance for every organisation. Organisation rules for notebooks, and its code and documentation standards, are in `../context/07_fabric_item_rules.md` and take precedence over this guide; the rules in `AGENTS.md` take precedence over both.

## What it is

A notebook holds code cells (PySpark, Python, Spark SQL, Scala or SparkR) and markdown cells, and runs on a Spark session or, for Python notebooks, on a single-node Python runtime. Notebooks do most of the loading and transformation in a lakehouse layout, and they are run by hand, on a schedule, or from a pipeline.

Notebooks are code that other people will read, review and support. This guide sets a default layout and code style so that every notebook the agent writes is legible to the team. The organisation's own standards in `07_fabric_item_rules.md` replace these defaults wherever they are set.

## Before working on it

- Read the notebook's row in `02_workspace_inventory.md`: purpose, what it reads and writes, parameters and schedule.
- Check which tables it writes. If any is a contract table, or feeds a Direct Lake model, rules 3 and 5 apply to the change.
- Check what runs it. A notebook run from a pipeline runs as the user who last modified the pipeline; a scheduled notebook runs as the person who set the schedule. Changing either changes the identity the notebook runs as.

## How the agent reads it

- `get_notebook_definition` returns the notebook's source and metadata. It is on the allow list. (Not yet verified live.)
- `list_notebook_runs`, `get_notebook_run_details` and `get_notebook_driver_logs` show past runs; `get_notebook_driver_logs` is the way to read a run's printed output and traceback (see `06_platform_gotchas.md`).
- Fallback: Get Item Definition through `az rest`. It is a POST call, so the operator is asked even though it only reads.

In the definition and in the Fabric environment repo, a PySpark notebook is a folder `Name.Notebook/` holding `.platform` and `notebook-content.py`. The source file uses markers: `# CELL ********************` before each code cell, `# MARKDOWN ********************` before each markdown cell (each line prefixed with `# `), `# PARAMETERS CELL ********************` before the parameter cell, and `# METADATA` blocks holding the kernel, default lakehouse and environment. Spark SQL, Scala and SparkR notebooks use `.sql`, `.scala` and `.r`. Cell output is not stored.

## How the agent changes it

- `create_notebook` and `update_notebook_definition` ask the operator first. Running a notebook (`run_on_demand_job`) consumes capacity and also asks.
- Change notebooks only as part of an approved plan, in development. Keep each change to what the plan names; an unrelated problem found in the same notebook becomes a new review record (rule 7).
- Before updating a definition, read the current one and keep everything the plan does not change, including the `# METADATA` blocks. Never edit the `logicalId` in `.platform`. `.platform` is applied on update only when `updateMetadata=true` is passed.
- Check the default lakehouse in the metadata (`dependencies.lakehouse`: `default_lakehouse`, `default_lakehouse_name`, `default_lakehouse_workspace_id`) points to the development lakehouse.
- Writes to Delta tables follow rules 3 and 5: no `mode("overwrite")` on a table that feeds Direct Lake, and no `overwriteSchema` on a contract table.
- Never put credentials, keys or connection strings in a notebook.

## Default layout

Use this layout unless `07_fabric_item_rules.md` sets another.

1. **`%%configure` cell**, only if the notebook needs one. Microsoft requires it to be the first cell, otherwise pipeline runs fail. (Whether a markdown cell before it counts is not documented; put it first.)
2. **Header**, a markdown cell:
   - title: the notebook's name;
   - purpose: one or two sentences, in business terms;
   - inputs: tables and files read, with their layer;
   - outputs: tables written, with the write mode (append, merge, partition overwrite);
   - run by: the pipeline or schedule, and the parameters it passes;
   - owner: a role or team;
   - changes: "See `agent_output/change_log.md`", not a list of changes. The change records and git history are the record.
3. **Parameters**, one parameter cell directly after the header. One parameter per line, each with a comment giving its meaning and an example. Parameters can only be `int`, `float`, `bool` or `str`; pass anything larger as a JSON string. Names use ASCII letters, digits and underscores only. Workspace and lakehouse IDs come from parameters or a Variable Library, never hard-coded.
4. **Imports and constants**, one code cell.
5. **Steps**, each starting with a markdown cell whose first line is a numbered heading, such as `## 2. Deduplicate orders`. The first heading of each markdown cell appears in the notebook's Contents pane, so the headings are the notebook's table of contents. Under each heading, say in a sentence or two what the step does and why, and cite the requirement or business rule it implements.
6. **One logical step per code cell**, short enough to read without scrolling far.
7. **Final cell**: checks and a summary, such as row counts read and written. If the notebook returns a value, call `notebookutils.notebook.exit()` here, and never inside `try`/`except`.

## Default code style

Fabric notebooks have no documented built-in formatter or linter, so the agent formats code as it writes it.

- **Python and PySpark:** PEP 8, as `ruff format` (or `black`) formats it with default settings. `snake_case` names. `from pyspark.sql import functions as F`.
- **PySpark chains:** wrap the chain in parentheses with one transformation per line; no backslash continuations. Name columns explicitly; do not write `select("*")` to a contract table.
- **Spark SQL:** keywords in upper case, one selected column per line, table names fully qualified where the notebook reads more than one lakehouse.
- **Utilities:** use `notebookutils`, not `mssparkutils`, which Microsoft is retiring.
- **Comments** explain why, not what. A business rule cites its source: a requirement (`R#####`), a reference document or a change (`CHG-###`).
- **Shared code:** reuse through `%run` of a shared notebook (same workspace, at most five levels deep) or through `notebookutils.notebook.run` and `runMultiple`. Say which in the header's "run by" line.

## Security

- A notebook reads and writes with the identity it runs as. The agent's own Contributor access bypasses OneLake security and RLS, so its runs prove nothing about what a reader can see (rule 9).
- Changing a pipeline that runs a notebook makes the changer the identity future runs use. If the agent's service principal modifies the pipeline, the notebook then runs as the service principal. State this in the plan.

## Lifecycle

- **Git:** the default lakehouse ID stays in the notebook metadata when a notebook is synced from git into another workspace, so it may still point at the original lakehouse. Lakehouse auto-binding (a notebook setting, stored in `notebook-settings.json`, which Fabric manages) replaces physical IDs with logical ones; do not edit that file.
- **Deployment pipelines:** bind the default lakehouse and environment automatically when they are in the same workspace as the notebook. A "Default lakehouse" deployment rule on the target stage overrides this. Check bindings after every deployment (see `06_platform_gotchas.md`).
- Frozen cells do not stay frozen through deployment pipelines.
- The notebook's resources folder is not committed to git by default.

## Verification

- After an update, read the definition back and confirm only the planned cells changed and the metadata is intact.
- Run the notebook in development with the planned parameters (asks first). Read the result with `get_notebook_run_details` and `get_notebook_driver_logs`.
- Check the outputs against the plan's verification step: row counts, schema unchanged or additive only, and no duplicate keys after a merge.

## Known limitations and traps

- `%%configure` must be the first cell; `notebookutils.notebook.run` ignores the child notebook's `%%configure`.
- A child notebook with a different default lakehouse from its parent is blocked unless `useRootDefaultLakehouse` is set.
- `%run` works within one workspace only. In Python notebooks it cannot run `.py` files from the resources folder, and Python notebooks cannot use environments.
- The resources folder holds at most 500 MB, 100 MB per file and 100 files and folders.
- After pinning a new default lakehouse, restart the session.

## Sources

Checked 27 Nov 2026:

- Notebook source control and deployment: https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-source-control-deployment
- Notebook definition: https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/notebook-definition
- Develop, execute and manage notebooks: https://learn.microsoft.com/en-us/fabric/data-engineering/author-execute-notebook
- How to use notebooks: https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook
- NotebookUtils and notebook run: https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-utilities and https://learn.microsoft.com/en-us/fabric/data-engineering/notebookutils/notebookutils-notebook-run
- Spark development best practices: https://learn.microsoft.com/en-us/fabric/data-engineering/spark-best-practices-development-monitoring
- CI/CD best practices: https://learn.microsoft.com/en-us/fabric/fundamentals/understand-best-practices-fabric-cicd
- Tool names: the `ms-fabric-mcp-server` 0.8.7 description on PyPI.
