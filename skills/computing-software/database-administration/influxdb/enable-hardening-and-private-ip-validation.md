---
id: computing-software.database-administration.influxdb.enable-hardening-and-private-ip-validation
name: enable-hardening-and-private-ip-validation
category: computing-software
field: database-administration
product: influxdb
tags: [security, hardening-enabled, private-ip, health-auth-mode, ssrf]
level: advanced
status: docs-checked
description: "Turn on hardening-enabled to block Flux, template and notification HTTP requests to private IPs and restrict /health detail to operators."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/security/enable-hardening/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Start `influxd` with `--hardening-enabled` (config option `hardening-enabled`) to enable extra protections.

Private IP validation: functions like `to()`, `from()`, `http.post()`, template fetching and notification endpoints make HTTP requests. With the feature on, InfluxDB first verifies the target URL does not resolve to a private address: IPv4 loopback 127.0.0.0/8, RFC1918 (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16), RFC3927 169.254.0.0/16, IPv6 loopback ::1/128, link-local fe80::/10 and unique local fc00::/7.

If your environment must call private addresses (for example an internal webhook), do not use `--hardening-enabled`; use egress firewalling instead.

Restricted health details (OSS v2.10+): `/health` and `/ready` can include file paths and permission errors. With hardening, only callers with operator permissions see check messages; others get names and statuses. HTTP status codes do not change, so unauthenticated probes still work. Control this separately with `health-auth-mode`:

```sh
influxd --hardening-enabled --health-auth-mode=disabled
```

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/admin/security/enable-hardening/
- Scope: address ranges, health behaviour from v2.10 and the combined flag example.
Method: documentation only; no commands were run.
