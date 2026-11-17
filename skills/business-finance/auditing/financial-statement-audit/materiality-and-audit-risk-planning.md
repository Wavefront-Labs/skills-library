---
id: business-finance.auditing.financial-statement-audit.materiality-and-audit-risk-planning
name: materiality-and-audit-risk-planning
category: business-finance
field: auditing
product: financial-statement-audit
tags: [financial-statement-audit, auditing, external-audit, materiality, overall-materiality, performance-materiality, clearly-trivial, audit-risk-model, inherent-risk, control-risk, detection-risk, significant-risk, risk-of-material-misstatement, revenue-recognition-fraud-risk, management-override, isa-320, isa-315, isa-330, as-2105, as-2110, audit-planning, audit-strategy, pcaob, aicpa]
level: advanced
status: gated
description: "Plan an external audit: set overall and performance materiality from a justified benchmark, assess risks of material misstatement by assertion, and link each significant risk to a planned response."
sources: ["https://pcaobus.org/oversight/standards/auditing-standards/details/AS2401", "https://pcaobus.org/oversight/standards/auditing-standards/details/AS2301", "https://www.iaasb.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Materiality and audit-risk planning — decide what matters before testing anything

**Goal:** turn "audit the financial statements" into a targeted plan: a materiality
figure you can defend, a short list of where misstatement is most likely, and a planned
response for each. Everything later (sample sizes, which accounts to test) flows from this.

Standards referenced: ISA 315 (risk assessment), ISA 320 (materiality), ISA 330 (responses);
US public-company equivalents are PCAOB AS 2110 (identifying and assessing risks; PCAOB lists an amended version with a later effective date, so check which applies to your audit period) / AS 2105 (materiality) / AS 2301 (responses), and AICPA AU-C for US
private entities. Firm methodologies add their own percentages — **follow your firm's
manual where it differs from the ranges below.**

## 1. Overall materiality
Pick a benchmark that users of the statements actually care about, then a percentage.
Illustrative ranges from firm practice; ISA 320 leaves the percentage to professional judgement (gated: unconfirmed, source is paywalled or blocked). Reason: the IAASB standard text could not be retrieved, and these figures come from firm methodologies:

| Entity type | Benchmark | Typical % |
|---|---|---|
| Profit-oriented, stable profits | Profit before tax (from continuing operations) | ~5% |
| Loss-making / volatile profit | Revenue or total expenses | ~0.5–1% (revenue) |
| Asset-heavy / investment entity | Total assets or net assets | ~1–2% |
| Not-for-profit / public sector | Total expenses or revenue | ~0.5–2% |

Normalise the benchmark for one-offs (a big impairment, a disposal gain). Document **why**
this benchmark and this percentage — reviewers challenge the choice, not the arithmetic.

## 2. Performance materiality and clearly trivial
- **Performance materiality** is set below overall materiality to leave headroom for
  undetected and uncorrected misstatements — often **50–75%** of overall materiality (gated: unconfirmed, source is paywalled or blocked) (a firm-methodology range, not set by the standards):
  lower end for a first-year audit, weak controls or a history of adjustments.
- **Clearly trivial threshold** — misstatements below it aren't accumulated; often **~3–5%** of overall materiality (gated: unconfirmed, source is paywalled or blocked) (a firm-methodology range).
- Set lower **specific materiality** for sensitive items (related-party transactions,
  directors' pay) where users care about smaller amounts.

## 3. Assess risks of material misstatement
Understand the entity: business model, industry, IT environment, controls, prior-year
findings, analytical review of this year's numbers vs last year and budget. Then, for each
significant account, identify risks at the **assertion** level (existence/occurrence,
completeness, accuracy, cut-off, valuation, rights and obligations, presentation).

- **Inherent risk** — how susceptible the item is (estimates, judgement, complex
  transactions, unusual volume changes).
- **Control risk** — whether controls would prevent or detect it (only reduce your work for
  controls you plan to test).
- **Significant risks** need a specific response. Two are **presumed** by the standards:
  **fraud in revenue recognition** (rebuttable, with documented reasons) and **management
  override of controls** (not rebuttable) — the latter always requires testing of journal entries and other adjustments (PCAOB AS 2401.58; ISA 240).

## 4. Link risks to responses
Build a table: risk → assertion → planned procedure → nature, timing, extent. Higher risk
→ more persuasive evidence (external confirmations over internal documents), testing
closer to year-end, bigger samples. Every significant risk must have substantive
procedures specifically responsive to it; analytics alone are rarely enough.

## Gotchas
- Using last year's materiality without re-checking the benchmark after a big change in results.
- Revisiting materiality at completion: if actual results differ markedly from the
  planning figures, recompute and assess whether testing done is still sufficient.
- Generic risk lists ("revenue may be misstated") don't satisfy reviewers — name the
  mechanism (e.g. "year-end bill-and-hold shipments recorded early").
- Group audits: component materiality must be lower than group materiality.
- Communicate the planned scope and significant risks to those charged with governance.

## Verify
- [ ] Benchmark, percentage and normalisations documented with a reason.
- [ ] Performance materiality and clearly trivial threshold set and justified.
- [ ] Risks recorded at assertion level, with the two presumed risks addressed.
- [ ] Each significant risk mapped to specific substantive procedures.
- [ ] Planning reviewed by the engagement partner before fieldwork.

Related: business-finance.auditing.audit-analytics (journal-entry testing for management override).

## Checked

Date checked: 2026-10-25. Jurisdiction: International (IAASB ISAs) and US public companies (PCAOB).
Sources read: PCAOB standards index and AS 2401 page via search results (AS 2105, AS 2110, AS 2301 and AS 2401 are current standards with the titles used; AS 2401.58 covers examining journal entries; revenue recognition fraud risk is a rebuttable presumption).
Not confirmed: the materiality percentage ranges, performance materiality and clearly trivial ranges. A search of secondary sources found that ISA 320 does not fix a formula, but the IAASB text itself was not retrievable, so those figures carry the gated marker.

Method: documentation only; no commands were run.
