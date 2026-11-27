# Troubleshooting

Common problems and what to do about them. Start with `python scripts/kit_setup.py --check` (`python3` on macOS and Linux; add `--copilot` for GitHub Copilot): it checks most of the workstation and prints no credential values, so you can paste its output to the agent.

## MCP servers do not connect

1. Run `python scripts/kit_setup.py --check` (`python3` on macOS and Linux) and fix each FAIL line. A missing `uvx` or `npx`, or a `.mcp.json` generated on another platform, stops the servers from starting.
2. If you changed `.claude/settings.local.json` or your environment variables, fully restart VS Code.
3. After pulling a new kit version, run `python scripts/kit_setup.py` to regenerate `.mcp.json`.
4. On an Intel Mac, the `powerbi-modeling` server is left out because the pinned version has no release for that platform.
5. The `powerbi-modeling` server is also left out unless `FABRIC_AGENT_PBI_EULA` is `accepted`, matching the lead operator's decision under Tooling in `01_environment_overview.md`. If the decision is declined, the server is not used.

## Authentication failures

1. Run `python scripts/kit_setup.py --check`. It reports the identity mode, the credential settings that mode needs, and which kind of identity the project Azure CLI profile is signed in as, without printing any value.
2. Check that `FABRIC_AGENT_IDENTITY` matches the identity mode in the Access model of `01_environment_overview.md`. After changing it, run `python scripts/kit_setup.py` (without `--check`) so `.mcp.json` is regenerated, then fully restart VS Code.
3. A line reported as "not used in identity mode" must be removed: it could make a tool sign in as another identity.
4. By mode:
   - `certificate`: the certificate in `AZURE_CLIENT_CERTIFICATE_PATH` must be the one IT uploaded (compare thumbprints) and must not have expired. A new service principal can take a few minutes to become usable in Fabric after it is added to the security group.
   - `user`: sign the project Azure CLI profile in again (`SETUP.md` step 8) as your agent account. If the `powerbi-modeling` sign-in window offers your personal account, choose another account and sign in as the agent account.
   - `managed-identity`: run the step 8 sign-in on the virtual machine, not on your own workstation. If the machine was rebuilt, its managed identity may have changed; ask the lead operator to check its group membership and workspace role.
5. If `list_workspaces` shows a workspace that is not marked Development, stop: see `SETUP.md` step 9.5.

## The connection check fails

- **It shows a workspace not marked Development.** Stop all Fabric work and tell the lead operator. The agent's identity has more access than the access model allows; the Fabric administrator must remove it. The agent makes no further Fabric calls until the lead operator confirms the access is corrected.
- **A development workspace is missing.** Access is not complete. Check with the Fabric administrator that the security group has the Contributor role on that workspace. A newly granted role or group membership can take a few minutes to apply.
- **The `powerbi-modeling` server connects to a test or production model.** Treat it like an extra workspace: stop, disconnect, and tell the lead operator.
- **The `powerbi-modeling` server is not listed.** See "MCP servers do not connect". If the EULA was declined, its part of the check is Not applicable.

## The agent will not do what you ask

The agent is designed to refuse in these cases. Each has a fix:

| The agent says | Why | What to do |
|---|---|---|
| Setup is not complete | Until organisation setup is complete, it works on setup only | Ask it to "set yourself up" and finish the open stages in `setup_status.md` |
| It does not know who you are, or your connection check has not passed | Fabric work needs an operator with a passed connection check | Tell it your name; complete your workstation and connection check stages |
| There is no approved plan | Rule 2 | Get the plan approved as `operator_guide.md` describes |
| The approver is not recorded | Only people marked "May approve plans" can approve | The lead operator adds them to Roles and approvers in `01_environment_overview.md` |
| The workload is not in scope | Rule 1 | The lead operator decides whether to mark it "Agent may work on this: Yes" in the organisation profile; otherwise the agent writes a recommendation |
| The request conflicts with the strategy, a policy or regulation | Rule 10 | The lead operator decides, and the decision is recorded in the review |
| It will not delete, or work in test or production | Rules 1 and 6 | It writes a recommendation or plan for a person to carry out |

Do not try to talk the agent round, and do not work around a refused or blocked tool call. Raise it with the lead operator.

## Unexpected permission prompts

- **Prompts that are expected.** In Claude Code, read-only calls run freely and everything else asks. Some reads still ask:
  - `az rest` calls other than `get`, even when they only read, such as Get Item Definition, which is a POST;
  - MCP tools that are not on the allow list in `.claude/settings.json`.

  In GitHub Copilot, at the Manual permission level, every tool call asks unless you have saved an approval.
- **A read that asks every time.** If the tool only reads, it can be added to the allow list. Changing `.claude/settings.json` is a recorded change, because it is a kit file.
- **A call that writes ran without asking.** An "always allow" choice has been saved. Remove it from your saved approvals (in Claude Code, the permission rules you added locally; in Copilot, its saved tool approvals), and tell the lead operator.
- **Claude Code has no PowerShell tool in this repository.** That is intended. The permission rules deny it, because the command rules are written for the Bash tool; on Windows the agent runs commands in Git Bash, which Git for Windows installs.
- **A call you expected to be blocked asked instead.** In Claude Code, check the deny list in `.claude/settings.json` has not been changed, and tell the lead operator. In Copilot this is expected, because Copilot has no deny list: decline the call.

## Notebook and pipeline job failures

The agent investigates read-only first, and a fix follows the normal workflow.

1. **Read the real error.** The job API gives only a generic failure reason. For a notebook, `get_notebook_driver_logs` gives the printed output and the traceback, and `get_notebook_run_details` gives the run's details. For a pipeline, `get_pipeline_activity_runs` shows which activity failed and why.
2. **Common causes:**
   - capacity: throttling, or too many Spark sessions at once;
   - the default lakehouse: a notebook pointing at another stage's lakehouse, often after a git sync or deployment, or a child notebook with a different default lakehouse from its parent;
   - `%%configure` not in the first cell, which makes pipeline runs fail;
   - parameters of the wrong type: notebook parameters can only be `int`, `float`, `bool` or `str`;
   - identity: a scheduled notebook runs as whoever set the schedule, and a pipeline-run notebook as whoever last changed the pipeline; their access may differ from the agent's;
   - a schema change upstream that a contract table did not allow for.
3. **Record it.** A failure in the environment is a bug: give the agent a bug brief, or let it record a `DF-###` or `F#` from its review. It does not fix it on the spot.

The notebook guide, `agent_context/fabric_item_guides/notebook.md`, lists more traps.

## Git and workspace sync

- **Workspace git.** Connecting a workspace to git needs the workspace Admin role, so it is a human step. Workspace commits and Update all are also human steps until service principal git access is verified in your environment (`06_platform_gotchas.md`).
- **After a sync or deployment,** check each notebook's default lakehouse and each semantic model's binding: they can still point at the previous stage.
- **`check-skills` fails a pull request.** Someone edited `.claude/skills/` without updating the Copilot copy, or edited `.github/skills/` directly. Run `python scripts/sync_skills.py` and commit both folders.
- **`git status` lists `.mcp.json` or `.claude/settings.local.json`.** They must never be committed. `kit_setup.py --check` reports whether they are ignored; do not commit them, and if one was committed, tell the lead operator. If it held credentials, treat them as exposed.
- **Line-ending changes across every file.** The repository keeps LF line endings (`.gitattributes`). Do not change git's line-ending settings for this repository; if a file shows as changed with no visible difference, it is usually line endings and can be discarded.

## GitHub Copilot

- **The skills are not listed.** Type `/` in the chat with the Fabric Developer agent selected. If `fabric-setup`, `fabric-assess-requirement` and `fabric-summarise-reference` are missing, pull `main` and check `.github/skills/` exists.
- **The MCP servers start but cannot sign in.** Copilot does not read `.claude/settings.local.json`. The identity mode and the credential variables must also be in the environment VS Code starts from (`SETUP.md` step 9.1). Run `kit_setup.py --check --copilot` to see what it finds.
- **Terminal rules are missing.** Run `python scripts/kit_setup.py --apply-copilot-rules`. If your User settings contain comments or trailing commas, add the rules from `scripts/copilot_terminal_rules.json` by hand.

## Large results

Large `list_items` results are written to a file instead of being returned in full. The agent reads the file; an apparently empty or cut-off result usually means it has not read it yet.

## Certificate expiry

Options A and B only. A certificate that has expired stops both MCP servers and the project Azure CLI profile from signing in. Renew it as `SETUP.md` step 11 describes; the expiry date is in the Identities table of the Access model.
