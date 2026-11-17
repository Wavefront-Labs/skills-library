---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-otlp-receiver-configuration
name: otel-collector-otlp-receiver-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [otlp-receiver-config, otlp-cors, collector-config, otlp, grpc, browser-telemetry]
level: practitioner
status: docs-checked
description: "Configure the collector OTLP receiver: gRPC/HTTP endpoints (localhost default since v0.104), message size limits, CORS for browsers, TLS, auth and URL paths."
sources: ["https://github.com/open-telemetry/opentelemetry-collector/blob/main/receiver/otlpreceiver/README.md", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/confighttp/README.md", "https://opentelemetry.io/docs/specs/otlp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTLP receiver configuration

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        max_recv_msg_size_mib: 16
        keepalive:
          server_parameters: {max_connection_age: 60s, max_connection_age_grace: 10s}
        tls: {cert_file: /certs/tls.crt, key_file: /certs/tls.key}
        auth: {authenticator: bearertokenauth}
      http:
        endpoint: 0.0.0.0:4318
        cors:
          allowed_origins: ["https://app.example.com", "https://*.example.com"]
          allowed_headers: ["X-Requested-With"]
          max_age: 7200
        traces_url_path: /v1/traces        # defaults /v1/traces, /v1/metrics, /v1/logs
```

## Notes
- The documented default `endpoint` is `localhost:4317` (gRPC) and `localhost:4318` (HTTP). Set `0.0.0.0:<port>` (or another non-loopback address) when clients are outside the host or pod; the README links the collector security best practices on denial-of-service protection for choosing the endpoint.
- gRPC server settings come from `configgrpc`: `keepalive.server_parameters` (`max_connection_age`, `max_connection_age_grace`, `max_connection_idle`, `time`, `timeout`), `keepalive.enforcement_policy`, `max_concurrent_streams`, `max_recv_msg_size_mib`, `read_buffer_size`, `write_buffer_size`, `tls`, `auth`.
- `max_recv_msg_size_mib` is only applied when greater than 0; otherwise grpc-go's own default of 4 MiB applies.
- OTLP/HTTP accepts protobuf and OTLP JSON on the same address; the README says a protocol is disabled by leaving it out of `protocols`. Browsers need `cors` (`allowed_origins` with `*` wildcards, `allowed_headers`, `max_age`).
- `auth` references an extension such as `bearertokenauth`, `basicauth` or `oidc`, declared under `extensions` and enabled in `service.extensions`.

## Gotchas
- The HTTP receiver serves per-signal paths (`traces_url_path`, `metrics_url_path`, `logs_url_path`, default `/v1/traces`, `/v1/metrics`, `/v1/logs`); POST to `[address]/[path]`. The `otlphttp` exporter takes matching `traces_endpoint`, `metrics_endpoint` and `logs_endpoint` URLs.
- Default ports: 4317 gRPC, 4318 HTTP. The client protocol must match the port you enabled.

## Verify
- [ ] A test export from an SDK or another collector is accepted on the configured port, and a browser preflight to the HTTP endpoint returns the CORS headers.

## Checked

2026-10-24. OpenTelemetry Collector otlpreceiver README, configgrpc and confighttp READMEs, receiver factory.go and config.go (main branch), and grpc-go server.go. Confirmed: default endpoints, per-signal URL path options and defaults, CORS options, the gRPC server option list, that `max_recv_msg_size_mib` is applied only when positive, and grpc-go's 4 MiB default. Removed an unconfirmed version gate (v0.104), an unconfirmed load-balancer rationale and the 404 claim.

Method: documentation only; no commands were run.
