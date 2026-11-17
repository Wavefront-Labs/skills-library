---
id: computing-software.cloud-infrastructure-engineering.alertmanager.tracing-config
name: tracing-config
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, tracing, otlp, sampling-fraction]
level: advanced
status: docs-checked
description: "Alertmanager top-level tracing configuration: client_type, endpoint, sampling_fraction, insecure, tls_config, headers, compression and timeout defaults."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tracing configuration

An optional block configures distributed tracing for Alertmanager. The `<tracing_config>` section of the reference documents these fields:

```yaml
tracing:
  client_type: grpc
  endpoint: collector.example.org:4317
  sampling_fraction: 0.1
  compression: gzip
  timeout: 5s
```

Fields and defaults:
- `client_type`: `http` or `grpc`; default `grpc`.
- `endpoint`: the tracing endpoint; default empty.
- `sampling_fraction`: default `0.0`.
- `insecure`: whether to disable TLS; default `false`.
- `tls_config`: TLS settings for the client.
- `http_headers`: custom headers sent with trace exports.
- `compression`: default `gzip`.
- `timeout`: default `0s`.

Caveat: the file skeleton in the reference lists the top-level key as `traciing`, which appears to be a typo in the documentation; the section is titled Tracing Configuration and the block type is `<tracing_config>`.


When `use_aws_http_client` is enabled on an SNS receiver, tracing is disabled for SNS requests.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): tracing_config fields and defaults, SNS use_aws_http_client note. Removed: closing advice to validate with amtool and the 'nothing is traced until set' inference.

Method: documentation only; no commands were run.
