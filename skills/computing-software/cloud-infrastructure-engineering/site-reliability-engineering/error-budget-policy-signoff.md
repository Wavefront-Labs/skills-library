---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.error-budget-policy-signoff
name: error-budget-policy-signoff
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, error-budget-policy, error-budget-policy-signoff, stakeholders, governance]
level: advanced
status: docs-checked
description: "Get an error budget policy approved by the product manager, development team and SRE per the Google SRE Workbook, and document approvers, dates and escalation."
sources: ["https://sre.google/workbook/error-budget-policy/", "https://sre.google/workbook/implementing-slos/", "https://sre.google/workbook/slo-document/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Getting error budget policy sign-off

**Goal:** an error budget policy that all parties will honour when the budget runs out.

## Who approves
The Workbook says getting the policy approved by all key stakeholders, the product manager, the development team and the SREs, is a good test of whether the SLOs are fit for purpose. Its three tests:
- If the SREs feel the SLO is not defensible without undue toil, they can make a case for relaxing some objectives.
- If the development team and product manager feel the extra reliability work will drop feature velocity below acceptable levels, they can argue for relaxing objectives; lowering SLOs also lowers the situations SREs respond to, which the product manager needs to understand.
- If the product manager feels the SLO will give a bad experience to a significant number of users before the policy prompts anyone to act, the SLOs are likely not tight enough.
If all three parties do not agree to enforce the policy, iterate on the SLIs and SLOs until all are happy, deciding whether you need more data, more resources or a change to the SLI or SLO.

## What the policy contains
Per the Workbook's example, sections are: service overview, goals, non-goals, SLO miss policy, outage policy, escalation policy and background. The header block lists status, author, date, reviewers, approvers, approval date and revisit date.

Example SLO miss clause from the Workbook:
> If the service has exceeded its error budget for the preceding four-week window, we will halt all changes and releases other than P0 issues or security fixes until the service is back within its SLO.

The Workbook's implementing-SLOs chapter also requires the documented policy to include authors, reviewers and approvers, approval and next-review dates, the actions on budget exhaustion, and a clear escalation path for disagreements. It notes common actions: the development team focuses exclusively on reliability until the system is within SLO, or a production freeze halts certain changes.

## Exceptions
The example policy lists cases where feature work may continue (company-wide network outage, another team's frozen dependency, out-of-scope users such as load tests, miscategorised errors with no user impact). Agree your equivalents in advance.

## Recording approval
Store the SLO document and policy where other teams and stakeholders can review them, with approvers and dates, as the Workbook advises. The example documents carry a revisit date a year after approval; the Workbook does not mandate a cadence.

## Verify
- [ ] The policy lists named approvers with approval and revisit dates.
- [ ] Product, development and SRE have each agreed to enforce it.

## Checked
Confirmed against the Workbook "Implementing SLOs" (stakeholder agreement and policy documentation sections), "Example Error Budget Policy" (sections, SLO miss wording, exceptions) and "Example SLO Document" (header block). Removed: sign-off role titles beyond the three the Workbook names, the pilot-a-quarter tip, and the unsourced "yearly" review cadence.
Method: docs-only read of cited pages, 2026-11-08
