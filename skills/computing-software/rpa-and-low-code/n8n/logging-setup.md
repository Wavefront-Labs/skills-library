---
id: computing-software.rpa-and-low-code.n8n.logging-setup
name: logging-setup
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, logging, log-level, winston, log-file, log-streaming]
level: practitioner
status: docs-checked
description: "Configure n8n logging with N8N_LOG_LEVEL, N8N_LOG_OUTPUT and file rotation variables; know the levels and that log streaming is Enterprise only."
sources:
  - https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/set-up-logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get useful logs for debugging. n8n uses the winston library. All options are on every Cloud plan and self-hosted edition, except log streaming (Enterprise only).

| Config file key | Variable | Meaning |
| --- | --- | --- |
| `n8n.log.level` | `N8N_LOG_LEVEL` | `error`, `warn`, `info` (default), `debug`; `silent` outputs nothing |
| `n8n.log.output` | `N8N_LOG_OUTPUT` | `console` (default) and/or `file`, comma separated |
| `n8n.log.file.location` | `N8N_LOG_FILE_LOCATION` | default `<n8nFolderPath>/logs/n8n.log` |
| `n8n.log.file.fileSizeMax` | `N8N_LOG_FILE_SIZE_MAX` | MB per file, default 16 |
| `n8n.log.file.fileCountMax` | `N8N_LOG_FILE_COUNT_MAX` | files kept, default 100; set it when using workers |

```bash
export N8N_LOG_LEVEL=debug
export N8N_LOG_OUTPUT=console,file
export N8N_LOG_FILE_LOCATION=/var/log/n8n/n8n.log
export N8N_LOG_FILE_SIZE_MAX=50
export N8N_LOG_FILE_COUNT_MAX=60
```
`debug` is the most verbose. File location is only used when output includes `file`. Front-end (editor) logs are not available.

For development code, n8n logs through `LoggerProxy` from `n8n-workflow`: `Logger.info('message', {workflowName, workflowId})`. Guidance: wrap names in quotes, repeat key facts in message and metadata, include `executionId`, `workflowId`, `sessionId`, prefer node types over node names. Any new CLI command must call `LoggerProxy.init()` itself since `start.ts` does it only for the start command.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/set-up-logging

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
