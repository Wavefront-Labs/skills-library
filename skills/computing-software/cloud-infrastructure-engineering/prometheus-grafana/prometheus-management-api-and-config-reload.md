---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-management-api-and-config-reload
name: prometheus-management-api-and-config-reload
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, management-api, healthy-ready-endpoints, config-reload-sighup, hot-reload, lifecycle-api, reload-endpoint, quit-endpoint, readiness-probe, liveness-probe, config-reloader, promtool-check-config, prometheus-config-last-reload-successful, sighup, pca]
level: practitioner
status: gated
description: "Use the Prometheus management API (/-/healthy, /-/ready, /-/reload, /-/quit): wire k8s probes, hot-reload config via SIGHUP or HTTP, validate with promtool, alert on failed reloads."
sources: ["https://prometheus.io/docs/prometheus/latest/management_api/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/", "https://github.com/prometheus-operator/prometheus-operator/tree/main/cmd/prometheus-config-reloader"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Management API and configuration reload

**Goal:** change scrape/rule configuration without restarting (no WAL replay, no gap), and
let orchestrators tell "up" from "ready".

## 1. The endpoints
| Endpoint | Method | Meaning |
|---|---|---|
| `/-/healthy` | GET | process is alive (always 200 once HTTP is up) — liveness probe |
| `/-/ready` | GET | 200 when Prometheus is ready to serve traffic (docs); readiness probe. The 503-during-startup behaviour was not caught in a startup poll here (gated: unconfirmed, source is paywalled or blocked) |
| `/-/reload` | POST/PUT | re-read config and rule files (needs `--web.enable-lifecycle`; GET returns 405 `Only POST or PUT requests allowed`, run) |
| `/-/quit` | POST/PUT | graceful shutdown (needs `--web.enable-lifecycle`) |

```bash
prometheus --config.file=prometheus.yml --web.enable-lifecycle
curl -X POST localhost:9090/-/reload          # or: kill -HUP $(pidof prometheus)
```
Kubernetes (gated: unconfirmed, source is paywalled or blocked; no cluster here):
```yaml
livenessProbe:  {httpGet: {path: /-/healthy, port: 9090}, periodSeconds: 10}
readinessProbe: {httpGet: {path: /-/ready,   port: 9090}, periodSeconds: 5}
startupProbe:   {httpGet: {path: /-/ready,   port: 9090}, failureThreshold: 120, periodSeconds: 10}
```
The startup probe matters: WAL replay on a large instance takes minutes and a liveness probe
with a short threshold would kill it mid-replay, forever.

## 2. What a reload does and does not do
Reloaded: `scrape_configs`, `rule_files`, `alerting`, `remote_write/read`, `global`.
**Not** reloaded: command-line flags (`--storage.tsdb.retention.*`, `--web.*`) — those need a
restart. Changing `global.external_labels` is reloaded; the claim that existing remote-write queues keep
the old labels until resharded was not tested (gated: unconfirmed, source is paywalled or blocked).

A failed reload keeps the **old** config running and returns the parse error (run: an unknown top-level key gave HTTP 500 `failed to reload config ... field bogus_key not found`, `runtimeinfo.reloadConfigSuccess` went false and `up` stayed 1 for every target). Check:
```promql
prometheus_config_last_reload_successful == 0
time() - prometheus_config_last_reload_success_timestamp_seconds > 3600   # stale
```
The gauge is only updated on the next scrape (still 1 one second after the failed reload, 0 after the next 5 s scrape). Alert on the first; the second catches "nobody ever triggers reloads" after a config push.

## 3. Validate before reloading
```bash
promtool check config prometheus.yml      # also checks the rule files that the rule_files globs match
promtool check rules rules/*.yml
```
`promtool check config` reports `FAILED` for a bad key (run) but a `rule_files` glob that matches nothing is silently SUCCESS with no rule files checked, so confirm the "N rule files found" line. Put this in CI and in the deploy step; the reload endpoint returns 500 with the error text on failure, so a deploy script can `curl -f` and abort (run: `curl -f` exit code 22).

## 4. Automatic reload on file change
- Kubernetes (gated: unconfirmed, source is paywalled or blocked; no cluster here): the operator's `prometheus-config-reloader` sidecar watches the ConfigMap/Secret
  mount and POSTs `/-/reload`. ConfigMap updates propagate to the pod with up to
  `kubelet --sync-frequency` (default 60s) delay plus the kubelet cache TTL; `subPath` mounts
  **never** update — mount the whole volume.
- Prometheus 3.x: `--config.auto-reload` (off by default) with `--config.auto-reload-interval` (default 30s) polls the file itself; the interval flag alone does nothing (run: with both flags the log said `Configuration file change detected, reloading the configuration.`).
- systemd: `ExecReload=/bin/kill -HUP $MAINPID` and `systemctl reload prometheus`.

## 5. Protect the lifecycle endpoints
`--web.enable-lifecycle` exposes unauthenticated reload/quit to anyone who can reach :9090.
Front it with the web config file (`basic_auth_users`, TLS) or a NetworkPolicy, or don't
enable it and use SIGHUP from the same host.

## Gotchas
- `/-/reload` with GET returns 405; it must be POST or PUT.
- A reload during a long rule evaluation waiting for the group to finish was not tested (gated: unconfirmed, source is paywalled or blocked).
- Whether a reload resets `for` state for changed rules was not tested here (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `curl -s -o /dev/null -w '%{http_code}' localhost:9090/-/ready` is 200 after startup.
- [ ] Break prometheus.yml, POST reload: response 500, `prometheus_config_last_reload_successful` = 0 after the next scrape, old targets still scraped.
- [ ] Fix it, reload: metric returns to 1 and `/targets` shows the new config.

## Checked
Prometheus 3.15.1 (windows-amd64) run locally with `--web.enable-lifecycle`: GET/POST/PUT `/-/reload` (405, 200, 200), a broken config (500 with message, `reloadConfigSuccess` false, targets still up, gauge flips after next scrape), `curl -f` exit 22, `promtool check config` on a bad key and on an unmatched rule_files glob, `--config.auto-reload` with and without the interval flag, `/-/healthy` and `/-/ready` 200. Docs read: management_api.md at tag v3.15.1. Not run: Kubernetes probes and the config-reloader sidecar, systemd HUP, 503 during startup, `for` state reset on reload.
