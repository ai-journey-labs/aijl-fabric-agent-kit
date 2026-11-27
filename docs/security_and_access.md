# Security and access

How the agent's access is controlled: the identity it works under, the permissions that limit its tools, credentials, requests for more access, security testing, and operators joining and leaving. For IT, the Fabric administrator and operators. Short answers to common questions are in [faq_fabric_administrator.md](faq_fabric_administrator.md).

## Identity

The identity the agent works under is its first fence (see Permissions and fences below): Fabric refuses anything that identity is not allowed to do, whatever the agent tries. Choose the identity model before setup starts, because it decides what IT and the Fabric administrator are asked for in the access request.

The table compares the identity models an organisation can use. Each supported option has an identity mode (`certificate`, `user` or `managed-identity`) that every operator sets on their workstation; `SETUP.md` gives the steps for each. Option A is the default.

| Option | How it works | Strengths | Weaknesses | Suits | Kit support in 0.1.x |
|---|---|---|---|---|---|
| **A. One service principal, one certificate per operator** | Every operator signs in as the same app registration, each with their own certificate | The agent cannot exceed the service principal's role on the development workspaces. One operator's access is revoked by removing one certificate. No client secrets | The Fabric activity log records the service principal, not the person. The Microsoft Entra sign-in logs record which certificate was used, so operators can be told apart only while each keeps their own certificate: if two operators share one, their activity cannot be distinguished | Most organisations | Supported (identity mode `certificate`). The default |
| **B. One service principal per operator** | A separate app registration for each operator, all in one security group with the same workspace role | Each person is identified separately in Fabric logs | More app registrations for IT to manage, renew and remove | Organisations that need per-person audit | Supported (identity mode `certificate`). Each operator sets their own client ID locally, and the Access model records one client ID per operator |
| **C. The operator's own user account** | The agent runs under the operator's normal sign-in | No identity setup | The agent receives all of the operator's access, which usually includes test, production and other services. There is no first fence | Not recommended for any organisation | Not supported. The connection check fails by design when the identity can see any workspace not marked Development |
| **D. A dedicated agent user account for each operator** | Each operator has a licensed agent user account, separate from their personal account, with access to the development workspaces only | Can use features that service principals cannot, for example running DAX queries against Direct Lake models (see `06_platform_gotchas.md`). Each person is identified separately in logs | Each account needs a licence, its own sign-in controls and multifactor authentication, and many security policies restrict non-personal accounts. One account shared by several operators is not supported: it cannot tell them apart and must be reset whenever anyone leaves | Organisations blocked by a service principal limitation | Supported (identity mode `user`). Not yet tested end to end |
| **E. Managed identity on an Azure virtual machine** | The agent runs on an Azure virtual machine with a managed identity. Operators sign in to that machine to work | No credential is held on any operator's workstation, nothing to renew, and network controls apply to the machine | Cost of the machine, and operators work remotely. Every process on the machine can use the identity, so whoever can sign in to the machine can act as the agent: sign-in to it must be limited to operators. With one shared machine, Fabric and Entra logs record only the identity; the machine's sign-in logs show who was working | Organisations with strict credential or network policies | Supported (identity mode `managed-identity`). Not yet tested end to end |

A further option, Microsoft Entra Agent ID (an identity type built for AI agents), is under review. It needs additional licensing, and its support in Fabric has not yet been confirmed.

Whichever option is chosen, record it in the Access model in `agent_context/context/01_environment_overview.md`.

In every mode, `scripts/kit_setup.py` pins each MCP server to a single credential in `.mcp.json`, so that neither can fall back to another sign-in on the workstation, such as the operator's personal account:

| Identity mode | `fabric` server (`AZURE_TOKEN_CREDENTIALS`) | `powerbi-modeling` server | Project Azure CLI profile |
|---|---|---|---|
| `certificate` | `EnvironmentCredential` | `--authmode=serviceprincipal` | `az login --service-principal` with the certificate |
| `user` | `AzureCliCredential` | `--authmode=interactive` | `az login` as the agent user account |
| `managed-identity` | `ManagedIdentityCredential` | `--authmode=managedidentity` | `az login --identity` |

The connection check in `SETUP.md` step 9 confirms the identity of both servers before any Fabric work.

## Permissions and fences

Two fences keep the agent inside its scope.

1. **Identity (first fence).** The agent's identity holds Contributor on the development workspaces only (see the Access model in `01_environment_overview.md`). Whatever the agent tries, Fabric refuses anything outside that scope. This fence is the same for Claude Code and GitHub Copilot, and it is the one that matters most.
2. **Tool permissions (second fence).** These decide which calls run freely, which ask the operator first, and which are blocked. They differ by tool:

| Control | Claude Code | GitHub Copilot in VS Code |
|---|---|---|
| Read-only calls | Run without asking (allow list in `.claude/settings.json`) | Ask at the Manual permission level unless the operator saves an approval |
| Writes, jobs, Livy sessions and statements | Ask the operator (ask list, or not listed) | Ask the operator at the Manual permission level |
| Destructive calls (deletes, force push) | Blocked by the deny list: `az rest` deletes, force pushes, and the `fabric` MCP server tools that delete an item, a folder or landed data. The `powerbi-modeling` server has no separate delete tools, so its deletes ask like its other calls | Not blocked. Terminal rules in User settings force a prompt; `AGENTS.md` and the Fabric Developer agent forbid them, and the agent file names the `fabric` delete tools |
| Removing part of an item, renames and SQL statements | Ask every time: removing a semantic model table, measure or relationship or a pipeline activity, `rename_item` (only in a plan that covers the rename, rule 3) and `execute_sql_statement` | Ask at the Manual permission level |
| Which tools the agent can use | All tools of the configured MCP servers | Limited by the `tools` list in `.github/agents/fabric-developer.agent.md` |
| Credential files | Blocked by `Read` deny rules | Not blocked; forbidden by instruction. Optional terminal sandboxing can deny paths |
| Who controls the rules | Kit file, changed only by a recorded change | Agent file is a kit file; terminal rules are each operator's User settings, added from `scripts/copilot_terminal_rules.json` by `scripts/kit_setup.py` |

Rules for terminal commands (`az rest`, `git push`) match the text of the command, in both tools. They catch the forms the agent normally writes, and they are not a security boundary:

- The Azure CLI uses the last `--method` given, so in both tools a `get` call that names a method a second time asks. Claude Code also denies a delete wherever `--method delete` or `-m delete` appears in the command. A delete written in some other form asks the operator instead of being blocked.
- `az rest --method get` runs without asking whatever host `--url` names and whatever token `--resource` attaches, so the rules do not stop a read being sent to a host outside Fabric. Narrowing this is planned (see `KIT_CHANGELOG.md`).
- In Claude Code the rules are written for the Bash tool. Its PowerShell tool is denied outright, so on Windows the agent runs commands in Git Bash.

This is why the identity is the first fence, and why the operator reads each call before approving it.

For Copilot users the second fence is weaker, so:

- Work at the Manual permission level for every Fabric session, and never use Assisted or Allow all.
- Treat the `list_workspaces` check in `SETUP.md` as mandatory: it is the proof that the first fence is in place.
- Consider Copilot's terminal sandboxing (`chat.agent.sandbox.enabled`) as an extra layer. It is available on macOS and Linux, and experimental on Windows 11.

How the identity options affect the fences:

- **Options A and B:** the first fence is the service principal's workspace role. Whoever holds a certificate can act as the agent, so each private key stays with its operator.
- **Option D:** the first fence is the agent account's workspace role, and the account's own sign-in controls and multifactor authentication protect it.
- **Option E:** the first fence includes the virtual machine. Every process on it can use its managed identity, so who can sign in to the machine decides who can act as the agent.
- **Option C (not supported):** the operator's own account usually reaches test, production and other services, so there would be no first fence. The connection check fails by design.

Behind both fences are the operating rules and the workflow in `AGENTS.md`, which apply whatever the tool and identity: nothing is implemented without an approved plan, the agent never deletes, and anything beyond development is a plan for a person.

## Credentials

- The kit never uses client secrets. `kit_setup.py` fails a workstation where `AZURE_CLIENT_SECRET` is set.
- Options A and B: each operator's private key stays in `~/.fabric-agent/` on their own workstation and is never shared, sent or committed. Certificates expire after one year and are renewed as `SETUP.md` step 11 describes.
- Option D: each agent account's password and multifactor authentication belong to its operator alone.
- Option E: there is no credential to hold; access to the agent is access to the virtual machine.
- Claude Code is denied read access to the key folder and the project Azure CLI profile (`.claude/settings.json`). The rules cover its file tools and the file commands it recognises in the Bash tool, such as `cat`; they do not cover a script or other program that reads a file indirectly.

## Elevated requests

The agent never asks for more access for itself, and never uses an operator's own access to get round its limits. Anything that needs more than Contributor on the development workspaces is a human step:

- tenant settings, capacity settings such as XMLA read-write, and workspace roles;
- connecting a workspace to git;
- deployments to test and production;
- deletions;
- anything in test or production.

The agent writes each one in the plan's Human steps as exact, numbered instructions for the Fabric administrator or other person named in Roles and approvers (`01_environment_overview.md`), and the plan says what should come back. The person carries it out and returns the result. Output that contains tenant detail goes in `agent_output/admin_returns/` or `agent_output/it_returns/`, which are not committed. The agent records the outcome in the change record without copying sensitive values.

## Security testing

The agent's own access proves nothing about security. Row-level security and OneLake security data access roles restrict Viewers only, so the Contributor role sees all the data, and a service principal cannot be added to an RLS role (AGENTS.md rule 9).

Security checks therefore use a Viewer-only test principal, offered as an optional item in the access request:

- an identity separate from the agent's, holding only the Viewer role on the development workspaces, and only the item permissions and security roles the check needs;
- preferably a test user account rather than a service principal, because some checks, such as DAX queries against models with RLS, do not work for a service principal (`06_platform_gotchas.md`);
- never a real person's account, and never with access to test or production.

The plan's verification states what the test principal must and must not see. A person signed in as the test principal runs the checks, as a human step, and the results go in the change record. Whether the test principal exists is recorded in the Access model in `01_environment_overview.md`.

## Onboarding and offboarding operators

Onboarding is `SETUP.md` steps 5 to 9, and the agent's `fabric-setup` skill. Offboarding is `SETUP.md` step 12: what IT removes depends on the option (a certificate, a service principal, an agent account, or sign-in access to the virtual machine).
