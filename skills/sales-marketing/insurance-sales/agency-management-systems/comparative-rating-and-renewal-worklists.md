---
id: sales-marketing.insurance-sales.agency-management-systems.comparative-rating-and-renewal-worklists
name: comparative-rating-and-renewal-worklists
category: sales-marketing
field: insurance-sales
product: agency-management-systems
tags: [agency-management-systems, ams, applied-epic, ezlynx, vertafore, ams360, hawksoft, qq-catalyst, comparative-rater, comparative-rating, quoting-workflow, renewal-list, renewal-worklist, activities, pipeline, opportunities, commission-tracking, commission-reconciliation, download, ivans, data-hygiene, insurance-crm, insurance-agency]
level: practitioner
status: draft
description: "Run the sales side of an insurance agency system: comparative-rating quotes, renewal worklists, pipeline opportunities, and commission reconciliation, with data hygiene that makes them work."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Comparative rating and renewal worklists in agency systems

**Goal:** use the agency management system (AMS) and comparative rater so
quotes go out fast, no renewal slips through, the pipeline is visible, and
commissions you're owed actually arrive. Products vary: **Applied Epic**,
**Vertafore AMS360**, **HawkSoft**, **QQ Catalyst** (AMS); **EZLynx** (rater +
AMS); others regionally. Menu names below are generic — **status draft:** exact
screens differ by product and version; map each step to your system's equivalent.

## 1. Data hygiene first
Every report below depends on clean records:
- One client record per insured (search before creating; merge duplicates).
- Policies carry correct line of business, carrier, effective/expiration dates,
  premium and commission rate.
- **Producer** and **CSR/account manager** codes set on every policy.
- Carrier **downloads** (in the US commonly via IVANS) switched on so policy
  changes and renewals flow in; review the download exceptions queue daily.
Spend a week fixing the top 20% of premium if the data is a mess.

## 2. Comparative rating (personal lines and small commercial)
1. Start the quote from the client record (not a blank rater) so data prefills.
2. Complete the **full** question set once — drivers, vehicles, prior insurance,
   claims, property details. Incomplete answers produce quotes that change at bind.
3. Select carriers you're appointed with and that suit the risk; run the rate.
4. Review results: price **and** coverage parity (limits, deductibles, endorsements
   identical across carriers?). Raters default differently per carrier.
5. Bridge the chosen quote to the carrier portal to bind; confirm the bound
   premium matches the rated premium (reports — MVR, CLUE, credit-based scores where
   permitted — often move the price at bind).
6. Save the quote and attach to the client; log an activity.

## 3. Renewal worklists
- Build a saved report/list: policies expiring in the next 90–120 days, filtered
  by producer/CSR, with premium, carrier and last activity.
- Turn it into **activities/tasks** with due dates at 90/60/30 days (see
  pre-renewal-review-and-premium-increase-conversation). Many AMSs can
  auto-create these from a workflow template — set it up once.
- Daily: work the "due today/overdue" queue; close activities with outcome notes.
- Flag renewals with large premium change (>10–15%) from the download for a
  personal call before the notice lands.

## 4. Pipeline and opportunities
Log new-business and cross-sell **opportunities** with stage (lead, quoting,
proposed, won/lost), estimated premium, target date and loss reason. Review
weekly: stuck quotes older than 14 days get a call or close-lost.

## 5. Commission tracking
- Each month reconcile carrier commission statements against expected commission
  (policy premium × rate) in the AMS. Many systems can import statements.
- Investigate differences: wrong rate, policy not on statement, cancellation
  return commission, split-producer errors.
- Producer commission splits: set them on the policy, not in a side spreadsheet.

## Gotchas
- Raters' default coverages differ by carrier — compare like with like.
- Downloads can overwrite manual notes on some fields; keep notes in activities.
- Expiration dates edited manually without a new policy term break renewal lists.
- Credit-based insurance scoring is restricted in some states/countries — follow the rater's compliance settings.

## Verify
- [ ] Every policy has producer/CSR, correct dates, premium and commission rate.
- [ ] Download exceptions reviewed daily.
- [ ] Quotes start from the client record with full questions and coverage parity checked.
- [ ] Renewal activities auto-created at 90/60/30 days and worked daily.
- [ ] Monthly commission reconciliation completed with variances explained.
