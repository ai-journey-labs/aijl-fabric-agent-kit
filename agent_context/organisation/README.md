# Organisation context

Context about the organisation itself: who it is, what it does, why it uses Microsoft Fabric, and what its strategy and policies say. The topic files in `../context/` describe the Fabric environment; this folder describes the organisation that environment serves. The agent reads both before proposing anything.

| File | Covers | Owned by |
|---|---|---|
| [profile.md](profile.md) | Organisation, sectors, regions, regulation, data domains, how Fabric is used, workloads in scope, people, constraints, writing conventions | Organisation |
| [data_strategy.md](data_strategy.md) | Summary of the organisation's data strategy, with references to the source document | Organisation |
| [reference/](reference/README.md) | Source documents (data strategy, policies, standards) as Markdown or PDF, their summaries, and an index | Organisation (the README is a kit file) |
| `_template/` | Template for summarising a reference document | Kit |

## How this folder is filled

1. Someone who knows the organisation completes `profile.md`. The agent can do this as an interview: ask it to "set yourself up" (the profile is the first setup stage) or to "complete the organisation profile".
2. Add the data strategy and any other reference documents to `reference/` (see [reference/README.md](reference/README.md)).
3. Ask the agent to summarise them. It uses the `fabric-summarise-reference` skill, writes `data_strategy.md` or a summary next to the document, and asks the document's owner to confirm.
4. Keep it current. When the organisation, its strategy or a policy changes, update the profile or add the new document version and ask for a new summary.
