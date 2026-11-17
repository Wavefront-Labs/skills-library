---
id: computing-software.database-administration.time-series-databases.influxdb-tls-hardening
name: influxdb-tls-hardening
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-auth, influxdb-tls-hardening, influxdb, flux]
level: practitioner
status: docs-checked
description: "Serve InfluxDB over TLS and limit exposure."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/security/enable-tls/
  - https://docs.influxdata.com/influxdb/v2/reference/config-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS and network hardening

**Goal:** Serve InfluxDB over TLS and limit exposure.

## Steps
- Start with certificates: `influxd --tls-cert=/etc/ssl/influx.crt --tls-key=/etc/ssl/influx.key` (or `INFLUXD_TLS_CERT` / `INFLUXD_TLS_KEY`).
- `--tls-min-version` defaults to `1.2`; `--tls-strict-ciphers` restricts the cipher list.
- Bind to a private interface: `--http-bind-address=10.0.0.5:8086` (default `:8086`).
- With a self-signed certificate, `curl --insecure` skips verification for testing; use a CA-issued certificate in production.
- Firewall port 8086 to known writers.
- Set `--reporting-disabled` (`INFLUXD_REPORTING_DISABLED`) if telemetry is not wanted.

**Gotcha:** Running over plain HTTP sends bearer tokens in clear text on every request.

## Verify
- `curl --verbose https://host:8086/api/v2/ping` shows a TLS handshake with a trusted certificate.
- Plain HTTP on the same port is refused.

## Checked

2026-11-03. Confirmed in the enable-TLS page (`--tls-cert`, `--tls-key`, ping check, `curl --insecure`) and the `influxd` config options page (env vars `INFLUXD_TLS_CERT`, `INFLUXD_TLS_KEY`, `INFLUXD_TLS_MIN_VERSION`, `--tls-strict-ciphers`, `--http-bind-address`, `--reporting-disabled`). Removed: the reverse-proxy advice, the `--skip-verify` flag, the token-header remark and the `/health` check (not on the pages read).
Method: documentation only; no commands were run.

