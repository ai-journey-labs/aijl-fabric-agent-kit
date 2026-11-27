# 02 Workspace inventory

Last reviewed: [TODO: date]

This file summarises the items that matter for planning. The full item-level enumeration lives in `agent_output/baselines/`. Latest baseline: [TODO: link].

## Capacities

| Capacity | SKU | Region | Workspaces | Notes |
|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Workspaces

The Stage column defines the agent's scope: it works only in workspaces marked Development (AGENTS.md rule 1).

| Workspace | ID | Stage | Agent role | Capacity | Git connected |
|---|---|---|---|---|---|
| [TODO] | [TODO] | Development | [TODO: expected Contributor, see Access model] | [TODO] | [TODO] |
| [TODO] | [TODO] | Test | None | [TODO] | [TODO] |
| [TODO] | [TODO] | Production | None | [TODO] | [TODO] |

## Lakehouses

| Lakehouse | Workspace | Layer | Schemas enabled | Shortcuts | Notes |
|---|---|---|---|---|---|
| [TODO] | [TODO] | [TODO: e.g. bronze, silver, gold] | [TODO] | [TODO: targets] | [TODO] |

## Notebooks

| Notebook | Workspace | Purpose | Reads | Writes | Parameterised | Schedule |
|---|---|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Pipelines

| Pipeline | Workspace | Purpose | Activities | Schedule | Notes |
|---|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Semantic models and their binding map

Check every model's binding after any deployment (see [06_platform_gotchas.md](06_platform_gotchas.md)).

| Model | Workspace | Storage mode | Bound to (lakehouse or SQL endpoint) | Tables | RLS | Last checked |
|---|---|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Git connection status

| Workspace | Repo and branch | Folder | Last workspace commit | Checked |
|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |
