# Records guide

The records the agent keeps, how they are numbered, and how they fit together. For how to give work and approve plans, see [operator_guide.md](operator_guide.md).

Records are permanent. They are written to be read later by people who were not there, including leadership and auditors, and they are corrected by dated notes, never rewritten.

## Record types

| Record | What it is | Where | Named |
|---|---|---|---|
| Enhancement brief | A request to add or improve something | `agent_context/enhancements/` | `YYYY-MM-DD_short_description.md` |
| Bug brief | A report that something is wrong | `agent_context/bug_fixes/` | `YYYY-MM-DD_short_description.md` |
| Requirement | A business need, and the agent's assessment of it | `agent_context/requirements/` | `R#####_short_description/` |
| Review | What exists, what a change touches, risks, open questions (read-only) | `agent_output/reviews/` | `CHG-###_short_description.md` |
| Plan | The steps, schema impact, rollback and verification; needs approval | `agent_output/plans/` | `CHG-###_short_description.md` |
| Change record | What was done, deviations, verification results, follow-ups | `agent_output/change_records/` | `CHG-###_short_description.md` |
| Recommendation | Advice for a person, without a change ID, such as a deletion or the access request | `agent_output/recommendations/` | `REC_YYYY-MM-DD_short_description.md` |
| Baseline | Every item, table and column in scope at a point in time | `agent_output/baselines/` | `YYYY-MM-DD_baseline_scope.md` |
| Process document | A repeatable procedure the organisation runs | `docs/processes/`, listed in `docs/processes/index.md` | `short_description.md` |

`short_description` is lower-case words joined by underscores, at most about six words.

Returns from people go in three folders that are not committed, because they can contain tenant detail or business data: `agent_output/admin_returns/` (the Fabric administrator), `agent_output/it_returns/` (IT) and `agent_output/business_sme_returns/` (business experts). The agent summarises what it needs in the relevant record, without copying sensitive values.

## IDs and allocation

| ID | For | Allocated in |
|---|---|---|
| `CHG-###` | A change, from review to close | `agent_output/change_log.md` |
| `DF-###` | A data or logic defect | `agent_output/findings_register.md` |
| `F#` | An architecture or platform defect | `agent_context/context/05_known_defects.md` |
| `R#####` | A business requirement | `agent_context/requirements/register.md` |
| `REC_YYYY-MM-DD` | A recommendation (the date is part of the file name) | No register |

IDs are sequential and never reused, even when a change is abandoned or superseded. With several operators, pull `main` before allocating an ID and push the allocation before starting the work.

## Change log

`agent_output/change_log.md` has one row for every change to the environment or to the agent, with its status and links to its documents. It is the register of briefs as well: the brief holds the request, the change log holds where it stands.

Status values, in order: Review, Planned, Awaiting approval, Approved, Implementing, Implemented, Closed. A change replaced by another is Superseded, with the replacing ID.

## Findings register

`agent_output/findings_register.md` holds every data and logic defect (`DF-###`), with its severity and status.

- **The register holds status.** It is the only place a finding's status is kept.
- **Discovery records hold evidence.** The review or change record in which a finding was found holds the evidence.
- **Fix records name what they close.** A change record that fixes a finding lists its `DF-###` IDs, and the register is updated in the same commit.
- Severity (High, Medium, Low) is proposed by the agent and confirmed by the lead operator.

Architecture and platform defects, such as a design that cannot scale or a platform limitation, are `F#` in `05_known_defects.md`, with the remediation sequence and the approaches already rejected.

A defect found in the middle of another change is recorded, never fixed on the spot (AGENTS.md rule 7). It gets its own ID and, if it needs fixing, its own change.

## Templates

| Template | For |
|---|---|
| `agent_output/_templates/review_template.md` | Review records |
| `agent_output/_templates/plan_template.md` | Plans |
| `agent_output/_templates/change_record_template.md` | Change records |
| `agent_output/_templates/access_request_template.md` | The access request at setup |
| `agent_context/enhancements/_template/enhancement_brief.md` | Enhancement briefs |
| `agent_context/bug_fixes/_template/bug_brief.md` | Bug briefs |
| `agent_context/requirements/_template/requirement.md` | Requirements |
| `agent_context/organisation/_template/reference_summary.md` | Summaries of reference documents |
| `agent_context/fabric_item_guides/_template/item_guide.md` | Item guides |
| `docs/processes/_template.md` | Process documents |

The templates are kit files. If your organisation needs a different template, change it through a recorded change, so it can be carried forward when the kit is upgraded.

## Lifecycle of a change

1. **Brief.** An operator commits a brief, or a requirement's assessment proposes a change.
2. **Allocate.** The agent allocates the next `CHG-###` in the change log (status Review) and writes it at the top of the brief.
3. **Review.** The review record is written in `reviews/`.
4. **Plan.** The plan is written in `plans/` (status Awaiting approval).
5. **Approve.** A named approver sets the plan's Status to "Approved by [name] on [date]" and commits it under their own name; the change log then says Approved.
6. **Implement.** The agent carries out the plan in development (Implementing).
7. **Record.** The change record is written in `change_records/`, the topic files are updated, the findings register is updated if the change closes findings, and both repositories are committed (Implemented).
8. **Close.** The lead operator accepts the change (Closed).

## Correcting a record

Records are not rewritten. To correct one:

1. Add a dated note at the end, under a heading "Corrections", saying what was wrong, what is right, and who confirmed it. For example: "27 Nov 2026: the row count in Verification results was for the test run, not the final run. Final run: 12,408 rows. Confirmed by [name]."
2. If the correction changes a finding's status, change it in the findings register only.
3. If the correction changes a fact in the context, update the topic file as well, with the date.

A plan that changes after approval is not corrected in place: the agent updates it, sets it back to Awaiting approval, and records the reason in the plan, and it needs approval again.
