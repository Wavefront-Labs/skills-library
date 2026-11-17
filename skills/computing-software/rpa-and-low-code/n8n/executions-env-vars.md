---
id: computing-software.rpa-and-low-code.n8n.executions-env-vars
name: executions-env-vars
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, executions, timeout, data-pruning, execution-mode, autodeactivation]
level: practitioner
status: docs-checked
description: "Execution environment variables for n8n: mode, timeouts, what data to save, storage mode, pruning age and count, display size limit and crash auto-deactivation."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tune how executions run and what is kept. Defaults in brackets.

- `EXECUTIONS_MODE` (`regular` or `queue`).
- `EXECUTIONS_TIMEOUT` (-1 disabled; seconds) default for all workflows; users may override per workflow up to `EXECUTIONS_TIMEOUT_MAX` (3600). `N8N_AI_TIMEOUT_MAX` (3600000 ms) is the HTTP timeout for AI/LLM nodes; raise it for slow local models.
- Saving: `EXECUTIONS_DATA_SAVE_ON_ERROR` and `EXECUTIONS_DATA_SAVE_ON_SUCCESS` (`all` or `none`), `EXECUTIONS_DATA_SAVE_ON_PROGRESS` (false), `EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS` (true).
- Storage: `N8N_EXECUTION_DATA_STORAGE_MODE` (`database`, `filesystem`, `s3`, `azure`; s3 and azure need a Business or Enterprise self-hosted plan); `N8N_STORAGE_PATH` (default `N8N_USER_FOLDER/storage`) is also used for filesystem binary data.
- Pruning: `EXECUTIONS_DATA_PRUNE` (true), `EXECUTIONS_DATA_MAX_AGE` (336 h), `EXECUTIONS_DATA_PRUNE_MAX_COUNT` (10000; 0 no limit), `EXECUTIONS_DATA_HARD_DELETE_BUFFER` (1 h), `EXECUTIONS_DATA_PRUNE_HARD_DELETE_INTERVAL` (15 min), `EXECUTIONS_DATA_PRUNE_SOFT_DELETE_INTERVAL` (60 min).
- `EXECUTIONS_DATA_MAX_DISPLAY_SIZE` (104857600 bytes): larger executions show as "too large to display" to protect memory; retry and resume still load full data.
- `N8N_CONCURRENCY_PRODUCTION_LIMIT` (-1 off in regular mode) and `N8N_CONCURRENCY_EVALUATION_LIMIT`.
- `N8N_WORKFLOW_AUTODEACTIVATION_ENABLED` (false) unpublishes a workflow after `N8N_WORKFLOW_AUTODEACTIVATION_MAX_LAST_EXECUTIONS` (3) crashed executions.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
