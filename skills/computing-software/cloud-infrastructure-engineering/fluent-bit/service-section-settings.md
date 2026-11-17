---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.service-section-settings
name: service-section-settings
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, service-section, flush, grace, http-server, log-level, parsers-file]
level: practitioner
status: docs-checked
description: "Set Fluent Bit's global service keys in YAML: flush, grace, log_level, the HTTP server, health check, hot reload and file includes."
sources: ["https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/yaml/service-section"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The service section

The `service` section of the YAML configuration sets global properties. Commonly used keys and their defaults:

| Key | Default | Meaning |
| --- | --- | --- |
| `flush` | `1` | flush time in `seconds.nanoseconds`; when the engine flushes ingested records to outputs |
| `grace` | `5` | seconds the engine waits on exit |
| `daemon` | `off` | background process; do not enable under a systemd unit such as the packaged one |
| `log_level` | `info` | `off`, `error`, `warn`, `info`, `debug`, `trace` (cumulative; `trace` needs a build with `FLB_TRACE`) |
| `log_file` | none | absolute path; default is stderr |
| `http_server` | `off` | built-in monitoring and control server |
| `http_listen` | `0.0.0.0` | HTTP server interface |
| `http_port` | `2020` | HTTP server port |
| `health_check` | `off` | registers a health endpoint; needs `http_server` |
| `hot_reload` | `on` | reload configuration on SIGHUP |
| `parsers_file` | none | standalone parsers file(s) |
| `plugins_file` | none | external `.so` plugins |
| `streams_file` | none | stream processor rules |
| `scheduler.base` / `scheduler.cap` | `5` / `2000` | retry backoff base and cap in seconds |
| `multiline_buffer_limit` | `2MB` | default limit for multiline parsers |

Health thresholds: `hc_period` `60`, `hc_errors_count` `5`, `hc_retry_failure_count` `5`.

```yaml
service:
  flush: 1
  log_level: info
  http_server: true
  http_listen: 0.0.0.0
  http_port: 2020
  hot_reload: on
pipeline:
  inputs:
    - name: random
  outputs:
    - name: stdout
      match: '*'
```

## Checked

2026-11-03. Confirmed on the Fluent Bit YAML Service section page: every key, default and value listed in the table, the health thresholds (hc_period 60, hc_errors_count 5, hc_retry_failure_count 5), and the configuration example. Fixed: the log_level default is `info`.

Method: documentation only; no commands were run.
