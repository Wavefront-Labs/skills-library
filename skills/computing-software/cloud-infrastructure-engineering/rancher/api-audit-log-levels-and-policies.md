---
id: computing-software.cloud-infrastructure-engineering.rancher.api-audit-log-levels-and-policies
name: api-audit-log-levels-and-policies
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [audit-log, audit-level, auditpolicy, redaction, rancher-api, helm, environment-variables]
level: advanced
status: docs-checked
description: "Enable the Rancher API audit log with AUDIT_LOG_ENABLED and AUDIT_LEVEL, understand what each level records, and use AuditPolicy resources to filter requests and redact data."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/advanced-user-guides/enable-api-audit-log
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The API audit log records every request to the Rancher API and its response, showing what happened, when, who initiated it and which cluster it affected. It is switched on by environment variables on the Rancher server container, at install or upgrade.

Parameters:

- `AUDIT_LOG_ENABLED`: `false` (default) or `true`.
- `AUDIT_LEVEL`: `0` metadata only (default), `1` adds request and response headers, `2` adds the request body, `3` adds the response body. Levels are cumulative, and one request/response pair shares an `auditID`.
- `AUDIT_LOG_PATH`: default `/var/log/auditlog/rancher-api-audit.log`; the directory can be mounted to the host.
- `AUDIT_LOG_MAXAGE`: days to keep old files, default 10.
- `AUDIT_LOG_MAXBACKUP`: files to keep, default 10.
- `AUDIT_LOG_MAXSIZE`: megabytes before rotation, default 100.

**Policies.** `AuditPolicy` cluster-scoped resources add redactions and filters on top of the defaults; all policies are additive. Header redaction uses regular expressions, and body redaction uses a JSONPath engine that does not support script or filter expressions. The page's skeleton:

```yaml
apiVersion: auditlog.cattle.io/v1
kind: AuditPolicy
spec:
  enabled : true # true/false
  filters:
    - action: allow # allow/deny
      requestURI: "/foo/.*"
  additionalRedactions:
    - headers:
      - "Cache.*"
      paths:
      - "$.gitCommit"
  verbosity:
    level : 0
```

A filter pattern such as `/foo/.*` matches `/foo/some/endpoint` but not `/foo` or `/foobar`.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Enabling the API Audit Log. Removed the pointer to Docker advanced options (the page covers the Kubernetes install only).

Method: documentation only; no commands were run.
