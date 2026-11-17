---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.tls-input-and-mtls
name: tls-input-and-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, tls, mtls, tls-verify-client-cert, http-input, self-signed]
level: advanced
status: docs-checked
description: "Serve TLS on an input plugin and require client certificates for mutual TLS."
sources: ["https://docs.fluentbit.io/manual/administration/transport-security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS on inputs and mutual TLS

Input plugins that perform network I/O can enable TLS. To use TLS on an input you must provide both a certificate and a private key with `tls.crt_file` and `tls.key_file`. Inputs documented as TLS-capable include Docker Events, Elasticsearch (Bulk API), Forward, Health, HTTP, Kubernetes Events, MQTT, NGINX Exporter Metrics, OpenTelemetry, Prometheus Scrape Metrics, Prometheus Remote Write, Splunk (HTTP HEC), Syslog and TCP.

Command-line example for the HTTP input with a self-signed pair:

```shell
fluent-bit -i http \
           -p port=9999 \
           -p tls=on \
           -p tls.verify=off \
           -p tls.crt_file=self_signed.crt \
           -p tls.key_file=self_signed.key \
           -o stdout \
           -m '*'
```

The docs set `tls` and `tls.verify` this way for demonstration only and say to always enable verification in production environments.

A test pair can be generated with openssl: `openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout self_signed.key -out self_signed.crt -subj "/CN=test.host.net"` (the docs example uses a 30-day expiry and an unencrypted key).

For mutual TLS, set `tls.verify_client_cert` (default `off`, inputs only). It requires and verifies the certificate presented by the connecting client. In v5.1.3 or later, enabling it also forces certificate validation for the connection even when `tls.verify` is `off`, and Fluent Bit logs a warning for that combination.

```yaml
pipeline:
  inputs:
    - name: http
      port: 9999
      tls: on
      tls.crt_file: /etc/certs/server.crt
      tls.key_file: /etc/certs/server.key
      tls.verify_client_cert: on
```

Fluent Bit 5.1 and later reloads certificates from disk without a restart when it creates a new TLS session; established sessions keep the old context until they reconnect.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs transport security (TLS) page (raw markdown, read in full).
