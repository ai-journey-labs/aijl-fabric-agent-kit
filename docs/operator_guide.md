# Operator guide

How to work with the agent day to day, once your workstation is set up and your connection check has passed (`SETUP.md`). For what the records are and how they are numbered, see [records_guide.md](records_guide.md). For problems, see [troubleshooting.md](troubleshooting.md).

## Starting a session

1. Pull `main`, so you start from the latest context and records.
2. Open the repository in VS Code and start Claude Code, or select the Fabric Developer agent in GitHub Copilot Chat. Copilot users work at the Manual permission level.
3. Tell the agent who you are if it asks. It does Fabric work only for an operator whose connection check has passed in `agent_context/setup_status.md`.
4. Say what you want to work on: a brief, a requirement, a plan to continue, or a question.

At the start of every session the agent reads its rules, the setup status, the organisation profile, the data strategy summary and the context index. It then reads the topic files and item guides the task needs. You do not need to point it to them.

If setup is not complete, the agent works on setup only (ask it to "set yourself up"). Answering questions about the kit is always allowed.

## Giving work

| You want | Give the agent | Where |
|---|---|---|
| Something new or improved: a table, column, measure, notebook, pipeline | An enhancement brief | `agent_context/enhancements/`, from `_template/` |
| Something fixed: a failing job, a wrong number, missing data | A bug brief | `agent_context/bug_fixes/`, from `_template/` |
| A business need to be scoped before anyone builds it | A requirement | `agent_context/requirements/R#####_short_description/`, from `_template/` |
| A document summarised: the data strategy, a policy, a standard | The document | `agent_context/organisation/reference/` |
| An answer about the environment or the kit | A question in the chat | |

Write briefs in plain terms, with acceptance criteria someone can check. Write "Unknown" rather than leaving a section blank. Commit and push the brief, then ask the agent to review it. A conversation is not a brief: anything the agent is to change needs a brief, so that the change has a record.

## The workflow from your side

| Step | The agent | You |
|---|---|---|
| 1. Review | Allocates a `CHG-###`, reads the brief, the context and the current state in development, and writes a review record. Read-only | Read the review. Answer its open questions, or get answers from the people it names |
| 2. Plan | Writes a plan: steps, affected items, schema impact, rollback, verification, human steps. Then stops. Read-only | Read the plan, then get it approved (see below) |
| 3. Implement | Carries out the approved plan in development, one step at a time, checking each | Approve each tool call it asks for, after checking it matches the plan step (see below) |
| 4. Document | Completes the change record: what was done, deviations, verification results, follow-ups | Read it |
| 5. Update context | Updates the topic files and the change log, and commits | Push, and commit the Fabric environment repo if that is a human step |

If what the agent finds during implementation differs from the plan, it stops, updates the plan and asks for approval again. That is the workflow working, not a failure.

## Approving a plan

Only the lead operator and the people marked "May approve plans" in Roles and approvers (`agent_context/context/01_environment_overview.md`) can approve a plan (AGENTS.md rule 2). The agent never approves its own plan.

Before approving, check that:

- the steps do what the brief asks, and nothing more;
- every step runs in development; anything for test or production is a human step for the people who run it;
- the schema contract statement says "additive only", or points to a separate migration plan with sign-off;
- any rename is covered in full: every reference, verification and rollback;
- the rollback is realistic, and any step marked not reversible has its own sign-off;
- the verification would show the change works, including a Viewer-only test principal check for anything about security;
- the human steps are clear enough to hand to the person named.

To approve, the approver changes the plan's Status to "Approved by [name] on [date]" and commits it under their own name. The git history is the evidence of who approved it and when, so every approver needs to be able to commit to this repository.

The agent checks the name against Roles and approvers. If it does not match, the plan stays not approved and the agent says why. The agent then sets the change log status to Approved.

## Answering requests to act

During implementation the agent asks before every call that writes, runs a job, starts a Spark session or statement, runs an SQL statement, renames or removes part of an item, or calls `az rest` with a method other than `get`. Before you approve:

- check the call belongs to the plan step the agent names;
- read what it will do: the item, the workspace, the code or statement;
- check the workspace is a development workspace;
- decline anything you do not understand, and ask the agent to explain.

Do not choose "always allow" for a tool that writes, runs jobs or uses capacity, and Copilot users never switch to Assisted or Allow all. Declining is safe: the agent stops and asks how to proceed.

Some things the agent will not do even if you approve them: deleting items or landed data, working outside development, and reading credential files. In Claude Code these are blocked; in GitHub Copilot they are forbidden by the agent's instructions.

## Human steps

Anything the agent cannot or must not do appears in the plan's Human steps, as exact numbered instructions for a named person:

- tenant, capacity and workspace settings, for the Fabric administrator;
- deployments to test and production, for the people who run them;
- connecting a workspace to git, workspace commits and Update all;
- deletions, from a written recommendation in `agent_output/recommendations/`;
- anything needing more than the agent's Contributor access.

Send each instruction to the person named, and tell the agent when it is done and what came back. Output that contains tenant detail goes in `agent_output/admin_returns/` or `agent_output/it_returns/`, which are not committed. The agent records what it needs without copying sensitive values.

## Closing a change

1. Read the change record. Check the verification results meet the brief's acceptance criteria, and that the deviations, if any, were approved.
2. Check the follow-ups: new findings, reviews or recommendations raised during the change.
3. Check the context updates are listed and committed, and the Fabric environment repo is committed.
4. If you are the lead operator and are satisfied, tell the agent the change is accepted. It sets the status to Closed in the change log.

## Working alongside other operators

- Pull `main` before you start, and before allocating any ID (`CHG-###`, `DF-###`, `R#####`). Push the allocation straight away, before doing the work, so two operators never take the same number.
- If your repository requires pull requests on `main`, "push" here and in the agent's rules means a small pull request, merged before the work starts. An ID is allocated once its row is on `main`, and a plan is approved once the approver's commit is on `main`.
- One change belongs to one operator's session at a time. To hand over, commit and push, and tell the next operator which step it has reached.
- Keep changes small, so reviews and approvals stay quick.
- If two changes touch the same item, finish and close one before implementing the other, or say in the second plan how they interact.

## When to escalate

Tell the lead operator, and stop the Fabric work until they decide, when:

- the connection check shows a workspace that is not marked Development, or the agent can reach something it should not;
- the agent reports a conflict with the data strategy, a policy or regulation (rule 10);
- a change would break a contract table, or needs a migration plan;
- a step fails in a way the plan's rollback does not cover;
- you suspect a credential has been exposed; tell IT as well, so it can be revoked;
- the agent does something you did not expect, or does not stop when it should.

Problems in the kit itself are reported as `SECURITY.md` describes.
