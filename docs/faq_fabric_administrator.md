# Questions from the Fabric administrator

For the Fabric administrator and IT security reviewers. Each answer is short and points to where the detail lives; the authoritative description of identity and permissions is [security_and_access.md](security_and_access.md).

Statements about Microsoft Fabric were checked against Microsoft's documentation on 27 Nov 2026. Fabric changes often: where an answer matters to a decision, confirm it in your own tenant. Your organisation's own choices (identity option, security group, approvers) are recorded in the Access model and Roles and approvers in `agent_context/context/01_environment_overview.md`.

## Identity and access

### What identity does the agent use?

Its own, never an operator's personal account. The organisation chooses one option before setup:

| Option | Identity |
|---|---|
| A (the default) | One service principal, with one certificate per operator |
| B | One service principal per operator, each with its own certificate |
| D | One dedicated agent user account per operator, licensed, with multifactor authentication |
| E | The managed identity of an Azure virtual machine that operators sign in to |

Option C, the operator's own account, is not supported: the connection check fails by design when the identity can see any workspace not marked Development. The options are compared, with their strengths and weaknesses, in the Identity section of [security_and_access.md](security_and_access.md).

### What exactly will we be asked for?

An access request, written by the agent from `agent_output/_templates/access_request_template.md` during setup. It asks for:

- the identities for the chosen option (app registrations with certificate authentication and no client secret, agent user accounts, or a virtual machine with a managed identity);
- a security group holding those identities;
- for options A, B and E, that group in the tenant setting that lets service principals call Fabric public APIs, limited to specific security groups;
- the Contributor role for that group on each development workspace, and no role on any other workspace;
- optionally, XMLA read-write on the development capacity, and a Viewer-only test principal.

It also lists what the agent will not have: no role on test or production workspaces, no tenant, capacity or workspace administration rights, and no client secret.

### Which tenant settings does the agent depend on?

- **"Service principals can call Fabric public APIs"** (Developer settings), limited to the agent's security group. Needed for options A and B. Microsoft's identity support page still refers to the older name, "Service principals can use Fabric APIs", for both service principals and managed identities, so for option E confirm in your tenant which setting applies. Option D needs neither.
- **"Service principals can create workspaces, connections, and deployment pipelines"** is not needed. The agent does not create workspaces, connections or deployment pipelines.
- **XMLA read-write**, only if the agent is to change semantic models through the XMLA endpoint: the capacity's XMLA Endpoint setting (under the capacity's Power BI workloads) set to Read Write, and the tenant setting "Allow XMLA endpoints and Analyze in Excel with on-premises semantic models". Microsoft announced read-write as the default for capacities from 9 Jun 2025, though some pages still describe read-only as the default; check your capacity.
- **Settings for particular workloads**, only if your organisation puts them in scope: for example, the Copilot and Azure OpenAI settings for data agents and the Fabric app settings. Each is named in its guide in `agent_context/fabric_item_guides/`.

### Why Contributor, and not Member or Admin?

Contributor is the lowest role that can create, edit and run items. It cannot add or remove people, update or delete the workspace, connect the workspace to git, publish apps or manage semantic model permissions, and it can share items only if someone grants it reshare permission.

Contributor can delete items in the development workspaces. Fabric does not prevent that; the kit does, through its permission rules and operating rules (the second fence). See Permissions and fences in [security_and_access.md](security_and_access.md).

### Does its access prove our security works?

No. Row-level security and OneLake security data access roles restrict Viewers only; Admin, Member and Contributor all have full access to the data. The agent's own results therefore say nothing about what a reader can see. Security checks use a separate Viewer-only test principal, which the access request offers as an optional item (AGENTS.md rule 9).

### Does the agent need a licence?

- **Agent user accounts (option D):** yes. On any F capacity, a Contributor who creates or edits Power BI items (semantic models, reports) needs a Pro or Premium Per User licence. A Free licence is enough only for non-Power BI Fabric items.
- **Service principals and managed identities (options A, B, E):** no licence is needed.

The agent uses the capacity of the development workspaces it works in.

### How do we confirm it cannot reach test or production?

Each operator runs a connection check before doing any Fabric work: the agent lists the workspaces its identity can see, through both MCP servers, and the list must contain exactly the development workspaces. If it shows any other workspace, the agent stops all Fabric work until the lead operator confirms the access has been corrected. The results are recorded in the Operators table of `agent_context/setup_status.md`. You can confirm the same from your side by checking the security group's workspace roles.

### How do we stop it at once?

- **For every operator:** remove the security group's role from the development workspaces, or remove the identities from the group.
- **For one operator:** remove their certificate (option A), disable their service principal (option B), disable their agent account and revoke its sessions (option D), or remove their sign-in to the virtual machine (option E). `SETUP.md` step 12 has the full steps.

Access tokens already issued remain valid until they expire, typically within about an hour to an hour and a half. Removing the workspace role is the quickest way to cut off Fabric access.

## Controls and oversight

### What stops it changing production or deleting things?

Three layers (see [overview.md](overview.md)):

1. **Its identity** has no role outside the development workspaces, so Fabric refuses anything else.
2. **Tool permissions:** in Claude Code, read-only calls run freely, anything that writes, runs a job or uses capacity asks the operator, and the tools that delete items or data are denied outright. GitHub Copilot has no deny list, so for Copilot users this layer relies on the operator's approvals and the agent's instructions.
3. **The operating rules:** nothing is implemented without a plan approved by a named person, nothing is deleted, and changes to test and production are written up as plans for people.

### What consumes capacity, and can we see its usage?

Notebook runs, Spark (Livy) sessions and statements, SQL and DAX queries, and semantic model refreshes. Each asks the operator before it starts, and setup discovery runs none of them. To attribute usage:

- the Monitor hub shows who submitted each job (under Advanced details);
- the User column of the Capacity Metrics app shows who triggered interactive operations, when the tenant setting "Show user data in the Microsoft Fabric Capacity Metrics app and reports" is on (the default).

Capacity constraints, such as busy periods, are recorded in the organisation profile.

### How are its actions audited?

Fabric records activities in the Microsoft Purview audit log, and the admin monitoring workspace reports on them. Activities appear under the agent's identity:

- options B and D identify each operator separately;
- with option A, every operator appears as the same service principal, and the Microsoft Entra sign-in logs tell them apart by certificate;
- with option E, the virtual machine's sign-in logs show who was working.

Microsoft does not document exactly how a service principal is shown in audit records, so check one in your tenant. Each activity can be matched to the change record (`CHG-###`) in `agent_output/` and to the git history.

### What will you ask the Fabric administrator to do?

The access request at setup. After that, anything that needs more than the agent's access appears in a plan's Human steps as exact, numbered instructions for the Fabric administrator named in Roles and approvers: tenant and capacity settings, deployments to test and production, and anything else beyond Contributor. Nothing is requested informally.

### What about git integration and deployment pipelines?

- **Git:** connecting a workspace to git needs the workspace Admin role, so it is always a human step. Microsoft now documents that a service principal can commit and update through the git APIs using a stored connection, but the kit treats workspace commits as human steps until this is verified in your environment (`06_platform_gotchas.md`).
- **Deployment pipelines:** the agent never deploys beyond development. Deployments to test and production are written as plans for the people who run them.

## Software and data

### What software runs on operators' workstations?

Claude Code or Visual Studio Code with GitHub Copilot, the tools in `SETUP.md` step 1, and two MCP servers that the agent starts locally from pinned versions in `scripts/mcp_servers.json`:

| Server | Published by | Notes |
|---|---|---|
| `ms-fabric-mcp-server` 0.8.7 (PyPI) | Published from a repository on an individual's GitHub account, not Microsoft's GitHub organisation | MIT licence, marked Beta. Its README says it is for development environments only |
| `@microsoft/powerbi-modeling-mcp` 1.0.0 (npm) | Microsoft | Use is subject to Microsoft's EULA. The kit never accepts it on anyone's behalf: the lead operator decides at setup, and the server is used only if they accept. The agent is blocked from calling the server's own `accept_eula` tool. Its README says it may send usage information to Microsoft. Microsoft now calls it the Power BI Authoring MCP server |

The servers call Fabric directly from the workstation (or the virtual machine, for option E) as the agent's identity. Each is pinned to that one credential, so neither can fall back to another sign-in on the machine. Versions change only through a new kit version or a recorded change tested in development first.

### How are credentials handled?

- No client secrets: the setup script fails a workstation where one is set.
- Options A and B: each operator's private key stays in their own home folder and is never shared, sent or committed. Certificates last one year and are renewed as `SETUP.md` step 11 describes.
- Claude Code is denied read access to the key folder and the project Azure CLI profile. GitHub Copilot is forbidden to read them by instruction only.

See Credentials in [security_and_access.md](security_and_access.md).

### What data leaves the tenant?

What the agent reads in order to work: files in its repository, and the results of its calls to Fabric, including item definitions, logs and query results. These go to the AI service behind the operator's tool (Claude Code or GitHub Copilot). The organisation records which AI tool and provider it uses, and whether development holds real personal or confidential data, under "AI tools and data" in `agent_context/organisation/profile.md`. See also [faq_leadership.md](faq_leadership.md).

### Can it use Microsoft Entra Agent ID?

Not yet. Entra Agent ID is an identity type built for AI agents. Fabric documentation does not yet describe support for it, so it is under review rather than an identity option.

### How do we report a security problem?

A problem in the kit itself: as `SECURITY.md` describes. A problem in your own Fabric environment or repository: through your organisation's own process.
