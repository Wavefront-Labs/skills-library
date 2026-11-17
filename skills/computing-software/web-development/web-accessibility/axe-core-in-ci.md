---
id: computing-software.web-development.web-accessibility.axe-core-in-ci
name: axe-core-in-ci
category: computing-software
field: web-development
product: web-accessibility
tags: [jest-axe, pa11y, axe-playwright, automated-accessibility-testing, vitest-axe, accessibility-testing]
level: practitioner
status: verified
description: "Automating accessibility checks: axe-core with Playwright, jest-axe/vitest-axe on components, pa11y-ci over sitemaps, WCAG tag selection, baselines and what automation misses."
sources:
  - https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright
  - https://github.com/nickcolley/jest-axe
  - https://github.com/pa11y/pa11y-ci
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# axe-core in CI

## 1. End-to-end pages (Playwright)
```ts
import AxeBuilder from "@axe-core/playwright";
test("checkout has no detectable a11y violations", async ({ page }) => {
  await page.goto("/checkout");
  await page.getByRole("button", { name: "Continue" }).click();      // test states, not just initial load
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .exclude("#third-party-chat")
    .analyze();
  expect(results.violations).toEqual([]);
});
```
Scan open dialogs, error states, expanded menus, dark mode. `AxeBuilder` needs a page created from `browser.newContext()` (a bare `browser.newPage()` throws "Please use browser.newContext()"; the `page` test fixture is fine; run with @axe-core/playwright 4.13).

Tag notes (axe-core API docs and `axe.getRules()`): the WCAG tags above do not include `best-practice` rules such as `region`, `skip-link` and `aria-allowed-role`, so add `"best-practice"` if you want them. `target-size` (2.5.8, tag `wcag22aa`) is disabled by default but does run when you select `wcag22aa` (run). In axe-core 4.13 `label-content-name-mismatch` was tagged `experimental` and off; in 4.14 it is on by default.

## 2. Components (unit level)
```ts
import { axe } from "vitest-axe";        // or jest-axe with toHaveNoViolations
const { container } = render(<LoginForm />);
expect(await axe(container)).toHaveNoViolations();
```
vitest-axe needs the matcher registered once: `import "vitest-axe/extend-expect"` in a setup file (or `expect.extend(matchers)` from `vitest-axe/matchers`); jest-axe uses `expect.extend(toHaveNoViolations)`. JSDOM does no layout, so colour contrast cannot be checked there (jest-axe's README says it turns `color-contrast` off for you; a `#ddd`-on-white paragraph passed under jsdom here); leave contrast to browser-based runs.

## 3. Whole site crawl
```json
// .pa11yci
{ "defaults": { "standard": "WCAG2AA", "runners": ["axe", "htmlcs"], "timeout": 30000 },
  "urls": ["http://localhost:3000/", "http://localhost:3000/pricing"] }
```
`pa11y-ci --sitemap https://staging.example.com/sitemap.xml` for broad coverage (pa11y-ci reads `.pa11yci` JSON, `.pa11yci.cjs`, `.pa11yci.js` or `.pa11yci.json`; the `//` label line above is not valid JSON, so drop it in the real file; `WCAG2AA` is pa11y's default standard); Lighthouse CI accessibility score as a coarse guard.

## 4. Rolling it out
- Existing debt: snapshot current violations (by rule + selector) as a baseline, fail only on new ones, burn down the baseline.
- Treat `serious`/`critical` impact as blocking first.
- Disable rules only with a comment and ticket.

## 5. Limits
Automated rules catch a minority of WCAG issues (missing names, contrast, invalid ARIA, duplicate ids, missing lang). They cannot judge alt text quality, focus order, keyboard operability, meaningful headings or screen reader experience. Pair with manual keyboard and screen reader testing.

## Verify
- [ ] CI fails when a button loses its accessible name; reports list rule, impact, selector and help URL.
