---
id: computing-software.cloud-infrastructure-engineering.alertmanager.tls-config-client
name: tls-config-client
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, tls-config, ca-file, min-version]
level: advanced
status: docs-checked
description: "The shared tls_config block for Alertmanager outbound connections: ca_file, cert_file, key_file, server_name, insecure_skip_verify and TLS versions."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tls_config for outbound connections

A `tls_config` configures TLS connections made by Alertmanager, used inside `http_config`, `smtp_tls_config`, email receivers, tracing and Kafka event outputs.

```yaml
tls_config:
  ca_file: /path/to/ca.pem
  cert_file: /path/to/client.pem
  key_file: /path/to/client-key.pem
  server_name: api.example.org
  min_version: TLS12
```

Fields:
- `ca_file`: CA certificate used to validate the server certificate.
- `cert_file` and `key_file`: certificate and key for client certificate authentication to the server.
- `server_name`: ServerName extension indicating the name of the server.
- `insecure_skip_verify`: disables validation of the server certificate; default `false`.
- `min_version`: accepted values `TLS10`, `TLS11`, `TLS12`, `TLS13`. If unset, the Go default minimum, TLS 1.2, applies.
- `max_version`: same accepted values. If unset, the Go default maximum, TLS 1.3, applies.

This is distinct from the server-side TLS in the web configuration file used with `--web.config.file`, which secures Alertmanager's own listener; see the HTTPS and authentication documentation.

For SMTP, `global.smtp_tls_config` sets the default and each email receiver can override it with its own `tls_config`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): shared tls_config fields, TLS version defaults; HTTPS page for the server side.

Method: documentation only; no commands were run.
