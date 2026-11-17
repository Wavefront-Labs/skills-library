---
id: computing-software.web-development.frontend-development.devtools-coverage-panel
name: devtools-coverage-panel
category: computing-software
field: web-development
product: frontend-development
tags: [coverage-panel, unused-css, unused-javascript, devtools, performance]
level: practitioner
status: docs-checked
description: "Finding unused CSS and JavaScript with the Chrome DevTools Coverage panel: recording, reading the report, acting on results, and Lighthouse audits."
sources:
  - https://developer.chrome.com/docs/devtools/coverage
  - https://developer.chrome.com/docs/lighthouse/performance/unused-javascript
  - https://developer.chrome.com/docs/lighthouse/performance/unused-css-rules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DevTools Coverage panel and unused CSS/JS

## 1. Recording
1. Open DevTools, open the Command Menu, type "coverage" and run **Show Coverage** (or More options > More tools > Coverage). The panel opens in the Drawer.
2. In the action bar choose **Per function** or **Per block** as the coverage scope.
3. Click **Reload** to start recording: the panel reloads the page, captures the code needed to load it, and keeps recording while you interact with the page. Open menus, submit forms and scroll so interaction-only code is captured.
4. Click **Stop instrumenting coverage and show results** to stop.

## 2. Reading the report
- Columns: URL, Type (CSS, JavaScript or both), Total Bytes, Unused Bytes, and Usage Visualization (gray is unused, green is used).
- Click a row to open the resource in Sources, where unused lines are marked with vertical gray lines beside the line numbers.
- The filter box filters by URL; the status bar shows the percentage of code used and respects the filter. The drop-down selects All, CSS or JavaScript.
- Turn on **Content scripts** to include extension code in the report.
- **Export coverage** (download icon) saves the report.
- The Puppeteer `Coverage` class can automate detecting unused code and extracting used code.
- The guide does not cover refactoring a codebase to avoid unused code; that depends on your stack.

## 3. Lighthouse audits
- Remove unused JavaScript flags every script file with more than 20 KiB of unused code.
- Remove unused CSS lists stylesheets with potential savings of 2 KiB or more.
- Unused CSS slows rendering because the browser must download external stylesheets before rendering, and checks which rules apply to each DOM node when building the render tree.

## 4. What to do with unused code
| Finding | Action (from the Lighthouse pages) |
|---|---|
| Large JavaScript bundle, not server-side rendered | React: split with `React.lazy()`; Vue with router: lazy-load routes |
| Bundler support unclear | Check the Tooling.Report tests for code splitting, unused code elimination and unused imported code |
| CSS needed only for first paint | Inline the critical styles in a `<style>` block in the head and load the rest asynchronously with preload; the Critical tool can automate extraction |
| Unused code from CMS plugins or modules | WordPress and Joomla: reduce or switch the extensions loading it; Drupal: attach libraries only to pages that use them |

Recording only reflects what the page loaded and what you did during that recording, so repeat it on each key route and interaction before deleting code.

## Verify
- [ ] Coverage recorded on each top route with interactions; unused bytes on initial load dropped and the Lighthouse unused JavaScript and CSS audits improved without visual regressions.

## Checked

2026-11-09. Read in full the DevTools Coverage page and the Lighthouse Remove unused JavaScript and Remove unused CSS pages. Confirmed the steps, columns, filters, Content scripts, export, the 20 KiB and 2 KiB audit thresholds, and the stack-specific advice. Removed: the keyboard shortcut, the Guest profile tip, red/blue bar colours, the Brotli saving figure, source-map and JSON-export remarks, the PurgeCSS/Tailwind and polyfill advice, and the false-positive list, none of which the pages state.

Method: documentation only; no commands were run.
