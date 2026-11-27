# Reference documents

Put the organisation's own documents here when they should guide the agent's work: the data strategy, data governance or classification policies, architecture standards, coding standards, business glossaries, or similar.

## Adding a document

1. Save the document in this folder as Markdown (`.md`) or PDF (`.pdf`). Use a descriptive file name with the version or year, for example `data_strategy_2026.pdf` or `data_classification_policy_v3.md`.
2. Add a row to [index.md](index.md).
3. Commit and push, then ask the agent to summarise it.

## Formats

- **Markdown** is preferred where available. It is read in full, and changes are easy to see in git.
- **PDF** is fine. It must contain selectable text; a scanned image cannot be read reliably, so ask for a text version or export it again from the original.
- **Word, PowerPoint and other formats:** save as PDF or Markdown first.
- Keep each file under about 50 MB. GitHub warns above 50 MB and rejects files above 100 MB.

## Summaries

The agent does not read full documents every session. It reads a summary, and goes back to the source when a task needs detail.

- The data strategy is summarised in [../data_strategy.md](../data_strategy.md).
- Any other document is summarised in a file next to it, named `<document name>_summary.md` (for example `data_classification_policy_v3_summary.md`), from [../_template/reference_summary.md](../_template/reference_summary.md).
- Each summary records its source, version and status, and gives page or section references. A summary is a draft until the document's owner confirms it.
- When a new version of a document arrives, add it as a new file, mark the old one Superseded in the index, and ask for a new summary.

## Confidentiality

Documents here are committed to the organisation's own repository by default. Anyone with access to the repository can read them, and so can the agent and the AI service it runs on. Before adding a document:

- Check it can be shared with everyone who has repository access.
- Remove or redact personal data, credentials and anything the organisation classifies above the level allowed in the repository.
- If a document cannot be committed, do not add it. Record its key points in `profile.md` instead.
