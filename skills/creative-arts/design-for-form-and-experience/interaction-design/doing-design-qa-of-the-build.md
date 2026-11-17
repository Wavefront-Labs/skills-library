---
id: creative-arts.design-for-form-and-experience.interaction-design.doing-design-qa-of-the-build
name: doing-design-qa-of-the-build
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [design-qa, ui-qa, visual-qa, design-review-of-build, implementation-review, design-code-parity]
level: practitioner
status: draft
description: "Do design QA on the built product: compare build to design on devices, check tokens, states, responsive, accessibility and motion, log defects with severity."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Design QA of the build

Design QA checks that what shipped matches the design intent. It is a collaboration with engineering, not a fault-finding exercise.

## Prepare
1. Get a **testable build** (staging or preview link) and the matching design version and spec.
2. List the **checklist:** layout and spacing, typography, colour and tokens, component usage, states (hover, focus, disabled, loading, error, empty), responsive behaviour, content and truncation, icons and images, motion and timing, accessibility (focus order, contrast, labels), dark mode, localisation.

## Run
1. **Compare side by side** at the same viewport sizes: overlay design with the build (browser extension, Figma plugin or screenshot overlay), or compare inspected values.
2. **Use real devices and browsers** from the supported matrix.
3. **Test interactions:** every state in the spec; keyboard navigation; screen reader pass on key flows; reduced motion.
4. **Check data edge cases:** long names, empty data, large numbers, other languages.
5. **Log defects** with screenshot, design reference, device and browser, expected vs actual, and severity (blocker, major, minor, polish).
6. **Triage with engineering:** distinguish bugs from acceptable deviations; decide what ships and what goes to the backlog.
7. **Verify fixes** and close.

## Prevent
Use shared tokens and components (see `...design-systems.running-a-design-code-parity-audit`), and visual regression tests (see `...design-systems.visual-regression-testing-for-components`).

## Verify
- [ ] Every checklist area was reviewed on at least two devices.
- [ ] Each defect has a reference and severity.
- [ ] Accepted deviations are recorded.
