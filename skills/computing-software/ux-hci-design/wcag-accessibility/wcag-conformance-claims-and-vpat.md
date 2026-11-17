---
id: computing-software.ux-hci-design.wcag-accessibility.wcag-conformance-claims-and-vpat
name: wcag-conformance-claims-and-vpat
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [vpat-acr, conformance-claim]
level: advanced
status: draft
description: "Define scope and level in a WCAG conformance claim and document an Accessibility Conformance Report."
sources:
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/WAI/test-evaluate/conformance/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conformance
WCAG requirements: conformance level (A, AA, AAA), full pages, complete processes, accessibility-supported technologies only, non-interference.
Claim contents: date, guidelines version, level, scope (URLs), technologies relied upon.
VPAT (ITI template) yields an Accessibility Conformance Report (ACR) rating each criterion: Supports, Partially Supports, Does Not Support, Not Applicable.
Methodology: WCAG-EM (scope, explore, sample, audit, report).

## Gotchas
- An automated pass is not conformance. Third-party content in scope must be addressed.

## Verify
- [ ] Each criterion has evidence and remarks in the report.
