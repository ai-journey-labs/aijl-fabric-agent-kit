# Documents

Guides for the people who work with the agent. Facts about the organisation and its environment (workspace names, people, versions, defects) live in the context files under `agent_context/context/` and in `SETUP.md`; these guides link to them rather than repeating them.

| Document | For whom | Covers |
|---|---|---|
| [overview.md](overview.md) | Leadership, IT, new operators | What the agent is, what it may and may not do, how work is controlled |
| [faq_leadership.md](faq_leadership.md) | CIO, CDO, Head of Data, sponsors | Value, risk and accountability, data and the AI provider, cost, adoption |
| [faq_fabric_administrator.md](faq_fabric_administrator.md) | The Fabric administrator, IT security | Identity, tenant settings, workspace roles, capacity, auditing, software on workstations, stopping the agent |
| [operator_guide.md](operator_guide.md) | Operators | Day-to-day use: giving work, approving plans, human steps, closing changes |
| [security_and_access.md](security_and_access.md) | IT, the Fabric administrator, operators | Identity, permissions, credentials, elevated requests, offboarding |
| [records_guide.md](records_guide.md) | Operators, reviewers | Record types, IDs, registers, templates |
| [troubleshooting.md](troubleshooting.md) | Operators | Common problems and fixes |
| [glossary.md](glossary.md) | Everyone | Terms used across the repository |
| [processes/](processes/README.md) | Operators | The organisation's own repeatable operational procedures |

## Reading order

1. New to the project: `overview.md`, then `glossary.md`.
2. Leadership deciding whether to adopt the agent: `overview.md`, then `faq_leadership.md`.
3. New operator: `SETUP.md`, then `operator_guide.md`, `records_guide.md` and `security_and_access.md`.
4. IT and the Fabric administrator: `overview.md`, then `faq_fabric_administrator.md` and `security_and_access.md`.
5. When something goes wrong: `troubleshooting.md`.

All files in `docs/` are kit files except the organisation's own process documents in `processes/` and their index, `processes/index.md` (see `README.md` at the repository root).
