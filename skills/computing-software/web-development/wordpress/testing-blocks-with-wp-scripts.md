---
id: computing-software.web-development.wordpress.testing-blocks-with-wp-scripts
name: testing-blocks-with-wp-scripts
category: computing-software
field: web-development
product: wordpress
tags: [wp-scripts-test, block-testing, playwright, jest, wp-env]
level: practitioner
status: docs-checked
description: "Testing WordPress blocks: unit tests with wp-scripts test-unit-js (Jest), end-to-end tests with test-playwright and wp-env, editor utilities, PHP render tests, and running in CI."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/packages/scripts/README.md
  - https://github.com/WordPress/gutenberg/blob/trunk/packages/e2e-test-utils-playwright/README.md
  - https://github.com/WordPress/gutenberg/blob/trunk/packages/env/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing blocks (wp-scripts test-unit-js / test-e2e)

## 1. Unit tests (Vitest by default in current @wordpress/scripts)
```json
{ "scripts": { "test:unit": "wp-scripts test-unit-js", "test:e2e": "wp-scripts test-e2e", "env": "wp-env" } }
```
```js
// src/utils/format-price.test.js
import { test, expect } from "vitest";
import { formatPrice } from "./format-price";
test("formats cents", () => expect(formatPrice(1999, "USD")).toBe("$19.99"));

// components with React Testing Library
import { render, screen } from "@testing-library/react";
import { Edit } from "../edit";
test("shows placeholder", () => {
  render(<Edit attributes={{}} setAttributes={() => {}} />);
  expect(screen.getByText("Add a title")).toBeInTheDocument();
});
```
- In current `@wordpress/scripts`, `wp-scripts test-unit-js` runs the Vitest you install in your project (for example `npm install --save-dev vitest@^5 vite@^8`). The default environment is Node, Vitest APIs (`test`, `expect`) are imported explicitly, and it discovers `*.test.*` and `*.spec.*` files. `@wordpress/scripts` supplies no Vitest preset, DOM environment, React transform or aliases: configure jsdom and JSX yourself (see the package's `vitest-migration.md`).
- Existing Jest suites keep working through `wp-scripts test-unit-jest` (maintenance-only adapter for a project-installed Jest); `@wordpress/scripts` no longer bundles Jest, jsdom or the WordPress Jest preset. The React Testing Library example below needs a DOM environment in either runner.
- Test `save()` output stability and `deprecated` migrations by parsing old markup with `parse()` from `@wordpress/blocks`.

## 2. End-to-end with Playwright
```js
// tests/e2e/block.spec.js
import { test, expect } from "@wordpress/e2e-test-utils-playwright";
test.describe("Acme Card", () => {
  test("can be inserted and saved", async ({ admin, editor, page }) => {
    await admin.createNewPost();
    await editor.insertBlock({ name: "acme/card", attributes: { title: "Hello" } });
    await editor.publishPost();
    expect(await editor.getEditedPostContent()).toContain("wp:acme/card");
    // then open the published post on the front end and assert the rendered output
  });
});
```
- `wp-scripts test-e2e` runs Playwright (`test-playwright` is an alias for the same command). By default it looks for `.test` or `.spec` files in a root-level `/specs` folder; add a `playwright.config.ts` or `.js` at the package root for custom options. `npm run test:e2e:debug` (`wp-scripts test-e2e --debug`) opens the Playwright inspector.
- The `test` export of `@wordpress/e2e-test-utils-playwright` provides the `admin`, `editor`, `pageUtils` and `requestUtils` fixtures.
- The editor canvas is an iframe: use the `canvas` property (for example `editor.canvas.locator(...)`) to select elements inside it.

## 3. Environment
`npx wp-env start` launches WordPress in Docker with your plugin mounted (`.wp-env.json` sets core, PHP version, plugins, themes). The development site is at `http://localhost:8888` (user `admin`, password `password`). The separate tests environment and its `testsPort` (default 8889) are deprecated in favour of a second config file passed with `wp-env --config`. The E2E runner uses `WP_BASE_URL` when set; otherwise it detects the `wp-env` environment in the current directory, and `--wp-env-config=<path>` selects a custom config file.

## 4. PHP side
Dynamic blocks: PHPUnit with the WordPress test suite, asserting `render_block()` output for given attributes. Composer, PHPUnit and WP-CLI are available in the environment via `wp-env run <container> <tool>` (for example `wp-env run cli phpunit`).

## 5. CI
In CI: set up Node, `npm ci`, `npx wp-env start`, `npm run test:unit`, install Playwright browsers, `npm run test:e2e`. Test against the minimum supported and latest WordPress versions by changing `core` in `.wp-env.json`.

## Verify
- [ ] Unit tests cover utilities, edit UI states and deprecations; e2e inserts, saves and renders the block front end; CI runs both against two WordPress versions.

## Checked

2026-10-25: against the Gutenberg trunk READMEs of `@wordpress/scripts`, `@wordpress/e2e-test-utils-playwright` and `@wordpress/env` (last commits 2026-10-25). Confirmed: `test-unit-js` now runs the project's Vitest (Jest moved to `test-unit-jest`), `test-e2e` with the `test-playwright` alias, default `/specs` discovery and config files, fixtures `admin`/`editor`/`pageUtils`/`requestUtils`, `canvas` property, wp-env default port 8888 and deprecated tests environment, `wp-env run <container>`. Corrected the stale Jest-default and `test-e2e`-was-Puppeteer claims. The example helper names `admin.createNewPost`, `editor.insertBlock`, `editor.publishPost` and `editor.getEditedPostContent` match files in the package source; the `acme/card` block and `formatPrice` are illustrative.

Method: documentation only; no commands were run.
