# Questions from data and technology leadership

For the CIO, the CDO, the Head of Data and sponsors deciding whether, and how, to use the agent. Each answer is short and points to where the detail lives. Start with [overview.md](overview.md) if you have not read it.

Answers describe the kit. Your organisation's own decisions are recorded in its organisation files, named in each answer.

## What it is and what it is for

### What is it?

An AI agent that works as a supervised senior Microsoft Fabric developer for your organisation. It runs in Claude Code or GitHub Copilot in Visual Studio Code, used by members of your data team (operators). It reviews requests, writes plans, carries out approved plans in your development workspaces, and documents every change. It never works in test or production, and it acts only on plans a named person has approved.

### What value does it bring?

- **Faster, more consistent preparation.** Reviews, plans and requirement assessments that follow the same structure every time, so approvers can judge them quickly.
- **A written record of the environment.** The agent keeps a current description of your workspaces, table contracts, conventions and known defects. That knowledge stays with the organisation when people change.
- **Every change documented.** A review, a plan and a change record for each change, with rollback and verification, suitable to share with leadership and auditors.
- **Your standards and strategy applied by default.** The agent reads your data strategy, policies and standards in every session and raises conflicts rather than working around them.
- **Engineers' time on harder problems.** Routine development, documentation and investigation can be prepared by the agent and checked by a person.

The kit does not promise particular savings. See "How do we know it is working?" below.

### What does it not do?

It does not touch test or production, approve its own work, delete items or data, make breaking changes to the tables your reports depend on without a separate migration plan, or work on Fabric workloads you have not put in scope. It does not replace your data team: it needs operators to direct it and approvers to sign off its plans, and it prefers solutions the team can maintain without it. The full list is in [overview.md](overview.md).

### How does it keep up with new Fabric features?

Through item guides in `agent_context/fabric_item_guides/`, which describe how to work with particular item types, such as data agents and Fabric apps, and record how far each guide has been verified. New and preview features get cautious defaults: for example, publishing a data agent and deploying a Fabric app are left to a person unless your organisation decides otherwise in `agent_context/context/07_fabric_item_rules.md`.

## Risk and accountability

### How is it kept under control?

By three layers (see "How work is controlled" in [overview.md](overview.md)):

1. its identity can reach the development workspaces only, so Fabric itself refuses anything else;
2. tool permissions make it ask before anything that writes or uses capacity, and block deletions;
3. ten operating rules and a fixed workflow: nothing is implemented without a plan approved by a named person, and every change is reversible and recorded.

### Who is accountable for what it does?

Your organisation. The agent makes mistakes, as any AI system does. Every plan and record it produces must be reviewed by a person before it is acted on, and only the people your organisation names as approvers can approve plans. The kit's rules and permissions reduce risk; they do not remove it or replace your own access controls. See the Disclaimer in the repository's `README.md`.

### What data does the AI provider see, and where does it go?

The agent sends the AI service behind the tool your operators use (Claude Code or GitHub Copilot) what it reads in order to do its work:

- the files in this repository: context, briefs, plans and records;
- the results of its calls to Fabric: item definitions, notebook code, logs, and the results of any queries or Spark statements it runs.

If your development workspaces hold real personal or confidential data, some of it can reach the AI provider. Your organisation decides which AI tool and provider to use, under which agreement, and what data the development workspaces may hold. Record that decision in "AI tools and data" in `agent_context/organisation/profile.md`, and check it with your privacy and security teams. The agent raises any request that conflicts with it (AGENTS.md rule 10).

### How does it respect our data strategy, policies and regulation?

Your profile, data strategy and reference documents are read at the start of every session. When a request conflicts with them, or with the regulation listed in your profile, the agent says so in its review and asks the lead operator to decide. It does not silently comply, and it does not overrule the request on its own judgement. The agent does not certify compliance; that remains with your organisation.

### What happens when it gets something wrong?

It works only in development, every plan has a rollback, and every step is verified as it goes. If a step does not go as planned, the agent stops and asks for approval again. Defects it finds are recorded in a findings register rather than fixed on the spot, so each fix is planned and approved in its own right. How changes then move to test and production stays with your own deployment process and the people who run it.

### What should our security team review before we adopt it?

[security_and_access.md](security_and_access.md) (identity options, permissions, credentials), [faq_fabric_administrator.md](faq_fabric_administrator.md), the permission rules in `.claude/settings.json` and the Copilot agent file in `.github/agents/`, and `SECURITY.md` for how to report a problem in the kit.

## Adoption

### What does it cost?

The kit itself is free and open source. The costs are:

- a Claude or GitHub Copilot subscription for each operator, from Anthropic or GitHub;
- Fabric capacity used by the notebook runs and Spark sessions the agent starts in development, each of which an operator approves;
- depending on the identity option: licences for dedicated agent user accounts (option D), or an Azure virtual machine (option E);
- the time of operators, approvers, IT and the Fabric administrator.

Prices are set by the vendors.

### Who do we need, and what does setup involve?

A lead operator who runs setup and is accountable for the agent's use, at least one approver, IT to create the agent's identity, and the Fabric administrator for tenant settings and workspace roles. Setup has six organisation stages (profile, reference documents, roles and approvers, environment outline, access request, initial read-only discovery) and two stages for each operator (workstation and connection check). The agent walks the lead operator through them. See "Getting started" in `README.md`.

### Claude Code or GitHub Copilot?

Both read the same rules and skills. Claude Code has the stronger controls: it can block tools outright (a deny list) and deny reads of credential files. GitHub Copilot has no deny list, so for Copilot users the rules and the operator's approvals carry more weight. The comparison is in Permissions and fences in [security_and_access.md](security_and_access.md). GitHub Copilot support has not yet been tested in a live session (see `KIT_CHANGELOG.md`).

### How mature is the kit?

It is at an early version. `KIT_CHANGELOG.md` lists what is included and the known limitations, including what has not yet been tested end to end, such as some identity options and setup on macOS and Linux. Fabric features change often, so the item guides record when each was last checked.

### How do we know it is working?

Your organisation sets its own measures. Measures that suit the kit's records include:

- time from brief to approved plan;
- how often plans are sent back, and why;
- changes that needed rollback;
- defects found and closed in the findings register;
- how much of the context is complete and current.

### Are we locked in?

No. Everything the agent produces is Markdown in your own repository, and your Fabric code stays in your own Fabric environment repository. To stop, remove the agent's identity from the workspaces; the records remain.

### Who supports the kit?

The kit is published by AI Journey Labs Pty Ltd under the Apache License 2.0, provided "as is" without warranty. New versions are released in the kit repository, and you apply them as "Upgrading the kit" in `README.md` describes. Security problems in the kit are reported as `SECURITY.md` describes.
