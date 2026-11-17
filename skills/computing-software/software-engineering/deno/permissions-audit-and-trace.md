---
id: computing-software.software-engineering.deno.permissions-audit-and-trace
name: permissions-audit-and-trace
category: computing-software
field: software-engineering
product: deno
tags: [permissions, audit-log, deno-audit-permissions, trace-permissions, opentelemetry, jsonl]
level: advanced
status: docs-checked
description: "Recording every permission access with DENO_AUDIT_PERMISSIONS (JSONL file or OpenTelemetry logs) and adding stack traces with DENO_TRACE_PERMISSIONS."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/permissions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno can log all accessed permissions, whether allowed or denied.

Set `DENO_AUDIT_PERMISSIONS` to a file path to write JSONL. Each line has keys `v` (format version), `datetime` (RFC 3339), `permission` (name) and `value` (or `null`). A schema is published as `permission-audit.v1.json` in the denoland/deno repo.

By default no stack trace is generated for permission requests because it costs performance. Set `DENO_TRACE_PERMISSIONS` to `1` to enable; combined with the audit variable, entries gain a `stack` array of frames.

Set `DENO_AUDIT_PERMISSIONS=otel` to emit each access as an OpenTelemetry log record instead, sent to whichever exporter is configured via `OTEL_DENO`. Attributes: `deno.permission.type`, `deno.permission.value`, and `deno.permission.stack` (if tracing is also on).

```sh
OTEL_DENO=true DENO_AUDIT_PERMISSIONS=otel deno run -A main.ts
```

This is the recommended setup if you already collect OpenTelemetry data, so the audit lands beside traces and metrics.

## Checked

2026-11-04. Confirmed against docs runtime/reference/permissions.md: DENO_AUDIT_PERMISSIONS file and otel modes, JSONL keys, schema file name, DENO_TRACE_PERMISSIONS, OTel attribute names, OTEL_DENO.

Method: documentation only; no commands were run.
