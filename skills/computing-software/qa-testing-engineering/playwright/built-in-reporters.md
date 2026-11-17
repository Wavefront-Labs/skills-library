---
id: computing-software.qa-testing-engineering.playwright.built-in-reporters
name: built-in-reporters
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [junit-reporter, github-reporter, playwright-reporters, json-reporter, blob-reporter-config]
level: practitioner
status: docs-checked
description: "Choose and combine Playwright built-in reporters (list, line, dot, html, json, junit, github, blob), configure output files and wire them into CI systems."
sources:
  - https://playwright.dev/docs/test-reporters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in reporters

**Goal:** right output for humans in the terminal, machines in CI, and annotations on the PR.

## Reporters
| Reporter | Use |
|---|---|
| `list` | default locally: one line per test |
| `line` | compact, good for large suites locally |
| `dot` | default in CI: minimal output |
| `html` | interactive report with traces |
| `json` | machine-readable results (`outputFile`) |
| `junit` | JUnit XML for Jenkins, GitLab, Azure DevOps, test management import |
| `github` | GitHub Actions annotations on failing lines |
| `blob` | for merging sharded runs |

## Combining
```ts
reporter: process.env.CI
  ? [['dot'], ['github'], ['junit', { outputFile: 'results/junit.xml' }], ['html', { open: 'never' }]]
  : [['list'], ['html', { open: 'on-failure' }]],
```
CLI override: `npx playwright test --reporter=line,junit` (output paths via env: `PLAYWRIGHT_JUNIT_OUTPUT_NAME=results.xml`, `PLAYWRIGHT_JSON_OUTPUT_NAME=results.json`; `PLAYWRIGHT_JUNIT_OUTPUT_FILE` and `PLAYWRIGHT_JSON_OUTPUT_FILE` take a full path).

## JUnit options
```ts
['junit', { outputFile: 'junit.xml', includeProjectInTestName: true, stripANSIControlSequences: true }]
```
`includeProjectInTestName` prefixes each test case name with the project name (env `PLAYWRIGHT_JUNIT_INCLUDE_PROJECT_IN_TEST_NAME`); `stripANSIControlSequences` removes ANSI sequences from the text (env `PLAYWRIGHT_JUNIT_STRIP_ANSI`).

## CI wiring
The `junit` reporter writes an XML file to `outputFile`; point your CI system's JUnit import at that path (see that system's documentation for the exact keyword).

## Gotchas
- Without `outputFile` (or the `PLAYWRIGHT_JSON_OUTPUT_NAME` / `PLAYWRIGHT_JUNIT_OUTPUT_NAME` variables) the JSON and JUnit reporters print to stdout, which mixes with other output; always set a file.
- Other reporters work on GitHub Actions too but do not produce annotations; the `github` reporter does.

## Verify
The CI test tab shows the same number of tests as a local run of the suite.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: default reporters (list locally, dot on CI), the reporter table entries, outputFile and the PLAYWRIGHT_JSON/JUNIT output environment variables, the JUnit options includeProjectInTestName and stripANSIControlSequences, and the github reporter producing annotations. Removed: the embedAnnotationsAsProperties option, the duplicate-annotation claim, the per-CI wiring snippets and the test-count command, none of which the Playwright docs cover.

Method: documentation only; no commands were run.
