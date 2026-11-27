# 03 Schema contracts

Last reviewed: [TODO: date]

## The contract

Contract tables are a published interface: semantic models, reports, downstream loads and external consumers depend on their names, columns and data types. In a medallion layout they are usually the gold tables; in any layout, they are the tables listed in the Contract table registry below. Semantic models bind to them by table name, column name and data type, so any rename, retype or drop breaks the models that read them.

- **Allowed without a migration plan:** adding a new contract table; adding a new column to an existing contract table.
- **Not allowed without a migration plan:** renaming, retyping or dropping a contract table or column; changing a column's meaning or grain; writing with `overwriteSchema`.
- A breaking change needs a separate migration plan with explicit sign-off (AGENTS.md rule 3).
- Every plan states its schema impact as "additive only" or invokes rule 3.
- Until the registry is complete, treat every table that a semantic model, report or another item reads as a contract table.

[TODO: any additions specific to this organisation, such as nullability rules or required audit columns.]

## Control tables

Tables that drive loads (watermarks, run logs, configuration).

| Table | Lakehouse | Purpose | Written by | Read by |
|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Source schema contracts

What each source system delivers, and how changes to it are notified.

| Source | Landing method | Landing location | Frequency | Schema owner | Change notification |
|---|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Contract table registry

In a medallion layout, list the gold tables here.

| Table | Lakehouse or warehouse | Grain | Key | Load pattern | Consumed by | Contract since |
|---|---|---|---|---|---|---|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO: append, merge, partition overwrite] | [TODO: models] | [TODO: date] |
