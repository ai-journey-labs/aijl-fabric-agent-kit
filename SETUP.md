# Workstation setup

> **Not yet tested end to end:** identity modes `user` (option D) and `managed-identity` (option E), and setup on macOS and Linux. Setup with identity mode `certificate` (options A and B) has been tested on Windows. Tracked in `KIT_CHANGELOG.md`.

Follow these steps in order on each operator workstation, on Windows, macOS or Linux. They prepare the workstation, start the agent so it can walk you through setting itself up, and then connect it to the development workspaces as the agent's identity. Nothing in this checklist writes a credential into the repository.

The identity option is chosen once for the organisation and recorded in the Access model in `agent_context/context/01_environment_overview.md` (options are compared in the Identity section of `docs/security_and_access.md`). Each option has an identity mode, which you set in step 7 and which decides your path through steps 5 to 8, 11 and 12:

| Option | Identity mode | You sign in as |
|---|---|---|
| A. One service principal, one certificate per operator | `certificate` | The agent's service principal, with your own certificate |
| B. One service principal per operator | `certificate` | Your own service principal, with your own certificate |
| D. A dedicated agent user account | `user` | Your own agent user account (one per operator), never your personal account |
| E. Managed identity on an Azure virtual machine | `managed-identity` | The virtual machine's managed identity; you work on that machine |

Option C (the operator's own account) is not supported.

Conventions:
- Windows commands are for PowerShell, the default terminal in VS Code on Windows. On macOS and Linux, type `python3` wherever this file says `python`.
- `<sp-name>` is the name of the service principal you sign in as (options A and B), and `<client ID>` and `<tenant ID>` are its identifiers. `<agent-account>` is your agent user account (option D). All are recorded in the Access model in `agent_context/context/01_environment_overview.md`.
- `<initials>` is your initials, for example `JS`.
- Your private key (options A and B) lives in `~/.fabric-agent/` and your project Azure CLI profile in `~/.azure-fabric-agent/`, where `~` is your home folder (`%USERPROFILE%` on Windows). The agent is denied read access to both.
- Option E: do every step on the Azure virtual machine, signed in to it with your own account, not on your own workstation.

## 1. Install the tools

1. Git. On Windows, install Git for Windows, which includes Git Bash and the `openssl` used in step 5 (options A and B). Claude Code also runs the agent's commands in Git Bash: its PowerShell tool is turned off by the permission rules. macOS and Linux include `openssl`.
2. Python 3.11 or later.
3. uv, which provides `uvx` to run the Fabric MCP server.
4. Node.js LTS, version 18 or later, which provides `npx` to run the Power BI modeling MCP server.
5. Azure CLI.
6. Visual Studio Code.
7. Your agent: Claude Code and the Claude Code extension for VS Code, or the GitHub Copilot Chat extension (which needs a Copilot licence). VS Code offers both when you open the repository.

Supported platforms are Windows (x64 and Arm64), macOS on Apple silicon, and Linux (x64 and Arm64). The pinned Power BI modeling MCP server has no release for Intel Macs; on one, setup leaves that server out and the agent cannot work on semantic models. Tell the lead operator if that applies to you.

## 2. Clone the repositories

1. Clone this repository.
2. Clone the Fabric environment repo (URL in `01_environment_overview.md`, Environments and deployment). If the organisation has not been set up yet, the lead operator does this once it is known.

## 3. Run the kit setup script

From the repository root, in your own terminal:

```
python scripts/kit_setup.py
```

The script checks the tools from step 1, generates `.mcp.json` for your platform from `scripts/mcp_servers.json`, and creates `.claude/settings.local.json` from the example if it does not exist. Both files are git-ignored. It never overwrites your local settings and never prints credential values. Add `--copilot` if you use GitHub Copilot.

Fix every line marked FAIL. Lines marked TODO for the credential variables are expected until step 8. Run `python scripts/kit_setup.py --check` at any time to check without changing anything.

## 4. Start the agent and ask it to set itself up

The organisation stages of setup need no credentials, so the lead operator can start them now.

**Claude Code**

1. Open this repository's folder in VS Code and start Claude Code.
2. Approve the project MCP servers if prompted. They cannot reach Fabric until step 9; that is expected.

**GitHub Copilot**

1. Add the terminal rules to your VS Code User settings: `python scripts/kit_setup.py --apply-copilot-rules`. The script saves a backup first, and changes the file only if it is plain JSON. Otherwise, add the rules from `scripts/copilot_terminal_rules.json` by hand under `chat.tools.terminal.autoApprove`. Copilot ignores terminal rules in workspace settings. A rule set to `false` makes Copilot ask every time, even if a command was approved before.
2. Fully restart VS Code, open this repository and open Copilot Chat.
3. Select the **Fabric Developer** agent and set the permission level to **Manual**. Use the Copilot harness, not the deprecated Local harness.

**Then**

Say "Set yourself up". The agent uses its `fabric-setup` skill: it reads `agent_context/setup_status.md`, tells you which stages are done, and interviews you for the next one. You can stop at any point and resume in a later session. If the organisation is already set up, it goes straight to your own workstation and connection check.

## 5. Prepare your credential

Follow the part for your identity option.

### Options A and B: create your certificate

Each operator has their own certificate. Never share or copy another operator's key: the Microsoft Entra sign-in logs tell operators apart only by their certificates.

1. Create the key folder and limit it to your own account.

   Windows (PowerShell):
   ```
   New-Item -ItemType Directory -Force "$HOME\.fabric-agent" | Out-Null
   icacls "$HOME\.fabric-agent" /inheritance:r /grant:r "${env:USERNAME}:(OI)(CI)F"
   ```
   macOS and Linux:
   ```
   mkdir -p ~/.fabric-agent && chmod 700 ~/.fabric-agent
   ```
2. Create a self-signed certificate with a one-year expiry, in Git Bash on Windows or a terminal on macOS and Linux:
   ```
   cd ~/.fabric-agent
   MSYS_NO_PATHCONV=1 openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
     -subj "/CN=<sp-name>-<initials>" \
     -keyout <sp-name>-<initials>.key -out <sp-name>-<initials>.crt
   ```
   Keep `MSYS_NO_PATHCONV=1` at the start. Without it, Git Bash on Windows rewrites the `/CN=...` subject as a file path, and `openssl` stops with "subject name is expected to be in the format /type0=value0" after writing the `.key` file but no `.crt` file. If that happens, run the command again in full; it replaces the `.key` file. The setting has no effect on macOS and Linux.
3. Convert to the PEM file the tools read (private key followed by certificate, in one file):
   ```
   cat <sp-name>-<initials>.key <sp-name>-<initials>.crt > <sp-name>-<initials>.pem
   ```
   On macOS and Linux, also limit the key files to your account: `chmod 600 *.key *.pem`.
4. Record the thumbprint and expiry date:
   ```
   openssl x509 -in <sp-name>-<initials>.crt -noout -fingerprint -sha1 -enddate
   ```
5. Keep the `.key` and `.pem` files in this folder only. Do not email, upload or commit them.

### Option D: receive your agent user account

1. IT creates an agent user account for you alone (`<agent-account>`), separate from your personal account. Never share it: a shared account cannot tell operators apart and has to be reset whenever anyone leaves.
2. Set up its sign-in and multifactor authentication on your own device, as IT instructs. Keep its password in your password manager only.
3. Never use the agent account for anything except the agent, and never sign your personal account in to the project Azure CLI profile.

### Option E: get access to the virtual machine

1. IT gives you sign-in access to the agent's Azure virtual machine. Everyone who can sign in to it can act as the agent, so access is limited to operators listed in Roles and approvers.
2. Sign in to the machine with your own account and do steps 1 to 4 there, if they have not been done for your account yet.
3. There is no certificate or password for the agent: the machine's managed identity is the agent's identity.

## 6. Confirm your access

- **Options A and B.** Send only the public certificate file (`<sp-name>-<initials>.crt`) to the lead operator, with its thumbprint and expiry date. The lead operator records it in the Access model in `01_environment_overview.md` and checks you are listed in Roles and approvers. Human step for your IT team: upload the public certificate to the app registration (Certificates and secrets, Certificates, Upload certificate) and confirm the thumbprint matches. For option B, IT also tells you your own service principal's client ID. Continue only after IT confirms.
- **Option D.** The lead operator records your agent account in the Access model and checks you are listed in Roles and approvers. Continue only after IT confirms the account has the development workspace role.
- **Option E.** The lead operator records you as a user of the machine in the Access model and checks you are listed in Roles and approvers.

For the first operator, this is part of the access request the agent drafts during setup.

## 7. Fill in your local settings

1. Open `.claude/settings.local.json`, created in step 3. It is git-ignored.
2. Set `FABRIC_AGENT_IDENTITY` to your identity mode: `certificate`, `user` or `managed-identity`.
3. Set `FABRIC_AGENT_PBI_EULA` to the lead operator's decision on Microsoft's EULA for the `powerbi-modeling` server, recorded under Tooling in `agent_context/context/01_environment_overview.md`: `accepted` or `declined`. The kit never accepts the EULA for you: `kit_setup.py` adds the server to `.mcp.json` only when this is `accepted`, and leaves it out otherwise.
4. Fill in the lines your mode uses, and remove the others. `kit_setup.py` reports a line your mode does not use, because it could make a tool sign in as another identity.

   | Setting | `certificate` (A, B) | `user` (D) | `managed-identity` (E) |
   |---|---|---|---|
   | `AZURE_TENANT_ID`: the tenant ID | Required | Required | Optional |
   | `AZURE_CLIENT_ID`: the client ID of the service principal you sign in as | Required | Remove | Only for a user-assigned managed identity: its client ID |
   | `AZURE_CLIENT_CERTIFICATE_PATH`: the full path to your `.pem` file | Required | Remove | Remove |
   | `AZURE_CONFIG_DIR`: the full path to your project Azure CLI profile | Required | Required | Required |

   Example paths: `C:\Users\<you>\.fabric-agent\<sp-name>-<initials>.pem` on Windows, `/Users/<you>/.fabric-agent/<sp-name>-<initials>.pem` on macOS or `/home/<you>/.fabric-agent/<sp-name>-<initials>.pem` on Linux; `C:\Users\<you>\.azure-fabric-agent` or `/Users/<you>/.azure-fabric-agent` for the profile.
5. Do not set `AZURE_CLIENT_SECRET`, `AZURE_TOKEN_CREDENTIALS` or `PBI_MODELING_MCP_ACCEPT_EULA`. The kit uses no client secrets, and `kit_setup.py` sets the other two in `.mcp.json`.
6. Run `python scripts/kit_setup.py` again, so `.mcp.json` pins each MCP server to your mode's credential.
7. Check that `git status` does not list `settings.local.json`.

## 8. Log the project Azure CLI profile in

1. In a terminal, point the Azure CLI at the project profile for this terminal session only, and sign in as the agent's identity.

   Windows (PowerShell):
   ```
   $env:AZURE_CONFIG_DIR = "$HOME\.azure-fabric-agent"
   ```
   macOS and Linux:
   ```
   export AZURE_CONFIG_DIR=~/.azure-fabric-agent
   ```
   Then, for your option:
   - **Options A and B**, with your certificate:
     ```
     az login --service-principal --username <client ID> --tenant <tenant ID> --certificate "<path to your .pem file>" --allow-no-subscriptions
     ```
   - **Option D**, as your agent account. When the sign-in window opens, choose `<agent-account>`, never your personal account:
     ```
     az login --tenant <tenant ID> --allow-no-subscriptions
     ```
   - **Option E**, on the virtual machine:
     ```
     az login --identity --allow-no-subscriptions
     ```
2. Check: `az account show` reports the agent's identity, not your personal account (a service principal for A and B, `<agent-account>` for D, `systemAssignedIdentity` or `userAssignedIdentity` for E). Your normal Azure CLI profile is unchanged. `python scripts/kit_setup.py --check` checks the kind of identity for you.

## 9. Check the workstation and connect

1. **GitHub Copilot users only: credentials.** Copilot does not read `.claude/settings.local.json`, so the variables your mode uses (step 7) must also be in the environment VS Code starts from, including `FABRIC_AGENT_IDENTITY`. Keep `FABRIC_AGENT_IDENTITY` in `.claude/settings.local.json` as well: `kit_setup.py` reads it there to generate `.mcp.json`. On Windows, set them as user environment variables (Settings, System, About, Advanced system settings, Environment Variables). On macOS and Linux, export them in your shell profile (for example `~/.zshrc` or `~/.bashrc`) and start VS Code from that shell with `code .`. This makes every Azure tool started from that environment authenticate as the agent's identity (see `KIT_CHANGELOG.md`).
2. Run `python scripts/kit_setup.py --check` (add `--copilot` for GitHub Copilot). Continue when it says "Result: ready."
3. Fully restart VS Code (close every window) and open this repository.
4. Check the MCP servers: `/mcp` in Claude Code, or **MCP: List Servers** from the Command Palette for Copilot. `fabric` must be connected, and `powerbi-modeling` too unless the lead operator declined Microsoft's EULA for it (step 7). Copilot users: type `/` in chat and confirm the `fabric-setup`, `fabric-assess-requirement` and `fabric-summarise-reference` skills are listed.
5. Ask the agent to continue setup. It runs your connection check. The `list_workspaces` result must show exactly the workspaces marked Development in `02_workspace_inventory.md`. If it shows any test or production workspace, stop and tell the lead operator: the agent's identity has more access than the access model allows. The agent then checks the `powerbi-modeling` server's identity the same way (it connects to a development semantic model, and must be refused by a test or production one). Option D: when `powerbi-modeling` first connects, a sign-in window opens; choose `<agent-account>`.

Copilot cannot block tools the way Claude Code's deny list does. See "Permissions and fences" in `docs/security_and_access.md` for what that means, and why step 9.5 matters more for Copilot users.

## 10. Check for newer releases

The MCP server versions are pinned in `scripts/mcp_servers.json`, and the date they were pinned is recorded in `KIT_CHANGELOG.md`. Check for newer releases of `ms-fabric-mcp-server` and `@microsoft/powerbi-modeling-mcp`. Do not edit `.mcp.json` by hand: `kit_setup.py` regenerates it. An upgrade is a new kit version, or a recorded change tested in development first.

## 11. Renewal

- **Options A and B.** Thirty days before your certificate expires, repeat steps 5 and 6 with a new certificate. After your IT team confirms the upload, update `AZURE_CLIENT_CERTIFICATE_PATH`, repeat step 8, and fully restart VS Code. The lead operator updates your entry in the Access model and asks IT to remove the old certificate from the app registration.
- **Option D.** Change the agent account's password and keep its multifactor authentication current as your organisation's policy requires. If you sign in to it again, repeat step 8.
- **Option E.** Nothing to renew. If the virtual machine is rebuilt, the lead operator confirms that its managed identity still has the development workspace role, and you repeat step 8.

## 12. When an operator leaves

1. The lead operator asks IT to remove the operator's access, quoting what the Access model records:
   - Option A: remove their certificate from the app registration, quoting the thumbprint.
   - Option B: disable or delete their service principal.
   - Option D: disable their agent user account and revoke its sessions.
   - Option E: remove their sign-in access to the virtual machine.
2. The lead operator removes the operator from the Access model and from Roles and approvers, with a dated note in the change log, and marks them as left in the Operators table of `agent_context/setup_status.md`.
3. The departing operator deletes `~/.fabric-agent/`, `~/.azure-fabric-agent/` and `.claude/settings.local.json` from their workstation (or their files on the virtual machine, for option E), and removes the credential variables from their environment if they set them for Copilot.

## After any change to local settings

Fully restart VS Code (close every window, not just the terminal). The agent and the MCP servers read environment variables only at start-up. After pulling a new kit version, run `python scripts/kit_setup.py` again so `.mcp.json` matches it.
