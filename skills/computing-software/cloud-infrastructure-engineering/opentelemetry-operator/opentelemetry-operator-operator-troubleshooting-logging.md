---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-operator-troubleshooting-logging
name: opentelemetry-operator-operator-troubleshooting-logging
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, troubleshooting, zap-devel, zap-log-level, json-logs, debug-logging]
level: intro
status: docs-checked
description: "Change the operator log format and verbosity with the zap flags, including custom JSON key names, to debug reconciliation and startup issues."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/troubleshooting/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Operator log format and debugging

By default the operator logs in a console format, with startup lines such as noting whether Prometheus CRDs and OpenShift CRDs are installed, whether `WATCH_NAMESPACE` is set (otherwise it watches all namespaces), and whether webhooks are disabled (`ENABLE_WEBHOOKS=false` runs in an unsupported mode).

Flags to customize logs:
- `--zap-devel`: development defaults (console encoder, Debug level, stacktraces at Warn); production defaults are JSON encoder, Info, stacktraces at Error.
- `--zap-encoder`: `json` or `console`.
- `--zap-log-level`: `debug`, `info`, `error`, or an integer above zero for increasing verbosity.
- `--zap-stacktrace-level`: `info`, `error` or `panic`.
- `--zap-time-encoding`: `epoch` (default), `millis`, `nano`, `iso8601`, `rfc3339`, `rfc3339nano`.
- Only with `--zap-encoder=json`: `zap-message-key`, `zap-level-key`, `zap-time-key`, `zap-level-format`.

Example: `--zap-encoder=json --zap-message-key="msg" --zap-level-key="severity" --zap-time-key="timestamp" --zap-level-format="uppercase"` produces lines like `{"severity":"INFO","timestamp":"...","logger":"setup","msg":"starting manager"}`.

Add these to the manager container args. The manager configuration reference also lists `zap` keys (message-key, level-key, time-key, level-format) for the config file, environment variables and flags.

## Checked

2026-11-04. Confirmed against docs/troubleshooting/README.md: the console default and startup lines, the --zap-devel, --zap-encoder, --zap-log-level, --zap-stacktrace-level and --zap-time-encoding options and values, the four JSON-only key and format options, and the example flags and JSON output. Confirmed against docs/reference/configuration.md: zap message-key, level-key, time-key and level-format keys with matching flags and environment variables. Removed the unconfirmed advice about Collector pod logs and the claim that all zap flags have config file keys.

Method: documentation only; no commands were run.
