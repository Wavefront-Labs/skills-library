---
id: computing-software.cloud-infrastructure-engineering.datadog.live-processes
name: live-processes
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, process-monitoring, live-processes, process-agent, process-collection]
level: practitioner
status: docs-checked
description: "Enable Datadog Live Processes collection, scrub sensitive command-line arguments, and alert on process counts or the process.up check."
sources: ["https://docs.datadoghq.com/infrastructure/process/", "https://docs.datadoghq.com/monitors/types/process/", "https://docs.datadoghq.com/monitors/types/process_check/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live Processes and process monitoring
Goal: see process-level resource use and alert on process counts.

Enable on Linux or Windows in the Agent main config file, then restart the Agent:

```yaml
process_config:
  process_collection:
    enabled: true
```

- Environment variables override the config file.
- Docker: pass `-v /etc/passwd:/etc/passwd:ro` and `-e DD_PROCESS_CONFIG_PROCESS_COLLECTION_ENABLED=true`; to collect container data in the standard install, the `dd-agent` user needs access to `docker.sock`. A containerised Agent still collects host processes.
- Helm: under `datadog:` set `processAgent.enabled: true` and `processAgent.processCollection: true`.
- ECS Fargate: set `DD_PROCESS_AGENT_PROCESS_COLLECTION_ENABLED` to `true` in the Agent container definition.
- I/O and open-file stats need the system-probe process module (`system_probe_config.process_config.enabled: true` in `system-probe.yaml`).
- Argument scrubbing is on by default: values of arguments matching sensitive words are hidden. Add your own words, merged with the defaults, under `process_config` in `datadog.yaml`; wildcards are allowed but a lone `*` is not, and words may contain only alphanumerics, underscores or `*`:

```yaml
process_config:
  scrub_args: true
  custom_sensitive_words: ['personal_key', '*token', 'sql*', '*pass*d*']
```

  `scrub_args: false` disables scrubbing; `strip_proc_arguments: true` removes all arguments. Helm equivalents are `DD_SCRUB_ARGS`, `DD_CUSTOM_SENSITIVE_WORDS` and `DD_STRIP_PROCESS_ARGS`.
- Live Process Monitor (Monitors > New Monitor > Live Process) alerts on the count of a group of processes across hosts or tags, filtered by tags or by text search on command line and user (`AND`, `OR`, `NOT`). It uses a rolling window and the docs discourage windows under 5 minutes.
- Process check monitor watches the Agent check `process.up`; thresholds are set at the Agent level on the check, and groups are `host` and `process`. It supports check alerts (consecutive statuses) and cluster alerts (percent of checks in a status).

Gotcha: keep scrubbing on; command lines can contain secrets in argument values.

## Verify
- Infrastructure > Processes lists the process after the Agent restart.

## Checked
2026-11-03. Confirmed against the Live Processes, Live Process Monitor and Process Check monitor pages. Removed: the `avg:system.processes.number` query, `conf.d/process.d` path and `[OK]` status check, `DD_PROCESS_AGENT_ENABLED=true` for Kubernetes (docs show Helm `processAgent` settings), the `custom_sensitive_words: ["token", "secret"]` values, and the data-volume and documentation advice.
Method: documentation only; no commands were run.
