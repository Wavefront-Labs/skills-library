---
id: computing-software.cloud-infrastructure-engineering.google-cloud.ops-agent-custom-logs-otlp-and-version-pinning
name: ops-agent-custom-logs-otlp-and-version-pinning
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, ops-agent, ops-agent-custom-logs, file-receiver, ops-agent-otlp-receiver, otlp-ingest, ops-agent-upgrade, agent-version-pinning]
level: practitioner
status: docs-checked
description: "Configure the Ops Agent beyond defaults: tail custom application log files with parsing, accept OTLP metrics and traces from apps, and pin agent versions across a fleet."
sources: ["https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/configuration", "https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/otlp", "https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/installation", "https://cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/managing-agent-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ops Agent: custom logs, OTLP and version pinning

Config file: `/etc/google-cloud-ops-agent/config.yaml` (merged with built-in defaults). Restart
after edits: `sudo systemctl restart google-cloud-ops-agent`.

## 1. Custom log files
```yaml
logging:
  receivers:
    orders_app:
      type: files
      include_paths: [/var/log/orders/*.log]
      exclude_paths: [/var/log/orders/debug-*.log]
      record_log_file_path: true
  processors:
    orders_json:
      type: parse_json
      time_key: ts
      time_format: "%Y-%m-%dT%H:%M:%S.%L%z"
    orders_severity:
      type: modify_fields
      fields:
        severity: {copy_from: jsonPayload.level}
  service:
    pipelines:
      orders:
        receivers: [orders_app]
        processors: [orders_json, orders_severity]
```
Non-JSON logs: `type: parse_regex` with named groups. Multiline stack traces:
`type: parse_multiline` with `match_any` rules for java/python/go.

## 2. OTLP receiver (apps send metrics and traces to the local agent)
```yaml
combined:
  receivers:
    otlp:
      type: otlp
      grpc_endpoint: 127.0.0.1:4317
      metrics_mode: googlemanagedprometheus     # the default; googlecloudmonitoring sends custom metrics
metrics:
  service:
    pipelines:
      otlp: {receivers: [otlp]}
traces:
  service:
    pipelines:
      otlp: {receivers: [otlp]}
```
Apps use the standard OTel SDK exporter to `localhost:4317`; no credentials in the app.

## 3. Install, pin, upgrade
```bash
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install --version=2.*.*     # pin major version
sudo bash add-google-cloud-ops-agent-repo.sh --also-install --version=<MAJOR>.<MINOR>.<PATCH>     # exact pin
dpkg -l google-cloud-ops-agent || rpm -q google-cloud-ops-agent
```
Fleet: manage with agent policies (`gcloud beta compute instances ops-agents policies create`; the command is in the beta track per the managing-agent-policies page) and roll upgrades by label (canary, then all).
Bake the agent into images for MIGs.

## Gotchas
- Invalid YAML can stop the agent from loading the config: check `systemctl status` after each restart.
- Unpinned `--version=latest` in startup scripts gives a fleet of mixed versions.
- `metrics_mode` defaults to `googlemanagedprometheus`; `googlecloudmonitoring` sends custom metrics instead, which changes how ingestion is billed (see the vendor's pricing page).

## Verify
- [ ] Logs Explorer shows the new log entries with parsed fields and correct severity.
- [ ] `sudo systemctl status 'google-cloud-ops-agent*'` all active; agent version uniform across the fleet.

## Checked
2026-10-28. Confirmed on the Ops Agent configuration, OTLP, installation and managing-agent-policies pages: config path `/etc/google-cloud-ops-agent/config.yaml`, `systemctl restart`, `files` receiver options (`exclude_paths`, `record_log_file_path`), `parse_regex`, `parse_multiline`, `match_any`, `time_format`, otlp receiver `grpc_endpoint` (default 0.0.0.0:4317) and `metrics_mode` (default `googlemanagedprometheus`, alternative `googlecloudmonitoring`), `--version=2.*.*` pinning and exact MAJOR.MINOR.PATCH.
Fixed: `gcloud compute instances ops-agents policies` is documented as `gcloud beta compute instances ops-agents`.
Removed: example exact version 2.52.0, the agent engine validation binary path, root/SELinux note, and the log_name check.
Method: documentation only; no commands were run.
