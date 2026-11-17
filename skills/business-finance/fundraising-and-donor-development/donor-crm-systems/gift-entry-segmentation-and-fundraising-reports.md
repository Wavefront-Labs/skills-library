---
id: business-finance.fundraising-and-donor-development.donor-crm-systems.gift-entry-segmentation-and-fundraising-reports
name: gift-entry-segmentation-and-fundraising-reports
category: business-finance
field: fundraising-and-donor-development
product: donor-crm-systems
tags: [fundraising-and-donor-development, donor-crm-systems, donor-database, donor-crm, raisers-edge, raisers-edge-nxt, blackbaud, salesforce-nonprofit, nonprofit-cloud, npsp, donorperfect, bloomerang, little-green-light, beacon, gift-entry, batch-gift-entry, hard-credit, soft-credit, deduplication, segmentation, moves-management, fundraising-reports, gift-aid, data-hygiene, finance-reconciliation]
level: practitioner
status: draft
description: "Work a donor CRM (Raiser's Edge, Salesforce Nonprofit, DonorPerfect class): clean gift entry with hard/soft credits, dedupe, appeal segments, moves tracking, finance-reconciled reports."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gift entry, segmentation and fundraising reports

**Goal:** a donor database finance trusts and fundraisers use daily. The concepts below
are shared across Raiser's Edge NXT, Salesforce Nonprofit Cloud/NPSP, DonorPerfect,
Bloomerang and similar; menu names differ, so map them to your system (and note that
Salesforce's newer Nonprofit Cloud data model differs from the older NPSP package).

## 1. Core data model (know where things live)
- **Constituent / contact**: a person; **organisation / account**: a company, foundation,
  or (in Salesforce) a household account grouping people.
- **Gift / opportunity / donation**: amount, date, type (cash, pledge, pledge payment,
  recurring, in-kind, stock), **fund** (restricted/unrestricted designation),
  **campaign** and **appeal** (the ask that produced it), payment method.
- **Relationships**: spouse, employer, board member, soft-credit links.
- **Actions / tasks / activities**: contacts and moves for moves management.

## 2. Gift entry rules (write them down as a data-entry manual)
- Enter in **batches** (by deposit or day), so batch totals can be checked against the
  bank deposit before posting.
- Search before creating: name variants, email, postcode. Duplicates are the main
  database disease.
- **Hard credit** goes to whoever legally made the gift (the cheque writer, the
  donor-advised fund, the company); **soft credit** recognises someone who influenced
  it (spouse, the employee whose company matched, the peer fundraiser). Reports must use
  hard credit for revenue totals or you'll double-count.
- **Pledges vs payments**: record the pledge once; link each payment to it. Don't enter
  payments as new gifts, or both revenue and pledge balances become wrong.
- Record restrictions exactly as the donor stated (fund code), and attach the gift
  agreement.
- Receipt and acknowledgement fields updated as letters go out; tax receipts
  per local rules (e.g. US written acknowledgment for gifts of $250+, UK Gift Aid
  declarations stored with the record).
- Recurring gifts: one recurring schedule, with each instalment posted against it.

## 3. Deduplication and hygiene
Monthly: run duplicate reports (same email, same surname + postcode), merge carefully
(keep the record with most history, check gifts and relationships move across). Apply
address updates, deceased flags and communication preferences (opt-outs) promptly;
suppress them from every mailing query, not just one. Track consent source and date for
privacy compliance.

## 4. Segmentation (queries / lists / reports)
Build saved, reusable queries rather than one-off exports:
- RFM: **recency** (last gift date), **frequency** (gifts count), **monetary** (largest or total).
- LYBUNT / SYBUNT for renewal appeals.
- First-time donors in the last 90 days (welcome series).
- Monthly donors; major-gift portfolio by assigned fundraiser.
Always exclude: deceased, do-not-contact, do-not-mail/email per channel, and anyone in
an active major-gift solicitation (handled personally).
Record the **appeal code** on the segment so incoming gifts attribute back.

## 5. Moves management in the CRM
Each prospect: assigned fundraiser, stage, next action with due date, target ask,
proposal/opportunity record with expected amount and close date. Dashboard: overdue
actions per fundraiser, pipeline by stage, asks made this quarter.

## 6. Reports that reconcile
- Monthly **reconciliation with finance**: CRM gift totals by fund and month vs the
  general ledger. Investigate every difference (timing, pledges vs cash, in-kind, refunds).
  Agree in writing who corrects what.
- Standard reports: income by campaign/appeal/fund, retention, donor counts by giving
  band, pledge receivables ageing, fundraiser activity.
- Document report definitions (e.g. "donor" = hard credit, cash gifts > $0 in period).

## Gotchas
- Free-text fields for things that should be codes (fund, appeal) wreck reporting.
- Bulk imports (event platforms, online giving) create duplicates unless matching rules are set.
- Deleting instead of adjusting gifts breaks audit trails; use reversal/adjustment entries.
- Too many custom fields nobody maintains; prune annually.

## Verify
- [ ] Batch totals match bank deposits before posting.
- [ ] Revenue reports use hard credit only.
- [ ] Pledge payments linked to pledges, not entered as new gifts.
- [ ] Mailing queries exclude deceased/opt-outs automatically.
- [ ] CRM-to-ledger reconciliation done monthly with differences explained.
