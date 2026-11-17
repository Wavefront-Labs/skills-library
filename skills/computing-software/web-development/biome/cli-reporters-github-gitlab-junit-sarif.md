---
id: computing-software.web-development.biome.cli-reporters-github-gitlab-junit-sarif
name: cli-reporters-github-gitlab-junit-sarif
category: computing-software
field: web-development
product: biome
tags: [biome, reporter, github-reporter, gitlab-reporter, junit, sarif, checkstyle, rdjson, reporter-file, json-reporter]
level: practitioner
status: docs-checked
description: "Choose a --reporter (default, concise, summary, json, github, gitlab, junit, checkstyle, rdjson, sarif) and write several outputs with --reporter-file."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--reporter=FORMAT` changes how diagnostics and the summary are written (default `default`):

| Value | Output |
| --- | --- |
| default | full diagnostics and summary for a terminal |
| concise | one line per diagnostic, formatter diagnostics grouped |
| summary | diagnostics grouped by category and rule, formatter diagnostics by file |
| json / json-pretty | machine-readable JSON (json-pretty uses Biome's default JSON formatting) |
| github | GitHub workflow commands that create annotations |
| gitlab | GitLab Code Quality report |
| junit | JUnit XML |
| checkstyle | Checkstyle XML |
| rdjson | Reviewdog diagnostic JSON |
| sarif | SARIF for static analysis integrations |

The `json` and `json-pretty` reporters are experimental and may change in patch releases.

`--reporter-file=PATH` writes the associated reporter's output to a file (default reporter if none given):

```shell
biome ci --reporter=junit --reporter-file=report.xml
```

Repeat `--reporter` to produce multiple outputs. Example: print the default output to the terminal and write RDJSON to a file:

```shell
biome ci --reporter=default --reporter=rdjson --reporter-file=report.json
```

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the closing advice on which reporter to use where and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
