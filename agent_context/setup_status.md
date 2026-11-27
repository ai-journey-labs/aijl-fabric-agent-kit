# Setup status

Progress of the agent's setup for this organisation. The agent updates this file through the `fabric-setup` skill, and the lead operator confirms each stage. Until organisation setup is complete, the agent works on setup only (see Setup and readiness in `AGENTS.md`). To start or continue, ask the agent to "set yourself up".

| Field | Value |
|---|---|
| Setup change | [TODO: CHG-### once allocated] |
| Organisation setup complete | No |
| Kit version at setup | [TODO: from `KIT_VERSION`] |

Status values: Not started / In progress / Complete / Not applicable (with the reason and the lead operator's name).

## Organisation stages

Completed once, by the lead operator.

| Stage | What it produces | Status | Completed | Confirmed by | Notes |
|---|---|---|---|---|---|
| 1. Organisation profile | `organisation/profile.md` | Not started | | | |
| 2. Reference documents | `organisation/data_strategy.md`, `organisation/reference/` summaries and index | Not started | | | |
| 3. Roles and approvers | Roles and approvers in `context/01_environment_overview.md` | Not started | | | |
| 4. Environment outline | Environments, capacity and architecture in `01`; workspace names and stages in `context/02_workspace_inventory.md` | Not started | | | |
| 5. Access request | Request to the Fabric administrator and IT in `agent_output/recommendations/`; Access model in `01`; the lead operator's decision on Microsoft's EULA for the `powerbi-modeling` server, under Tooling in `01` | Not started | | | |
| 6. Initial discovery | Baseline in `agent_output/baselines/`; inventory in `02`; Key facts in `01` | Not started | | | Needs the lead operator's connection check |

## Operators

Each operator completes the workstation and connection check stages on their own workstation. An operator uses the agent for Fabric work only once their connection check has passed.

| Operator | Agent | Platform | Identity mode | Workstation ready | Connection check | Result | Notes |
|---|---|---|---|---|---|---|---|
