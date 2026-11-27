# Business requirements

A requirement describes a business need in the business's own terms. It may be delivered by one change or by several. The agent assesses requirements before any change is planned.

## Structure

- [register.md](register.md) lists every requirement and its status, and is where `R#####` IDs are allocated.
- One folder per requirement, named `R#####_short_description`, for example `R00001_monthly_margin_report`. Each folder holds:
  - `requirement.md`, copied from [_template/requirement.md](_template/requirement.md).
  - `assessment.md`, written by the agent using the `fabric-assess-requirement` skill.
  - Any supporting material (sample reports, definitions, correspondence). Business answers that contain confidential data go in `agent_output/business_sme_returns/` (git-ignored) instead.

## How to raise a requirement

1. Pull `main`, take the next free `R#####` number in [register.md](register.md), add the row and push before writing the requirement.
2. Create the folder, copy the template and fill it in with the business owner.
3. Ask the agent to assess it. The assessment is read-only and proposes how to split the work into changes.
4. When the operator accepts the assessment, each proposed change becomes an enhancement brief (or a bug brief) linked to this requirement.

## Status values

New / Assessing / Assessed / Accepted / In delivery / Delivered / Deferred / Rejected
