---
id: law-government.tax-law.corporate-tax-structuring.reorganisation-step-plans-and-tax-opinions
name: reorganisation-step-plans-and-tax-opinions
category: law-government
field: tax-law
product: corporate-tax-structuring
tags: [corporate-tax-structuring, tax-law, step-plan, steps-memo, reorganisation, reorganization, tax-free-reorganization, section-368, section-351, spin-off, section-355, merger, demerger, hive-down, share-for-share-exchange, tax-opinion, should-opinion, will-opinion, more-likely-than-not, step-transaction-doctrine, business-purpose, continuity-of-interest, gaar, anti-avoidance, substantial-shareholding-exemption, group-relief, tax-clearance, ruling-request]
level: advanced
status: docs-checked
description: "Drafting a corporate reorganisation step plan and supporting tax opinion: mapping steps, testing each against statutory and anti-avoidance rules, and setting opinion levels."
sources: ["https://www.law.cornell.edu/uscode/text/26/351", "https://www.law.cornell.edu/uscode/text/26/368", "https://www.law.cornell.edu/uscode/text/26/6662", "https://www.irs.gov/tax-professionals/circular-230-tax-professionals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reorganisation step plans and tax opinions

**Goal:** turn a commercial objective (separate a business, merge two groups, move a
holding company) into an ordered list of legal steps whose tax result can be stated with
a defined level of confidence, and document that result in an opinion. Jurisdiction: US federal
(IRC subchapter C), checked current on 2026-10-24; UK and other concepts are illustrative only, and
reorganisation reliefs differ by country, so map each step to the local statute. Not tax advice; a
qualified tax adviser must review any real plan.

## 1. Fix the facts and the target end state
- Obtain current and target **structure charts**: entities, jurisdictions, tax
  classification, ownership percentages, tax basis/base cost, E&P or reserves, debt.
- Record the business purpose in the client's own words; many reliefs and anti-avoidance
  rules turn on it (business purpose, continuity of interest/enterprise, "bona fide
  commercial reasons").
- Identify hard constraints: lender consents, regulatory approvals, employee transfer
  rules, stamp/transfer taxes, local corporate law (distributable reserves, solvency
  statements).

## 2. Draft the step plan
Write a numbered table, one legal act per row:

| # | Date | Entity | Legal step (document) | Corporate law basis | Tax treatment | Authority | Risk |
|---|---|---|---|---|---|---|---|
| 1 | D | HoldCo | Contribute shares of Sub A to NewCo for NewCo shares (share contribution agreement) | Board/shareholder resolutions | Non-recognition, if control test met (US §351: control immediately after the exchange, 80% under §368(c)) | US §351 (confirm the relief in other countries) | Low |

- One document per step; no "and then" steps that hide two transactions.
- Show the tax basis and holding period carried through each row.
- Mark steps that depend on another step's completion and ask whether the **step-transaction
  doctrine** (or a GAAR) would collapse them; if they would, analyse the collapsed version too.
- Include post-closing steps (liquidations, check-the-box elections, intra-group debt
  settlement) and their filing deadlines.

## 3. Test each step
For every row: statutory requirements met? anti-avoidance rules (GAAR, specific
anti-avoidance, controlled-foreign-company, hybrid-mismatch, interest limitation)?
transfer/stamp taxes? exit or de-grouping charges? withholding on distributions?
reporting obligations (mandatory-disclosure regimes for reportable transactions — check each jurisdiction's current regime)?
Prefer the simplest route that achieves the end state; every extra step is a new risk.

## 4. Decide whether to seek a ruling
A private ruling or clearance (see the tax-ruling-and-guidance-practice skill) is worth
it when the tax at stake is large and the law unsettled. Build the ruling timetable into
the step plan; some authorities will not rule on certain issues.

## 5. Write the opinion
- **Opinion levels** (US convention, roughly): *will* (very high confidence), *should*
  (high), *more likely than not* (>50%), *substantial authority*, *reasonable basis*.
  In the US the accuracy-related penalty is 20% of the underpayment (§6662(a)) and the understatement is reduced for
  items with substantial authority, or adequately disclosed with a reasonable basis (§6662(d)(2)(B)); other
  jurisdictions differ.
- Structure: question, conclusion with level, facts relied on, **representations**
  (obtained in a signed certificate), assumptions, analysis, limitations, reliance
  (who may rely; no third parties without a reliance letter).
- Tie every fact in the opinion to a document or representation; never assume a fact
  that the client can confirm.
- Comply with the professional rules governing practice before the tax authority (US: Treasury Department Circular 230).

## Gotchas
- A late commercial change (cash added to a share exchange) can break continuity tests;
  re-run the analysis on every draft of the deal documents.
- Steps executed out of order or on the same day without board minutes showing sequence.
- Forgetting non-income taxes: stamp duty, real-property transfer taxes, VAT on asset moves.
- Opinions copied from precedent with stale law.

## Verify
- [ ] Every step is one legal act with its own document and corporate approval.
- [ ] Collapsed (step-transaction) version analysed.
- [ ] Representations certificate signed and matched to opinion assumptions.
- [ ] Disclosure/reporting obligations and post-closing filings diaried.
- [ ] Executed documents checked against the final step plan after closing.

## Checked

Checked 2026-10-24. Jurisdiction: US federal income tax (IRC), other systems illustrative. Sources: Cornell LII text of 26 U.S.C. §§351, 368 and 6662; IRS Circular 230 page.

Confirmed: §351 non-recognition with control immediately after the exchange and the 80% control definition in §368(c); the 20% accuracy-related penalty and the substantial authority and reasonable basis reductions in §6662; Circular 230 as the Treasury rules on practice before the IRS. Removed as unconfirmed: the UK share-for-share relief reference, the EU DAC6 hallmark reference, and the claim that Circular 230 sets written-advice standards. The opinion-level vocabulary is a professional convention, not a statutory scale.

Method: documentation only; no commands were run.
