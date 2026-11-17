---
id: computing-software.cloud-infrastructure-engineering.thanos.sidecar-prometheus-http-client
name: sidecar-prometheus-http-client
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-sidecar, http-client, basic-auth, tls-config]
level: advanced
status: docs-checked
description: "Give the sidecar credentials, TLS and transport settings for reaching a protected Prometheus."
sources: ["https://thanos.io/tip/components/sidecar.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sidecar Prometheus HTTP client

Configure how the sidecar calls Prometheus with YAML in `--prometheus.http-client` (inline) or `--prometheus.http-client-file` (path).

```yaml
basic_auth:
  username: ""
  password: ""
  password_file: ""
bearer_token: ""
bearer_token_file: ""
proxy_url: ""
tls_config:
  ca_file: ""
  cert_file: ""
  key_file: ""
  server_name: ""
  insecure_skip_verify: false
transport_config:
  max_idle_conns: 0
  max_idle_conns_per_host: 0
  idle_conn_timeout: 0
  response_header_timeout: 0
```

Use it when Prometheus sits behind basic auth, a bearer token, a proxy or TLS. Durations are strings such as `90s` or `2m`.

Timeouts for reading Prometheus config: `--prometheus.get_config_interval=30s` and `--prometheus.get_config_timeout=30s`.

## Checked

2026-11-03. Confirmed against the Thanos Sidecar page (components/sidecar.md) and the Thanos troubleshooting page: Store API over remote-read, 2h upload, block-duration requirement for upload, reloader flags, HTTP client config, upload-compacted, defaults. Fixed: the 2h fixed-block requirement applies to sidecar upload only. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
