---
id: computing-software.web-development.ghost.ghost-theme-validation-with-gscan
name: ghost-theme-validation-with-gscan
category: computing-software
field: web-development
product: ghost
tags: [ghost, gscan, theme-validation, npm, ci]
level: practitioner
status: docs-checked
description: "Validate a Ghost theme with gscan online or on the command line, and know that uploads are checked automatically."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/gscan.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: catch theme problems before Ghost does.

Facts from the docs:
- The GScan website is the first place to test a theme you are building; it produces a full validation report.
- When you upload a theme in Ghost Admin it is automatically checked with gscan, and fatal errors stop the theme being used.
- gscan also runs as a command-line tool.

CLI usage:
```bash
npm install -g gscan
gscan /path/to/ghost/content/themes/casper
gscan -z /path/to/download/theme.zip
```
The first form scans a folder; `-z` scans a ZIP file.

GScan checks a theme for errors, deprecations and compatibility issues.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 25 lines, no imported snippets): themes/gscan.mdx. The three uses and the CLI commands match. Removed as unconfirmed: the CI workflow, the instruction to re-run after changing helpers or package.json, the pre-1.0 upgrade guide statement and the Verify step. The page does not describe the report format or exit codes, so none are given.
Method: documentation only; no commands were run.
