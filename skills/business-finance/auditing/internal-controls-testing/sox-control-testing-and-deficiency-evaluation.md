---
id: business-finance.auditing.internal-controls-testing.sox-control-testing-and-deficiency-evaluation
name: sox-control-testing-and-deficiency-evaluation
category: business-finance
field: auditing
product: internal-controls-testing
tags: [internal-controls-testing, auditing, sox, sox-404, icfr, internal-control-over-financial-reporting, coso, coso-2013, walkthrough, test-of-design, test-of-operating-effectiveness, toe, tod, sample-size, key-controls, itgc, ipe, information-produced-by-entity, control-deficiency, significant-deficiency, material-weakness, compensating-controls, remediation, as-2201]
level: advanced
status: gated
description: "Test SOX/ICFR controls end to end: walkthrough and design assessment, frequency-based sample sizes, IPE and ITGC dependencies, and grading a deficiency as deficiency, significant or material weakness."
sources: ["https://www.ecfr.gov/current/title-17/section-240.12b-2", "https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201", "https://pcaobus.org/oversight/standards/auditing-standards/details/AS1305", "https://www.coso.org/guidance-on-ic"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOX control testing and deficiency evaluation

**Goal:** conclude, with evidence a reviewer or external auditor will rely on, whether each
key control is designed to address its risk and operated throughout the period — and
grade any failure correctly.

Context: Sarbanes-Oxley s.404 requires management of US-listed companies to assess
internal control over financial reporting (ICFR), usually against COSO 2013; the external
auditor's integrated audit follows PCAOB AS 2201. Similar regimes exist elsewhere
(e.g. J-SOX). *Sample-size tables below are common practice, not mandated — use your
firm's or the external auditor's table so they can rely on your work.*

## 1. Walkthrough and test of design (TOD)
Follow one transaction from initiation to the general ledger, through the actual documents
and systems, talking to the people who perform each step. For each key control record:
- the **risk / what could go wrong** and financial statement assertion it covers;
- **who** performs it, **how often**, **what** they look at, the **precision** (threshold
  for investigation — "variances over €25k or 5%"), and the **evidence** left behind;
- whether it's manual, automated or IT-dependent manual.
A control is well designed only if, operated as described, it would catch a material
error at that precision. "Reviews the reconciliation" with no threshold is a design gap.

## 2. Test of operating effectiveness (TOE)
Illustrative sample sizes by frequency (firm-methodology figures; no standard prescribes them) (gated: unconfirmed, source is paywalled or blocked). Reason: no free official source publishes these figures, so use the table agreed with the external auditor:

| Frequency | Population per year | Typical sample |
|---|---|---|
| Annual | 1 | 1 |
| Quarterly | 4 | 2 |
| Monthly | 12 | 2–5 |
| Weekly | 52 | 5–15 |
| Daily | ~250 | 20–40 |
| Many times a day | 250+ | 25–60 |
| Automated | — | 1 per configuration, if ITGCs are effective (baseline) |

Select randomly or haphazardly across the whole period. For each item, **re-perform** or
inspect evidence that the review actually happened at the stated precision — not just a
signature. Ask: what did the reviewer find, and what did they do about it?

## 3. Dependencies people miss
- **IPE (information produced by the entity)** — reports the control relies on (an aged
  listing, an exception report). Test completeness and accuracy of the report, or the
  control tests nothing.
- **ITGCs** — access, change management and operations controls over the systems.
  Ineffective ITGCs undermine automated controls and IPE.
- **Service organisations** — get SOC 1 Type II reports, check the period and the
  complementary user entity controls you must operate.

## 4. Evaluate deficiencies
1. Describe the exception and its cause. A single exception in a small sample usually
   means the control failed unless you can show it's isolated (often by extending the sample).
2. Consider **magnitude** (how big a misstatement could result — potential, not just actual)
   and **likelihood** (reasonable possibility).
3. Grade it (definitions from SEC/PCAOB guidance):
   - **Deficiency** — (PCAOB AS 1305.01) the design or operation of a control does not
     allow management or employees, in the normal course of performing their assigned
     functions, to prevent or detect misstatements on a timely basis.
   - **Significant deficiency** — (SEC Rule 12b-2) a deficiency, or combination of
     deficiencies, in ICFR that is less severe than a material weakness yet important enough
     to merit attention by those responsible for oversight of financial reporting.
   - **Material weakness** — (SEC Rule 12b-2) a deficiency, or combination of deficiencies,
     in ICFR such that there is a reasonable possibility that a material misstatement of the
     annual or interim financial statements will not be prevented or detected on a timely basis.
4. Consider **compensating controls** — only if tested and precise enough.
5. Aggregate deficiencies affecting the same account or assertion; several minor ones can
   add up.

## 5. Remediation testing
After a fix, the control must operate for a sufficient period before retesting (e.g.
several occurrences of a monthly control) to conclude it's effective as of year-end.

## Gotchas
- Testing the control as documented in the narrative rather than as actually performed.
- Evidence created after the fact ("signed today for March") — check dates and metadata.
- Accepting management's population without checking it's complete.
- Evaluating only actual misstatements; severity depends on what *could* have happened.

## Verify
- [ ] Walkthrough documented with risk, precision, performer and evidence for each key control.
- [ ] Sample size matches frequency per the agreed table; selection spans the period.
- [ ] IPE completeness/accuracy and relevant ITGCs addressed.
- [ ] Each exception root-caused and graded with magnitude and likelihood reasoning.
- [ ] Remediated controls re-tested after enough operation.

Related: business-finance.auditing.internal-audit.writing-findings-and-tracking-remediation.

## Checked

Date checked: 2026-10-25. Jurisdiction: US (SEC, PCAOB).
Sources read: eCFR 17 CFR 240.12b-2 (material weakness and significant deficiency definitions quoted; the rule does not define "deficiency"); PCAOB AS 1305.01 via PCAOB search results (deficiency definition); COSO site (2013 Internal Control - Integrated Framework superseded the 1992 version on 15 December 2014).
Not confirmed: the sample-size table, which comes from firm methodologies; no official page publishes it, so it carries the gated marker.

Method: documentation only; no commands were run.
