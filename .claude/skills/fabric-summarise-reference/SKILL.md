---
name: fabric-summarise-reference
description: Summarise an organisation document held in agent_context/organisation/reference/ (data strategy, policy, standard, glossary; Markdown or PDF) into a referenced summary the agent can apply in every session. Use when an operator adds or updates a reference document, asks to summarise or digest the data strategy or a policy, or a summary's status is Not started.
---

# Summarise a reference document

A summary lets the agent apply an organisation document in every session without reading it in full. The summary must be faithful to the source: it records what the document says, with references, and keeps the agent's own interpretation separate. This is a context task: it changes nothing in Fabric and needs no change ID. All rules in `AGENTS.md` apply.

## Inputs

- The document's file name in `agent_context/organisation/reference/`. If the operator gives none, list the rows in `reference/index.md` whose summary status is Not started, and ask which one.

## Steps

1. **Locate.** Find the file and its row in `reference/index.md`. If the file has no row, add one first. If the file does not exist, stop and say so.
2. **Choose the output.**
   - The data strategy goes in `agent_context/organisation/data_strategy.md`, following the sections already in that file.
   - Any other document goes in `reference/<document name>_summary.md`, from `agent_context/organisation/_template/reference_summary.md`.
   - If a summary already exists for an earlier version, write the new one and mark the old one Superseded; do not edit the old summary in place.
3. **Read the whole document.**
   - Markdown: read it in full.
   - PDF: find the page count, then read it in ranges of at most 20 pages until every page has been read. Record the page count in the summary.
   - If pages come back empty or garbled (a scanned image), stop and ask for a version with selectable text. Do not summarise a partial read.
4. **Write the summary.**
   - State what the document says, in its own terms. Give a page or section reference for every point.
   - Do not add facts, fill gaps or soften requirements. If the document is unclear, say so under Gaps and tensions.
   - Keep "Implications for the agent" clearly separate, and word each one as an interpretation.
   - Aim for a summary that can be read in five minutes. Detail stays in the source.
5. **Compare with the current context.** Read `agent_context/organisation/profile.md`, `agent_context/context/01_environment_overview.md`, `05_known_defects.md` and any other confirmed summaries. Record each difference between the document and the current environment, or between documents, under Gaps and tensions. Do not raise findings or change anything because of them; they are questions for the owner.
6. **Update the index.** Set the row's summary link and status to Draft.
7. **Ask for confirmation.** Tell the operator who the document owner is and list what the owner should check: the key points, the implications for the agent, and each gap or tension. When the owner confirms, set the status to "Confirmed by [name] on [date]" in the summary and the index.
8. **Commit.** Use a message such as "Context: summarise data_strategy_2026.pdf".

## Rules

- Until a summary is confirmed, any review or plan that relies on it says that it relies on a draft summary.
- Never copy personal data, credentials or text marked confidential into a summary. Refer to the page instead.
- If the document conflicts with a rule in `AGENTS.md`, the rule wins; record the conflict under Gaps and tensions and raise it with the lead operator.
- Follow the writing style in `AGENTS.md`, and the English variant set in `profile.md`.
