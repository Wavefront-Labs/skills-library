---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-health-check-types
name: consul-health-check-types
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, health-checks, consul-checks, ttl-check]
level: practitioner
status: docs-checked
description: "Define HTTP, TCP, TTL, gRPC and script health checks with sensible intervals, and handle the critical-by-default initial state."
sources: ["https://developer.hashicorp.com/consul/docs/services/usage/checks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Checks attach to services or nodes. Types: script, HTTP, TCP, UDP, TTL, Docker, gRPC, H2ping, alias and OSService. New checks start `critical` so an instance is not served before it proves healthy; set `status = "passing"` only when you accept the risk.

```hcl
check {
  id       = "api-http"
  http     = "https://localhost:8443/healthz"
  method   = "GET"
  interval = "10s"
  timeout  = "3s"
  deregister_critical_service_after = "30m"
}
```

HTTP 200-299 is passing, 429 is warning, anything else fails. TTL checks are passive: the check goes critical if the service does not post a status update before the TTL expires.

Gotchas: script checks need `enable_local_script_checks` (only checks from local config files) or `enable_script_checks` (any registration method, with a documented remote execution risk; the docs recommend the local option). Script and Docker output is limited to 4KB and HTTP responses over 4KB are truncated. HTTP checks require a valid TLS certificate unless `tls_skip_verify` is true. A TTL check persists its last status to disk and restores it across agent restarts, valid through the end of the TTL from the last update.

Verify: `curl -s localhost:8500/v1/health/checks/web | jq '.[].Status'` shows `passing`; stopping the app turns it `critical`, and critical instances are excluded from DNS answers.

## Checked

2026-11-03. Confirmed against the health check registration page (check types, critical initial status, HTTP response codes, 4KB limits, script check options and warning, tls_skip_verify, TTL persistence) and the DNS agent options page (critical instances excluded). Removed: the within-an-interval timing claim.

Method: documentation only; no commands were run.
