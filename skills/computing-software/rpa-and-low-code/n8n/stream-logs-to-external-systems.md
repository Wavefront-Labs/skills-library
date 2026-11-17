---
id: computing-software.rpa-and-low-code.n8n.stream-logs-to-external-systems
name: stream-logs-to-external-systems
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, log-streaming, audit, syslog, webhook, sentry, event-log]
level: advanced
status: docs-checked
description: "Stream n8n events to syslog, webhook or Sentry from the UI or N8N_LOG_STREAMING_DESTINATIONS, and avoid corrupted event log files on shared volumes in queue mode."
sources:
  - https://docs.n8n.io/administer/observe-and-log/stream-logs-to-external-systems
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: send n8n events (workflow, node, audit, worker, AI, runner, queue) to your logging tools. Enterprise only (Cloud and self-hosted).

## UI setup
**Settings > Log Streaming > Add new destination**, choose type (syslog server, generic webhook, Sentry client), fill the **New Event Destination** modal, pick **Events**, **Save**.

## Event log files
n8n writes each event to `<n8n-user-folder>/n8nEventLog.log` (suffix `-worker` or `-webhook-processor` on those processes) before forwarding, so undelivered events survive restarts. If several processes share one writable volume (queue mode workers on NFS or EFS) set `N8N_EVENTBUS_LOGWRITER_LOGFULLPATH` per process to a unique absolute path ending in `.log`; n8n uses it verbatim with no suffix. `N8N_EVENTBUS_LOGWRITER_MAXTOTALMESSAGESPERFILE` bounds lines parsed from one file on recovery so a corrupted file cannot exhaust memory. Quarantine an old shared `n8nEventLog-worker.log` manually first; n8n does not delete it.

## Events
Groups: Workflow (`n8n.workflow.started`, `.success`, `.failed`, `.cancelled`; cancelled also carries `reason`), Node executions, Audit (logins, user changes, credentials, workflows, variables, external secrets, 2FA, MCP and more), Worker, AI node logs, Runner, Queue. Subscribe to a group prefix such as `n8n.workflow`. Every workflow event has `executionId`, `workflowId`, `workflowName`.
MCP audit events (n8n 2.34.0 and later): `n8n.audit.mcp.oauth.completed`, `n8n.audit.mcp.tool.called` (fields include `toolName`, `status`, `authType`, `clientId`), `n8n.audit.mcp.access.updated`. `anonymizeAuditMessages` masks email and name but not `userId`, `authType` or `clientId`.

## Env-managed destinations (n8n 2.19.0 and later)
Set `N8N_LOG_STREAMING_MANAGED_BY_ENV=true` and `N8N_LOG_STREAMING_DESTINATIONS` to a JSON array; n8n reapplies it at every startup and locks the UI. Common fields: `type` (`webhook`, `syslog`, `sentry`), `label`, `enabled`, `subscribedEvents`, `anonymizeAuditMessages`, `circuitBreaker`.
```json
[{ "type": "webhook", "label": "Audit", "subscribedEvents": ["n8n.audit","n8n.workflow"],
   "anonymizeAuditMessages": true, "url": "https://hooks.example.com/n8n", "method": "POST",
   "options": { "timeout": 5000 } }]
```
Webhook defaults: `method` POST, `timeout` 5000 ms, `allowUnauthorizedCerts` false, redirects off (`maxRedirects` 21). Syslog: `host` required, `port` 514, `protocol` `udp` default (or `tcp`, `tls` which needs `tlsCa` PEM), `facility` 16.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Stream logs to external systems" page (docs.n8n.io, Markdown version, read in full).
Nothing removed; event groups, workflow and MCP fields, env-managed destination fields, defaults and the example match the page.
