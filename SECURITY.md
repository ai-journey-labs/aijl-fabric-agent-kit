# Security policy

This policy covers the AIJL Agent Kit for Microsoft Fabric itself: its rules, permission settings, skills, setup script and workflows.

## Reporting a vulnerability

Email **community@aijourneylabs.com** with the subject "Security: AIJL Agent Kit". Please do not open a public issue or pull request for a security problem.

Include, as far as you can:

- what the problem is and why it matters;
- the kit version (from `KIT_VERSION`) and the files involved;
- the steps to reproduce it, with Claude Code or GitHub Copilot and their versions;
- whether you know of it being exploited.

Do not include credentials, tenant details or any organisation's data in your report.

## What is in scope

Problems in the kit's own files, for example:

- a gap in the rules or permission settings that lets the agent act outside its scope, such as writing to a test or production workspace, deleting an item, or running a job without asking;
- a way for the setup script, a skill or a workflow to expose a credential or write one into a repository;
- an instruction in the kit that leads an operator to configure access more widely than intended.

## What is out of scope

- Vulnerabilities in Microsoft Fabric, Power BI, the MCP servers, Claude Code, GitHub Copilot or Visual Studio Code. Report these to the vendor concerned.
- Problems in an organisation's own repository, Fabric environment or access set-up. Report these to that organisation's security team.

## Supported versions

Only the latest kit version receives fixes. Fixes are released as a new kit version and recorded in `KIT_CHANGELOG.md`.

## For organisations using the kit

This file was copied into your repository from the kit, and it covers the kit only. Report a security problem in your own Fabric environment or repository through your organisation's own process.
