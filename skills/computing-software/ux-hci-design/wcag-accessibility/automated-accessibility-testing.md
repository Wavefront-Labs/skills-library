---
id: computing-software.ux-hci-design.wcag-accessibility.automated-accessibility-testing
name: automated-accessibility-testing
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [axe-core, automated-a11y-testing, wcag-testing-conformance]
level: practitioner
status: draft
description: "Use axe-core and Lighthouse in dev and CI, and know that automated tools find only a portion of issues."
sources:
  - https://www.deque.com/axe/
  - https://www.w3.org/WAI/test-evaluate/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated checks
- axe DevTools / `axe-core` in unit/e2e tests (jest-axe, `@axe-core/playwright`); Lighthouse accessibility audit; pa11y CLI.
- Fail CI on new violations; triage existing with a baseline.
- Tools detect only a minority of WCAG issues (commonly cited as roughly 30-40%; exact share varies by study); they cannot judge alt text quality or logical order.
```js
const results = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag22aa']).analyze();
```

## Verify
- [ ] CI step fails on seeded violation (missing alt).
