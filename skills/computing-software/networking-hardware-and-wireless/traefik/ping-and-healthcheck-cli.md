---
id: computing-software.networking-hardware-and-wireless.traefik.ping-and-healthcheck-cli
name: ping-and-healthcheck-cli
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, ping, healthcheck, liveness, readiness, traefik-entrypoint]
level: practitioner
status: docs-checked
description: "Expose a Traefik liveness endpoint with ping and use the traefik healthcheck command in container health checks."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/observability/healthcheck.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ping and healthcheck cli
Enable the ping endpoint with `ping: {}` in the install config. It serves `/ping` on the `traefik` entrypoint (port 8080 by default) and returns OK with status 200. The command `traefik healthcheck` calls it and exits 0 when healthy or 1 otherwise, which suits Docker `HEALTHCHECK` or Compose health checks.

```yaml
ping: {}
```
```yaml
# compose service
healthcheck:
  test: ["CMD", "traefik", "healthcheck"]
  interval: 10s
```
Gotchas: `/ping` (GET or HEAD) is an endpoint to check for Traefik process liveness, not route health. `ping.entryPoint` (default `traefik`) enables it on a dedicated entrypoint. `ping.manualRouting` disables the default internal router so you can create your own for `ping@internal`. During graceful shutdown it returns 503 by default; `ping.terminatingStatusCode` changes that.

## Checked
2026-11-03. Confirmed against the Traefik CLI and ping reference page: `traefik healthcheck` exit status 0 or 1, `/ping` returning 200 with OK, `ping.entryPoint` default `traefik` (port 8080), `manualRouting` and `terminatingStatusCode` 503. Removed: the `--ping` flag on the healthcheck command in the Compose example (the page shows the plain command), the exposure claim and the curl Verify step.
Method: documentation only; no commands were run.


