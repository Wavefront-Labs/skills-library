---
id: computing-software.web-development.storybook.a11y-addon-setup
name: a11y-addon-setup
category: computing-software
field: web-development
product: storybook
tags: [accessibility, a11y, axe-core, a11y-addon, wcag]
level: practitioner
status: docs-checked
description: "Install the accessibility addon and configure axe-core context, config and options per project, component or story."
sources:
  - https://storybook.js.org/docs/writing-tests/accessibility-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Accessibility addon

Goal: audit stories against WCAG rules with axe-core.

```shell
npx storybook add @storybook/addon-a11y
```
Adds a toolbar vision-impairment simulator and an Accessibility panel with Violations, Passes and Incomplete tabs. It runs automatically when you open a story.

Parameters (`parameters.a11y`):
- `context` (default `'body'`): axe context; limits which elements are checked
- `config`: passed to `axe.configure()`, mainly for rules
- `options`: passed to `axe.run` (default `{}`)
- `test`: behavior under the Vitest addon (see a11y-test-behavior)
- `globals.a11y.manual = true` disables automatic checks on visit

Default rulesets are WCAG 2.0 and 2.1 Level A and AA plus best practices. The `region` rule is disabled by default because it does not typically apply to components in stories and can lead to false negatives.

```ts
parameters: {
  a11y: {
    config: { rules: [{ id: 'image-alt', enabled: false }] },
    context: { include: ['body'], exclude: ['.no-a11y-check'] },
  },
},
```

Set at preview, meta or story level. Use `context.exclude` for elements you do not own.

Verify: a deliberate violation (missing alt text) appears under Violations.

## Checked
Date: 2026-11-04. Read the Accessibility testing page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: panel tabs, parameter names and defaults, default rulesets, `region` rule note, `globals.a11y.manual`.
Removed: an invented color-contrast config example, replaced by the page's own image-alt and context examples.
Method: documentation only; no commands were run.
