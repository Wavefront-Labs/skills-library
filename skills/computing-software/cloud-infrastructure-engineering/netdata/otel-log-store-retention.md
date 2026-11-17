---
id: computing-software.cloud-infrastructure-engineering.netdata.otel-log-store-retention
name: otel-log-store-retention
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, otel-yaml, log-retention, s3-offload]
level: advanced
status: docs-checked
description: "Configure retention and optional S3 offload of Netdata's OpenTelemetry log store in otel.yaml, with credential handling, sizing and the otel-plugin query tool."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/logs/log-storage-and-retention.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Edit `otel.yaml` with `edit-config`, then restart the Agent. `base_dir` defaults to `/var/log/netdata/otel/v2` on package installs.

```
logs:
  retention:
    default:
      max_total_size: "20GB"
      max_age: "30 days"
```

Defaults: `max_files` 100000, `max_total_size` 1GB, `max_age` 7 days.

Offload:

```
remote_storage:
  enabled: true
  uri: "s3://my-bucket/netdata-logs?region=us-east-1"
  read_cache_max_size: "4GB"
```

Put credentials in a root-only (mode 0600) env file loaded by a systemd drop-in (`EnvironmentFile=/etc/netdata/s3-credentials.env` with `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`), never in the URI or `otel.yaml`. Then `systemctl daemon-reload && systemctl restart netdata`.

Gotchas:
- `max_total_size` does not cap total plugin disk use (write-ahead logs, catalogs and download cache are extra).
- Offloaded files are never deleted by the Agent; use an object-storage lifecycle rule.
- If the remote is unreachable, sealed files pile up locally; monitor free disk.
- A query whose offloaded files exceed `read_cache_max_size` fails; downloads time out after 5 minutes.

Sizing: measure `du -sh` on `<base_dir>/logs/index/` after a full day, multiply by desired retention.

Query: `sudo /usr/libexec/netdata/plugins.d/otel-plugin logs --config /etc/netdata/otel.yaml --name checkout --since -1h --filter 'level=error' --limit 1000` (local files only).

## Checked

2026-11-04. Confirmed against the Netdata Log Storage and Retention page: base_dir default, retention defaults and example, remote_storage example, EnvironmentFile credential handling, the four gotchas, the sizing rule and the otel-plugin logs command. Removed the `sudo ./edit-config` form, which the page does not show.

Method: documentation only; no commands were run.
