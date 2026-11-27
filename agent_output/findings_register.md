# Findings register

Data and logic defects found in the organisation's Fabric environment. Architecture and platform defects are recorded as `F#` in `agent_context/context/05_known_defects.md`.

## How this register works

- Each finding has a permanent `DF-###` ID, sequential and never reused. With several operators, pull `main` before allocating an ID and push the allocation before starting work.
- **This register holds status.** It is the only place a finding's status is kept; no other document states it.
- **Discovery records hold evidence.** The review or change record in which a finding was discovered holds the evidence. It is never rewritten; it is corrected only by dated notes.
- **Fix records list the DF IDs they close.** A change record that fixes a finding names the `DF-###` IDs it closes, and this register is updated in the same commit.

## Severity

High / Medium / Low. Proposed by the agent, confirmed by the lead operator.

## Status values

| Status | Meaning |
|---|---|
| Open | Confirmed, not yet addressed |
| Open (sizing needed) | Confirmed, effort or impact not yet assessed |
| Open (decision needed) | Confirmed, waiting for a business or technical decision |
| Mitigated | Impact reduced by a workaround; root cause remains |
| Fixed in development | Fix implemented and verified in development, not yet promoted |
| Fixed | Fix promoted to production and verified |
| Closed | No further action, with reason recorded |
| Tracked as F# | Reclassified as an architecture or platform finding in `05_known_defects.md` |
| Not a defect | Investigated; behaviour is correct or as designed |

## Register

| ID | Title | Severity | Status | Raised | Discovered in | Fixed by | Last updated |
|---|---|---|---|---|---|---|---|
