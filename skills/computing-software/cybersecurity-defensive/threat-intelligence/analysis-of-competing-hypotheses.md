---
id: computing-software.cybersecurity-defensive.threat-intelligence.analysis-of-competing-hypotheses
name: analysis-of-competing-hypotheses
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [intelligence-lifecycle, analysis-of-competing-hypotheses, ach, structured-analytic-techniques, cognitive-bias, attribution-analysis]
level: advanced
status: draft
description: "Apply analysis of competing hypotheses to CTI questions such as attribution or intrusion cause: list hypotheses, score evidence for diagnosticity, refute rather than confirm, and record sensitivity."
sources: ["Richards J. Heuer Jr. - Psychology of Intelligence Analysis (CIA Center for the Study of Intelligence)", "US Government Tradecraft Primer - Structured Analytic Techniques", "Heuer and Pherson - Structured Analytic Techniques for Intelligence Analysis"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Analysis of competing hypotheses (ACH)

**Goal:** reach a judgment that survives scrutiny by systematically trying to disprove alternatives instead of confirming a favourite.

## Steps (Heuer)
1. **Hypotheses:** brainstorm all reasonable ones, including the uncomfortable ("insider", "red team test", "commodity malware, not targeted").
2. **Evidence and arguments:** list everything significant, including absence of expected evidence and assumptions.
3. **Matrix:** for each evidence item vs hypothesis mark Consistent (C), Inconsistent (I), or Not applicable (N/A). Weight credibility/relevance.
4. **Diagnosticity:** evidence consistent with all hypotheses is not diagnostic - it does not help choose. Focus on items that distinguish.
5. **Refine:** merge/split hypotheses; delete non-diagnostic evidence from consideration (keep it recorded).
6. **Tentative conclusion:** the hypothesis with the **fewest inconsistencies** is most likely, not the one with most consistencies.
7. **Sensitivity:** which few items drive the conclusion? What if one is wrong or deceptive (false flags, shared tooling)?
8. **Report:** conclusion with confidence, alternatives, and why they were rejected.
9. **Milestones:** indicators that would change the judgment; revisit when they appear.

## CTI example
Question: who is behind intrusion X? Hypotheses: Actor A, Actor B (shares tooling), unknown criminal, insider. Evidence: infrastructure overlap with A (moderately diagnostic: infrastructure reuse is common), custom loader only seen with A (high), working hours UTC+3 (low, easily faked), ransom note absent (inconsistent with criminal hypothesis).

## Tools
Spreadsheet works; open-source ACH tools exist. Do it as a team to expose different assumptions.

## Gotchas
- Listing only evidence you already gathered to support one hypothesis.
- Treating ACH output as a calculation; it structures judgment, it does not replace it.

## Verify
- [ ] At least 3 hypotheses including a null/benign one.
- [ ] Report states which evidence was most diagnostic and what would change the conclusion.
