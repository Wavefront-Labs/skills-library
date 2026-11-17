---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.tls-and-mtls-configuration
name: tls-and-mtls-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, security, tls, mtls, certificates, receiver]
level: practitioner
status: docs-checked
description: "Enable TLS and mutual TLS on Collector receivers and exporters with the tls settings block."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For production, the page says to use TLS certificates, or mTLS for mutual authentication. Its example creates a CA and a certificate with `cfssl`: `cfssl genkey -initca csr.json | cfssljson -bare ca`, then `cfssl gencert -ca ca.pem -ca-key ca-key.pem csr.json | cfssljson -bare cert`, producing `ca.pem`, `cert.pem` and `cert-key.pem`.

Receiver TLS uses `cert_file` and `key_file`:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        tls:
          cert_file: /path/to/server-cert.pem
          key_file: /path/to/server-key.pem
          client_ca_file: /path/to/ca.pem
```

Adding `client_ca_file` makes it mTLS. An exporter verifies the server with `ca_file`, and presents a client certificate with `cert_file` and `key_file`:

```yaml
exporters:
  otlp_grpc:
    endpoint: remote-collector:4317
    tls:
      ca_file: /path/to/ca.pem
      cert_file: /path/to/client-cert.pem
      key_file: /path/to/client-key.pem
```

Other settings: `insecure` (not for production), `insecure_skip_verify`, `min_version` and `max_version` (for example `1.2`), and `reload_interval`, the duration after which the certificate is reloaded.

For server-only TLS, a receiver needs just `cert_file` and `key_file`, and an exporter needs just `ca_file` to verify the server certificate. The page generated the CA with `O` set to "OpenTelemetry Example" and hosts `localhost` and `127.0.0.1` in `csr.json`, using RSA 2048. Some exporters require x.509 certificates to establish secure connections.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
