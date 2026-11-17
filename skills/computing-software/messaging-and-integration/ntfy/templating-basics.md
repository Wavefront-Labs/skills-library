---
id: computing-software.messaging-and-integration.ntfy.templating-basics
name: templating-basics
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, template, templating, webhook, go-template]
level: practitioner
status: docs-checked
description: "Turn a JSON webhook body into an ntfy notification with X-Template using pre-defined github, grafana and alertmanager templates."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message templating

Enable with header `X-Template` (aliases `Template`, `Tpl`) or query `?template=`. The webhook body must be valid JSON. Values:

- A pre-defined name: `github`, `grafana`, `alertmanager`.
- A custom name: loads `<name>.yml` from `template-dir` (default `/etc/ntfy/templates`).
- `yes` or `1`: inline templating.

```
curl -sT- "https://ntfy.example.com/mytopic?template=github" < payload.json
```

A file with the same name as a pre-defined template in the template directory overrides the built-in.

## Limits

- Disabled actions: `{{define}}`, `{{template}}`, `{{block}}`, `{{call}}`.
- A template that runs too long returns HTTP 400.
- Maximum template size is 32 KB.
- `printf` width/precision must be below 1000; `indent`/`nindent` are limited to 100 spaces.

## Debugging

The docs recommend the Go Template Playground for testing before use. See templating-custom-inline for writing your own and template-functions for the function list.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Message templating: X-Template aliases, pre-defined, custom and inline modes, template-dir, disabled actions, HTTP 400, 32 KB, printf and indent limits, Go Template Playground). Removed: the Verify step.
Method: documentation only; no commands were run.
