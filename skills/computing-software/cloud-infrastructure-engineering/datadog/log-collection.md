---
id: computing-software.cloud-infrastructure-engineering.datadog.log-collection
name: log-collection
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, log-collection, logs-agent, file-tail, logs-config]
level: practitioner
status: docs-checked
description: "Enable the Logs Agent and tail files, TCP/UDP, journald or Windows events with source and service, plus multi-line rules and permissions."
sources: ["https://docs.datadoghq.com/agent/logs/", "https://docs.datadoghq.com/agent/logs/advanced_log_collection/", "https://docs.datadoghq.com/agent/configuration/agent-status-page/", "https://docs.datadoghq.com/logs/guide/log-collection-troubleshooting-guide/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log collection with the Agent
Goal: ship logs from a host Agent to Datadog. (For Kubernetes and Docker use their dedicated log collection pages.)

Log collection is off by default. In `datadog.yaml`:

```yaml
logs_enabled: true
```

or `DD_LOGS_ENABLED=true`. Then create `<CUSTOM_LOG_SOURCE>.d/conf.yaml` under the Agent's `conf.d/` directory (readable by the Datadog user), restart the Agent, and look for the source under Checks in `datadog-agent status`.

```yaml
# conf.d/myapp.d/conf.yaml
logs:
  - type: file
    path: "<PATH_LOG_FILE>/<LOG_FILE_NAME>.log"
    service: "<APP_NAME>"
    source: "<SOURCE>"
    log_processing_rules:
      - type: multi_line
        name: new_log_start_with_date
        pattern: \d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])
```

- Valid `type` values: `tcp`, `udp`, `file`, `windows_event`, `docker`, `journald`. `tcp`/`udp` need `port`; `file` and `journald` need `path`; `windows_event` needs `channel_path`.
- `multi_line` rules aggregate lines into one entry until the pattern matches again (for logs not sent as JSON).
- A log line must end with a newline (`\n` or `\r\n`); otherwise the Agent waits and does not send it.
- `exclude_paths` (Agent 6.18+) excludes files matched by a wildcard `path`. The `beginning` start position does not support wildcard paths.
- HTTPS is the default transport from Agent 6.19/7.19; `logs_config.force_use_http: true` is shown in the docs' example.
- On Windows, `ddagentuser` needs read access to the log file; on Linux the Agent user must be able to read the file and traverse its folder (for example `chmod o+rx` on the directory, per the troubleshooting guide).
- The status page Logs Agent section shows counters such as `LogsProcessed` and `LogsSent`.

Gotcha: permission errors on log files are the most common cause of missing logs; see the permission section of the log collection troubleshooting guide.

## Verify
- `LogsProcessed` and `LogsSent` increase in `datadog-agent status` and entries appear in Log Explorer with the configured service.

## Checked
2026-11-03. Confirmed against the Agent log collection, Advanced Log Collection, Agent status page and log collection troubleshooting pages. Removed: `usermod -a -G adm dd-agent`, `max_message_size_bytes`, the `BytesSent` counter and the `status | grep` pipeline (none confirmed), logrotate advice, and "empty source means unparsed" wording.
Method: documentation only; no commands were run.
