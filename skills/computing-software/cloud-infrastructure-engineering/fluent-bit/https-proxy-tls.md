---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.https-proxy-tls
name: https-proxy-tls
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, http-proxy, tls-proxy, ca-file, tls-proxy-verify, corporate-ca]
level: advanced
status: docs-checked
description: "Verify an HTTPS proxy's certificate in Fluent Bit with the tls.proxy keys, independent of destination TLS."
sources: ["https://docs.fluentbit.io/manual/administration/http-proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS to an HTTPS proxy

When `HTTP_PROXY` uses the `https` scheme, Fluent Bit opens a TLS connection to the proxy itself before issuing the HTTP CONNECT request. That proxy-side TLS is configured separately from the destination's `tls.*` keys, which verify the destination.

| Key | Default | Meaning |
| --- | --- | --- |
| `tls.proxy.ca_file` | none | absolute path to the CA certificate that verifies the proxy |
| `tls.proxy.ca_path` | none | absolute directory scanned for proxy CA certificates |
| `tls.proxy.verify` | `on` | force certificate validation of the proxy |
| `tls.proxy.verify_hostname` | `on` | force hostname verification of the proxy |

These apply only to output plugins (supported in v5.1 or later) and are set on the output like any `tls.*` key. If both `tls.proxy.ca_file` and `tls.proxy.ca_path` are unset, the system default trust store verifies the proxy certificate.

Example for a proxy signed by a private or corporate CA:

```yaml
pipeline:
  outputs:
    - name: http
      match: '*'
      host: backend.example.com
      port: 443
      tls: on
      tls.proxy.ca_file: /etc/certs/proxy-ca.crt
```

Setting up the proxy variable itself is in `computing-software.cloud-infrastructure-engineering.fluent-bit.http-proxy-environment`.

## Checked

2026-11-03. Confirmed on the Fluent Bit HTTP proxy page (TLS to the proxy): the four tls.proxy keys with defaults, output-only scope, v5.1 support, system trust store fallback, and the proxy-ca.crt example. Removed: unsourced production advice.

Method: documentation only; no commands were run.
