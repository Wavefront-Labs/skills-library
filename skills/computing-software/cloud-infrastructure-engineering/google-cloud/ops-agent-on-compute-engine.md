---
id: computing-software.cloud-infrastructure-engineering.google-cloud.ops-agent-on-compute-engine
name: ops-agent-on-compute-engine
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, ops-agent, monitoring-agent, logging-agent, google-cloud-ops-agent, agent-policies, fleet-agent-install, agent-config-yaml, fluent-bit, otel-collector-agent, log-parsing, nginx-metrics, mysql-metrics, prometheus-receiver, process-metrics, windows-event-log, agent-troubleshooting, vm-observability]
level: practitioner
status: docs-checked
description: "Deploy the Ops Agent on Compute Engine fleets: install via OS policy, config.yaml receivers and processors for logs and metrics, Prometheus scraping, restart and checks."
sources: ["https://docs.cloud.google.com/stackdriver/docs/solutions/agents/ops-agent", "https://docs.cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/configuration", "https://docs.cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/managing-agent-policies", "https://docs.cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/prometheus", "https://docs.cloud.google.com/stackdriver/docs/solutions/agents/ops-agent/troubleshooting"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Ops Agent on Compute Engine

**Goal:** every VM ships system metrics, application logs parsed into structured fields,
and app metrics (including Prometheus endpoints) to Cloud Operations, installed and kept current without SSH.

## 1. Install at fleet scale
- The Ops Agent (Fluent Bit + OpenTelemetry Collector) replaced the legacy `google-fluentd` and `stackdriver-agent`; do not run both.
- Fleet: **agent policy** via VM Manager OS policies: `gcloud compute instances ops-agents policies create ops-agents-prod --project=<P> --zone=europe-west1-b --file=policy.yaml` (or the console "Install agents" that generates an OS policy assignment) — selects by labels/zones, installs and pins versions, auto-upgrades if `--agent-rules=type=ops-agent,version=current-major,package-state=installed,enable-autoupgrade=true`.
- Single VM: `curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh && sudo bash add-google-cloud-ops-agent-repo.sh --also-install`.
- User overrides live in `/etc/google-cloud-ops-agent/config.yaml` and are merged with the built-in configuration when the agent restarts.
- The VM's service account needs Logs Writer (`roles/logging.logWriter`) and Monitoring Metric Writer (`roles/monitoring.metricWriter`).
- Do not run the Ops Agent alongside the legacy Logging or Monitoring agents: it can ingest duplicate logs or conflict on metrics. `add-google-cloud-ops-agent-repo.sh` has `--uninstall-standalone-logging-agent` and `--uninstall-standalone-monitoring-agent` to replace them.

## 2. config.yaml (merge over defaults)
```yaml
logging:
  receivers:
    app_json:
      type: files
      include_paths: [/var/log/app/*.json]
      record_log_file_path: true
    journald_sshd: {type: systemd_journald}
  processors:
    parse_app:
      type: parse_json
      time_key: ts
      time_format: "%Y-%m-%dT%H:%M:%S.%L%Z"
    sev:
      type: modify_fields
      fields:
        severity: {move_from: jsonPayload.level, map_values: {info: INFO, warn: WARNING, error: ERROR}}
        labels."app": {static_value: payments}
  service:
    pipelines:
      app:   {receivers: [app_json], processors: [parse_app, sev]}
      system: {receivers: [journald_sshd]}
metrics:
  receivers:
    hostmetrics: {type: hostmetrics, collection_interval: 60s}
    prom_app:
      type: prometheus
      config:
        scrape_configs:
        - job_name: app
          scrape_interval: 30s
          static_configs: [{targets: ['localhost:9100']}]
  processors:
    drop_unwanted:
      type: exclude_metrics
      metrics_pattern: [<METRIC_PREFIX_PATTERN>]
  service:
    pipelines:
      default_pipeline: {receivers: [hostmetrics], processors: [drop_unwanted]}
      prom: {receivers: [prom_app]}
```
- Log receiver types: `files`, `syslog`, `systemd_journald`, `tcp`, `fluent_forward`, `windows_event_log`, plus third-party integrations (see the Ops Agent third-party application list).
- Processors: `parse_json`, `parse_regex` (named groups → fields), `parse_multiline` (stack traces), `modify_fields` (rename/move/static/map, including `severity`), `exclude_logs` (`match_any` filters — drop debug lines at the source, before billing).
- Metrics: `hostmetrics` (cpu, memory, disk, network, swap, processes), the `prometheus` receiver ingests metrics as `prometheus.googleapis.com` metrics, treated as custom metrics for quotas and limits.
- Config changes need an agent restart (`sudo service google-cloud-ops-agent restart`; Windows: `Restart-Service google-cloud-ops-agent -Force`); user config is merged with the built-in config, and redefining a built-in receiver, processor or pipeline with the same identifier overrides it.

## 3. Verify and troubleshoot
- After a restart, `sudo systemctl status google-cloud-ops-agent"*"` should show the "Metrics Agent" and "Logging Agent" components started; see the Ops Agent troubleshooting page for health checks and self logs.
- Check the VM service account roles first when no data arrives.
- `gcloud logging read 'resource.type="gce_instance" jsonPayload.app="payments"' --limit=5` after a restart to confirm pipelines.

## Gotchas
- `config.yaml` **replaces** `default_pipeline` if you redefine it — include `hostmetrics` again or you lose system metrics.
- Legacy agents still installed on old images mean duplicate logs or conflicting metrics; remove them before creating the policy.
- Never commit passwords in config.yaml.
- Pin versions in the prod agent policy and roll upgrades via the policy.

## Verify
- [ ] Every VM matched by the policy label selector reports agent metrics; versions match the policy.
- [ ] A JSON line written to `/var/log/app/test.json` appears in Logs Explorer with `jsonPayload` fields, correct `severity`, and the original timestamp.
- [ ] Prometheus-scraped series appear under `prometheus.googleapis.com`.
- [ ] Stopping the agent on one VM fires the absence alert within the configured window.

## Checked
2026-10-31. Confirmed on the Ops Agent configuration, agent-policies and Prometheus pages and the install script header: overrides merged at restart and same-identifier redefinition, `record_log_file_path`, `parse_json` `time_key`/`time_format`, `parse_multiline`, `exclude_logs`, `exclude_metrics`/`metrics_pattern`, restart and status commands, Logs Writer and Monitoring Metric Writer roles, legacy-agent duplicate warning, uninstall-standalone flags, `prometheus.googleapis.com` custom metrics. Removed: NGINX and MySQL receivers, the Windows path, Private Google Access note, metric names, secret-substitution and Windows event log notes, troubleshooting cause list (not found on fetched pages). Commands checked with check_commands.py.
Method: documentation only; no commands were run.
