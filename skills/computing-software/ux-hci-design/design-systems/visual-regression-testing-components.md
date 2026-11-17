---
id: computing-software.ux-hci-design.design-systems.visual-regression-testing-components
name: visual-regression-testing-components
category: computing-software
field: ux-hci-design
product: design-systems
tags: [visual-regression-testing, component-testing]
level: practitioner
status: draft
description: "Catch unintended UI changes with snapshot or visual tests in CI plus automated accessibility checks."
sources:
  - https://storybook.js.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Component testing
- Unit/interaction tests (Testing Library) for behaviour.
- Visual regression: screenshots per story compared to baselines (Chromatic, Playwright `toHaveScreenshot`); fix fonts and animations for determinism.
- Automated a11y per story (axe).
- Review diffs before accepting new baselines.

## Verify
- [ ] An intentional padding change triggers a visual diff in CI.
