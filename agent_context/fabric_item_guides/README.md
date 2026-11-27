# Fabric item guides

General guidance on working with particular Microsoft Fabric item types: what each item is, what it needs, how the agent reads and changes it, how a change is checked, and the item's known traps. The guides apply to every organisation and hold no facts about yours.

This folder is a kit folder. A new kit version can add, correct or replace guides. Your organisation's own rules for an item type, and its code and documentation standards, go in [../context/07_fabric_item_rules.md](../context/07_fabric_item_rules.md), which the kit never overwrites.

## Guides

| Guide | Item types | Fabric status |
|---|---|---|
| [notebook.md](notebook.md) | Notebook | Generally available |
| [data_agent.md](data_agent.md) | Data agent | Generally available; several parts in preview |
| [fabric_app.md](fabric_app.md) | Fabric app (`AppBackend`), not org apps or workspace apps | Treated as preview |

Lakehouses, Delta tables and Direct Lake semantic models are covered by the rules in `AGENTS.md` and by [../context/06_platform_gotchas.md](../context/06_platform_gotchas.md). They have no guide yet.

## How the agent uses a guide

1. Before reviewing or planning work on an item, read its guide and its section of `07_fabric_item_rules.md`.
2. Apply them in this order:
   1. the rules in `AGENTS.md`, which always win;
   2. the organisation's rules in `07_fabric_item_rules.md` and its reference documents;
   3. the guide.

   An organisation rule may be stricter than a guide or add to it. Where it relaxes something a guide advises, follow the organisation rule and say so in the review.
3. A guide does not change what the agent may work on. If the item's workload is not marked "Agent may work on this: Yes" in the organisation profile, the agent writes a recommendation for a person (AGENTS.md rule 1).
4. If an item type has no guide, say so in the review and work from Microsoft's documentation, with the sources named.

## How far a guide can be trusted

Each guide records two dates:

- **Checked against Microsoft documentation:** when the guide was last compared with Microsoft's published documentation. Fabric changes often, and preview features change without notice.
- **Verified in a live environment:** whether the guide's statements about tools and behaviour have been confirmed in a Fabric environment, and when.

Statements not yet verified live are marked "(not yet verified live)". When a review or plan relies on one, say so. If you find a statement is wrong in your environment:

- record the observed behaviour in `06_platform_gotchas.md`, dated;
- raise it as a finding (`F#` in `05_known_defects.md`);
- do not edit the guide in place, because it is a kit file. A correction to a kit file is a recorded change (see "Kit files and organisation files" in `README.md`), and is worth reporting to the kit's maintainers.

## Adding a guide

Start from [_template/item_guide.md](_template/item_guide.md). Keep a guide general: anything true only for your organisation belongs in `07_fabric_item_rules.md`. An organisation that writes a guide for an item type the kit does not cover records it as a change to a kit file, so it can be carried forward at the next upgrade.
