---
id: computing-software.cybersecurity-defensive.pomerium.health-check-probes
name: health-check-probes
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [health-check, readyz, pomerium-health, exclude-filter, systemd-watchdog]
level: practitioner
status: docs-checked
description: "Set up Pomerium health checks: HTTP probes on port 28080, the pomerium health CLI with exclude filters, the watch TUI and systemd notify."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/health-checks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**HTTP probes** default to `127.0.0.1:28080`: `/startupz`, `/readyz`, `/healthz`, `/status`. Change with `health_check_addr` or `HEALTH_CHECK_ADDR`, then match `pomerium health --health-addr` and probe ports.

Semantics: startup waits for all components and the latest config; readiness needs all components RUNNING and healthy; liveness treats a terminating state as healthy so shutdown is graceful.

Kubernetes example values: liveness `/healthz` with `initialDelaySeconds: 15`, `periodSeconds: 60`, `failureThreshold: 10`; readiness `/readyz` with 15, 60 and 5.

Caveat: HTTP probes may fail spuriously with unreliable database connectivity. Prefer CLI probes with exclusions.

**CLI**: `pomerium health` exits 0 healthy, 1 unhealthy. Flags: `-e, --exclude`, `-a, --health-addr` (default `127.0.0.1:28080`), `-v, --verbose`. Docker Compose: `test: [CMD, pomerium, health]`, `interval: 30s`, `retries: 5`, `timeout: 5s`.

Filter example: `pomerium health -e storage.backend -e config.databroker.build`.

Components include `authenticate.service`, `authorize.service`, `config.databroker.build`, `databroker.sync.initial`, `envoy.server`, `proxy.service`, `storage.backend`, `xds.*`.

**TUI**: `pomerium health watch -a <grpc_address> -s <shared_secret>`.

**Systemd**: configured automatically via sd_notify, `Type=notify`, `WatchdogSec=30s`. Disable by removing those options or `health_check_systemd_disabled: true`.

## Checked

2026-11-04. Read the Health Checks page: default probe address and endpoints, address override, startup, readiness and liveness semantics, Kubernetes example values, CLI exit codes and flags, Compose example, filters, component names, TUI command and systemd settings all confirmed. Nothing removed.

Method: documentation only; no commands were run.
