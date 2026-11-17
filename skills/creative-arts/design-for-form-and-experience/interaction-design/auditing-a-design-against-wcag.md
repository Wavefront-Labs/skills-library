---
id: creative-arts.design-for-form-and-experience.interaction-design.auditing-a-design-against-wcag
name: auditing-a-design-against-wcag
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [accessibility-audit, wcag-audit, wcag-em, design-accessibility-review, conformance-evaluation, accessibility-checklist]
level: advanced
status: draft
description: "Audit a design against WCAG 2.2: scope and conformance target, sample pages and states, test with tools and assistive technology, rate issues and report."
sources:
  - "W3C WCAG 2.2 (w3.org/TR/WCAG22)"
  - "W3C WCAG-EM Website Accessibility Conformance Evaluation Methodology (w3.org/TR/WCAG-EM)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# WCAG audit of a design

WCAG 2.2 is organised under four principles (perceivable, operable, understandable, robust) with success criteria at levels A, AA and AAA. Most legal and procurement requirements point to AA. WCAG-EM describes an evaluation process: define scope, explore, select a sample, audit, report.

## Steps
1. **Set scope and target:** product areas, platforms, conformance level (typically WCAG 2.2 AA), and any laws or contracts (check with legal; not covered here).
2. **Explore and sample:** list templates, key flows (sign-up, checkout), components, states, and responsive views; pick representative pages.
3. **Audit design files first** for what can be judged without code: contrast (see `...interaction-design.checking-colour-contrast`), text size and spacing, target size (see `...interaction-design.sizing-touch-targets`), focus states, reading order, error patterns, motion, alt text plans, headings, link text, colour-only information, reflow at 320 px and zoom.
4. **Audit the build** with automated tools (axe, WAVE, Lighthouse find only a portion of issues), manual keyboard testing, and screen readers; test zoom and text spacing, and reduced motion.
5. **Record each issue:** criterion, location, evidence, user impact, severity, suggested fix, owner.
6. **Report:** a conformance statement per criterion (pass, fail, not applicable), a prioritised list, and a plan; retest after fixes.
7. **Include disabled users** in testing where possible; automated and checklist audits do not equal usability.

## Verify
- [ ] Every issue cites a success criterion and evidence.
- [ ] Both tools and manual tests were used.
- [ ] A retest date is set.
