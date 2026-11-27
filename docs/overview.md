# Overview

What the agent is, what it may and may not do, and how its work is controlled. For IT leadership, data leadership and new operators. Questions are answered in [faq_leadership.md](faq_leadership.md) and [faq_fabric_administrator.md](faq_fabric_administrator.md).

## Purpose

The kit sets up an AI agent, run in Claude Code or GitHub Copilot in Visual Studio Code, to work as a supervised senior Microsoft Fabric developer for the organisation. It reviews requests, writes plans, and, once a named person approves a plan, carries it out in the development workspaces. It documents everything it does.

The aim is to speed up careful development work without loosening control over it: every change is planned, approved by a person, reversible and recorded, and the organisation's knowledge of its Fabric environment is written down where the whole team can use it.

## What the agent does

- **Reviews.** Reads a brief or requirement, the context and the current state of the development workspaces, and writes a review: what exists, what the change touches, risks and open questions.
- **Plans.** Writes a plan with numbered steps, the items affected, the schema impact, rollback and verification, and stops until a person approves it.
- **Implements in development.** Carries out an approved plan step by step in the development workspaces, checking each step. If reality differs from the plan, it stops and asks again.
- **Documents.** Completes a change record for every change and keeps the context files current, so the next session, and the next person, starts from an accurate picture.
- **Assesses requirements.** Turns a business requirement into a read-only assessment: feasibility, affected items, risks and proposed changes.
- **Summarises reference documents.** Reads the data strategy, policies and standards, and applies them in every piece of work.
- **Sets itself up.** Walks the organisation through setup, stage by stage, and onboards each operator.

## What the agent does not do

- It does not work outside the development workspaces. For test and production it writes a plan for a person.
- It does not act without an approved plan, and it cannot approve its own plans.
- It does not delete items or landed data. A person deletes, from its written recommendation.
- It does not make breaking changes to the tables that models, reports and other consumers depend on, except through a separate migration plan with explicit sign-off.
- It does not work on Fabric workloads the organisation has not put in scope. For those it writes recommendations.
- It does not treat its own access as a security test, and it does not hold or handle passwords, keys or secrets.
- It does not settle conflicts with the organisation's strategy, policies or regulation on its own judgement. It raises them for a person to decide.

## How work is controlled

Three layers keep the agent inside its scope:

1. **Its identity.** The agent signs in as its own identity, which holds the Contributor role on the development workspaces only. Fabric itself refuses anything outside that scope. See the Identity section of [security_and_access.md](security_and_access.md).
2. **Tool permissions.** Read-only calls run freely; anything that writes, runs a job or uses capacity asks the operator first; deleting items or data is blocked. See Permissions and fences in [security_and_access.md](security_and_access.md).
3. **The operating rules and the workflow.** Ten rules in `AGENTS.md` that override any request, and a fixed workflow: review, plan, approval by a named person, implementation, change record, context update.

Every change gets a `CHG-###` ID and a review, a plan and a change record in `agent_output/`. The organisation's own Fabric environment repository holds the code history.

## Who is involved

| Role | Responsibility |
|---|---|
| Lead operator | Sets the agent up, runs it, keeps the context current, and is accountable for its use |
| Operators | Give the agent work and supervise its sessions |
| Approvers | People named in Roles and approvers who may approve plans |
| Fabric administrator | Receives requests that need more than the agent's own access, such as tenant settings and deployments beyond development |
| IT | Creates and removes the agent's identity and credentials |
| Business owners | Own requirements and confirm that results meet them |

The people in each role are recorded in Roles and approvers in `agent_context/context/01_environment_overview.md`.

## Where things live

| What | Where |
|---|---|
| The operating rules | `AGENTS.md` |
| The organisation: profile, data strategy, policies | `agent_context/organisation/` |
| The Fabric environment: architecture, workspaces, contracts, conventions, known defects, item rules | `agent_context/context/` |
| Guidance for particular Fabric item types | `agent_context/fabric_item_guides/` |
| Work given to the agent: briefs and requirements | `agent_context/enhancements/`, `bug_fixes/`, `requirements/` |
| What the agent produces: reviews, plans, change records, registers | `agent_output/` |
| Workstation setup | `SETUP.md` |
| Guides for people | `docs/` |
