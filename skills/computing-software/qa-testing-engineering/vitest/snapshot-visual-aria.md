---
id: computing-software.qa-testing-engineering.vitest.snapshot-visual-aria
name: snapshot-visual-aria
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [to-match-screenshot, aria-snapshot, visual-regression, to-match-aria-snapshot]
level: advanced
status: docs-checked
description: "Snapshot UI in Vitest browser mode with toMatchScreenshot for visual regression and the experimental toMatchAriaSnapshot (4.1.4) for accessibility trees."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/browser/visual-regression-testing.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/browser/aria-snapshots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Visual regression with `toMatchScreenshot`, using `page` from `vitest/browser`:

```ts
import { expect, test } from 'vitest'
import { page } from 'vitest/browser'

test('button renders in default state', async () => {
  await expect(page.getByRole('button')).toMatchScreenshot()
})
```

Rendering depends on GPU, OS, fonts, browser version and headless versus headed, so run it in a standardised environment (Docker, CI-only workflows or a cloud service). Keep visual tests in a separate project (for example files named `*.vrt.test.ts`, headless, fixed `viewport`) so unit tests exclude them.

It documents how something looks; it is not a substitute for behavior assertions.

ARIA snapshots (experimental, 4.1.4) assert the accessibility tree instead of pixels or raw HTML:

```ts
await expect.element(page.getByRole('navigation')).toMatchAriaInlineSnapshot(`
  - navigation "Main":
    - link "Home":
      - /url: /
`)
```

`toMatchAriaSnapshot()` stores it in a `.snap` file. They use the usual snapshot workflow (`-u`, watch updates, CI rules). They survive HTML restructuring as long as the semantics match, and catch missing labels, broken roles and wrong heading levels.

On the first run of a visual test Vitest creates the reference screenshot (in a `__screenshots__` folder next to the tests) and fails the test, asking you to review it before running again. Commit the references. Screenshots of deleted or renamed tests are not removed automatically.

## Checked

2026-11-04. Confirmed against guide/browser/visual-regression-testing.md and guide/browser/aria-snapshots.md: the environmental factors, Docker/CI/cloud advice, the separate vrt project with headless and a fixed viewport, not a replacement for behaviour testing, reference creation on first run, the experimental 4.1.4 ARIA snapshot matchers, the shared snapshot workflow, and semantic matching despite HTML changes. Replaced a generic gotcha with the documented first-run behaviour.

Method: documentation only; no commands were run.
