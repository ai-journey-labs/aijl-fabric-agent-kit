# Item guide: Fabric app

| Field | Value |
|---|---|
| Item type in the Fabric REST API | `AppBackend` |
| Workload row in the organisation profile | Fabric apps |
| Status in Fabric | Announced as generally available at Ignite (17 to 20 Nov 2026), but Microsoft's documentation still labels the item type, its REST API and its tenant setting as preview. Treat it as preview until the labels change. |
| Checked against Microsoft documentation | 27 Nov 2026 |
| Verified in a live environment | Not yet |

General guidance for every organisation. Organisation rules for Fabric apps are in `../context/07_fabric_item_rules.md` and take precedence over this guide; the rules in `AGENTS.md` take precedence over both.

## What it is

A Fabric app is a data-driven web application hosted in Fabric. A developer defines data models in TypeScript, and Fabric generates the database schema and a GraphQL API, stores the app's own data in a child SQL database (PostgreSQL in a Pro workspace), and hosts the front end. An app can also have server-side functions and file storage in OneLake. Connectors give it access to existing items: read-only on a lakehouse SQL endpoint, read and write on a warehouse or SQL database, and DAX queries on a semantic model. Apps are built and deployed with the open-source Rayfin SDK and command-line tool.

Do not confuse it with two older features with similar names. An **org app** (`OrgApp`) packages content for an audience and can include a Fabric app. A **workspace app** (formerly a Power BI app) publishes a workspace's reports. This guide covers neither.

Unlike most Fabric items, a Fabric app holds data its users write. That data lives in the app's database and is not in the item definition or in git.

## Before working on it

- The workload must be marked "Agent may work on this: Yes" in the organisation profile.
- Tenant settings: "Enable Fabric App Items (preview)" and "Users can create Fabric items"; for a service principal, "Service principals can call Fabric public APIs". "Enable anonymous data access for Fabric Apps (Preview)" allows apps to be public; record whether it is on.
- Licence: F, P or trial capacity, or a Power BI Pro workspace (no functions, file storage or public access on Pro). Only some regions are supported.
- Read the app's connectors. Every table it reads or writes through a connector is treated as a contract table (rule 3); record the app as a consumer in `03_schema_contracts.md`.

## How the agent reads it

- The pinned `fabric` MCP server has no Fabric app tools. `list_items` and `get_item` show that an app exists. (Not yet verified live.)
- Read the definition with Get Item Definition through `az rest` (POST, asks first). Its parts include `.platform`, `rayfin.yml`, `data/dab-config.json` (the data model), `connectors/<name>/dab-config.json`, `frontend/static-app.zip`, `functions/functions-app.zip`, `functions/deploymetadata.json` and `storage/storage-config.json`. It holds no rows, files, users or secret values.
- If the app's source is in a repository, read the source there rather than unpacking the zip parts.

## How the agent changes it

There is no draft. Every deployment goes live at once, and rollback means redeploying an earlier commit.

- **Deployment is a human step by default.** The Rayfin command-line tool signs in on its own, outside the kit's identity and permission controls, and a bare `rayfin up` deploys to whichever workspace the project's `rayfin/.env` currently points to. On an operator's machine that can be a production workspace. Unless the organisation's rules allow otherwise, the agent writes and tests the app's source and the plan names the deployment as a step for a person.
- Where the organisation does allow the agent to deploy, the plan names the development workspace explicitly, runs `rayfin up --dry-run` first and shows its output, and confirms the target before the real deployment.
- **Schema changes are additive only.** The tool refuses to drop or rename a column unless `--force` is passed, which can lose the app's data. Never use `--force` (rules 3 and 6); a breaking change needs a migration plan for a person.
- Schema edits made directly in the database (in the portal or SSMS) are overwritten by the next deployment. Change the data model in the source.
- Importing a definition applies its schema changes, which can be destructive. Treat Update Definition like a deployment.

## Security

- Members of the workspace can run and use an app by default; deploying needs Edit; resharing needs the workspace Admin role.
- Connectors to SQL sources use **application** authentication by default: they run as the app's identity, which Microsoft says is currently the app item's owner, so every user gets the owner's access to that data. **Delegated** authentication uses each user's own access. Prefer delegated, and flag application authentication as a risk in every review. If a service principal creates the app it is likely to become the owner, so the app would run with the service principal's access (an inference; Microsoft does not say).
- Semantic model connectors are delegated only, and the user needs Build permission.
- Row-level rules come from role policies in the data model. Checks in the front end are not a security boundary.
- Hosting is `protected` (signed-in users) by default; `public` allows anonymous access. Never set `public` without an organisation rule that allows it and an approved plan.
- Sharing an app also gives access to related items in its lineage.
- Test what a user can see as a Viewer-only test principal (rule 9).

## Lifecycle

- Git integration and deployment pipelines are supported.
- Deployment pipelines copy secret names but not their values, and do not remap connectors' workspace and item IDs. After a deployment, every connector can still point at the previous stage's items. Check each one.
- A Fabric administrator can block an app from loading (preview); blocking does not stop its functions or APIs.

## Verification

- For a deployment by a person: they run `rayfin up --dry-run` against development, share the output, deploy, and record the result.
- Read the definition back and confirm the data model and connectors match the plan.
- Test the app in development as the planned users, including a Viewer-only test principal, and confirm the row-level rules and connector authentication behave as planned.

## Known limitations and traps

- Deployed apps sign users in with Microsoft Entra single sign-on only.
- TypeScript only. Each entity needs a single UUID `id`; there are no composite keys, many-to-many relationships or raw SQL, and an app cannot use an existing database schema.
- Not supported with workspace outbound access protection or private links.
- Sharing an app that reads a lakehouse does not give Read on the lakehouse.
- Power BI Desktop for apps, the PostgreSQL database option and the Apps governance view are in preview.

## Sources

Checked 27 Nov 2026:

- Overview: https://learn.microsoft.com/en-us/fabric/apps/overview
- Connectors: https://learn.microsoft.com/en-us/fabric/apps/connectors
- Licensing: https://learn.microsoft.com/en-us/fabric/apps/licensing
- Deploy, and development and production: https://learn.microsoft.com/en-us/fabric/apps/deploy-app and https://learn.microsoft.com/en-us/fabric/apps/dev-prod-workflow
- Source control: https://learn.microsoft.com/en-us/fabric/apps/source-control
- Data permissions: https://learn.microsoft.com/en-us/fabric/apps/data-permissions
- Hosting: https://learn.microsoft.com/en-us/fabric/apps/hosting
- Troubleshooting and FAQ: https://learn.microsoft.com/en-us/fabric/apps/troubleshooting and https://learn.microsoft.com/en-us/fabric/apps/faq
- Sharing: https://learn.microsoft.com/en-us/fabric/apps/share-app
- Blocking apps: https://learn.microsoft.com/en-us/fabric/governance/block-unblock-fabric-apps
- REST API: https://learn.microsoft.com/en-us/rest/api/fabric/appbackend/items/create-app-backend
- Tenant settings: https://learn.microsoft.com/en-us/fabric/admin/tenant-settings-index
- Ignite 2026 Book of News: https://news.microsoft.com/events/ignite/2026/book-of-news/
- Tool names: the `ms-fabric-mcp-server` 0.8.7 description on PyPI.
