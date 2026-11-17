---
id: computing-software.web-development.web-accessibility.wcag-em-sampling-and-audit-reports
name: wcag-em-sampling-and-audit-reports
category: computing-software
field: web-development
product: web-accessibility
tags: [accessibility-testing, wcag-em, audit-report, accessibility-audit, conformance, accessibility-audit-report]
level: practitioner
status: docs-checked
description: "Running a structured accessibility audit with WCAG-EM: defining scope, exploring the site, sampling representatively, auditing per criterion, and writing an actionable report."
sources:
  - https://www.w3.org/TR/WCAG-EM/
  - https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/
  - https://www.w3.org/WAI/eval/report-tool/
  - https://www.w3.org/WAI/WCAG22/quickref/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WCAG-EM sampling and audit reports

WCAG-EM (WCAG Evaluation Methodology; version 2.0 is a W3C Group Note dated 23 July 2026, building on the 2014 WCAG-EM 1.0 Note) gives a repeatable 5-step process: define scope, explore, select a sample, evaluate, report.

## 1. Define scope
- Target: WCAG 2.2 level AA (usually), which pages/states/subdomains, third-party content in or out, accessibility-supported technologies (browsers + AT combos, e.g. NVDA+Chrome, JAWS+Chrome, VoiceOver iOS Safari, TalkBack Chrome).
- Agree goal: conformance claim, gap analysis, or regression check.

## 2. Explore
Identify common pages (home, login, search, contact), essential functionality (checkout, account creation), page types/templates, varieties of content (forms, tables, media, maps, PDFs), technologies (frameworks, embedded widgets) and states (errors, logged in, empty states).

## 3. Select a sample
- **Structured sample**: one of each template/component type + all common pages + every step of complete processes (all steps of checkout, not just the first).
- **Random sample**: ~10% of the structured sample size, chosen randomly from the rest, to check that the structured sample is representative.

## 4. Audit
For each sample item, evaluate every success criterion: automated scan (axe) + manual checks (keyboard, zoom/reflow, contrast, screen reader, content review). Record per criterion: pass / fail / not present, with location, evidence (screenshot, snippet), user impact, and recommended fix. Complete processes are evaluated as a whole.

## 5. Report
- Executive summary: scope, methodology, overall result, top risks.
- Results by criterion and by page; severity rating (blocker / high / medium / low) based on user impact and frequency.
- Each issue: WCAG SC, where, how to reproduce, who's affected, how to fix (code example), and whether it's a global component issue (fix once).
- W3C's WCAG-EM Report Tool (version 4.1.0 at the check date) helps build the report.
- Date and version tested - conformance is a snapshot.

## Tips
Group duplicates by component (one header bug isn't 40 issues). Re-test after fixes on the same sample. Include people with disabilities for usability validation (WCAG-EM is conformance, not usability).

## Verify
Report lets a developer reproduce and fix each issue without the auditor; re-test results are traceable to the original issue IDs.

## Checked

- Date: 2026-10-26. Documentation: WCAG-EM 2.0 (W3C Group Note, 23 July 2026), W3C WCAG-EM Report Tool page.
- Confirmed: the five steps (define scope, explore, select a representative sample, evaluate, report); the random sample is 10% of the structured sample set; the baseline of accessibility-supported technologies is agreed with the commissioner in step 1; WCAG-EM 2.0 points to WCAG 2.2 conformance requirements.
- Removed (no documentation found): the 15-40 page figure and the JSON/HTML output claim.
Method: documentation only; no commands were run.