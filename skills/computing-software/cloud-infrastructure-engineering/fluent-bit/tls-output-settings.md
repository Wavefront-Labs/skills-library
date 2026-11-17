---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.tls-output-settings
name: tls-output-settings
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, tls, ssl, ca-file, tls-verify, tls-vhost, certificates]
level: practitioner
status: docs-checked
description: "Enable TLS on a network output and set CA, verification, SNI and version keys."
sources: ["https://docs.fluentbit.io/manual/administration/transport-security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS on outputs

Input and output plugins that perform network I/O can enable TLS through `tls.*` properties set in the plugin section.

| Property | Default | Meaning |
| --- | --- | --- |
| `tls` | `off` | enable TLS |
| `tls.verify` | `on` | force certificate validation |
| `tls.verify_hostname` | `off` | force verification of host names |
| `tls.ca_file` | none | absolute path to the CA certificate file |
| `tls.ca_path` | none | absolute path scanned for certificate files |
| `tls.crt_file` / `tls.key_file` | none | absolute paths to the certificate and private key; optional `tls.key_passwd` |
| `tls.vhost` | none | host name used for the TLS SNI extension |
| `tls.min_version` / `tls.max_version` | none | TLS version bounds |
| `tls.ciphers` | none | TLS ciphers up to TLSv1.2 |
| `tls.debug` | `1` | verbosity: `0` none, `1` error, `2` state change, `3` informational, `4` verbose |
| `tls.crl_file` | none | CRL file in PEM format; revoked certificates are rejected (v5.1.3 or later) |

```yaml
pipeline:
  outputs:
    - name: http
      match: '*'
      host: logs.example.com
      port: 443
      tls: on
      tls.verify: on
      tls.verify_hostname: on
      tls.ca_file: /etc/certs/ca.crt
```

By default host names are not verified automatically. A certificate whose Subject Alternative Name covers only one DNS name fails when `tls.verify_hostname` is on and you connect by another name, with an error such as `certificate verify failed`.

When the target is an IP address, Fluent Bit sends no SNI extension, consistent with RFC 6066, but certificate validation still applies against the IP address. If the server requires SNI or uses a hostname-based certificate, use a hostname as the target and set `tls.vhost` if needed.

Outputs going through an HTTPS proxy use separate `tls.proxy.ca_file`, `tls.proxy.ca_path`, `tls.proxy.verify` and `tls.proxy.verify_hostname` (v5.1 or later, both verify keys default `on`).

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs transport security (TLS) page (raw markdown, read in full).
