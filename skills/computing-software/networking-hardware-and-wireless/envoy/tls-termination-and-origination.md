---
id: computing-software.networking-hardware-and-wireless.envoy.tls-termination-and-origination
name: tls-termination-and-origination
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, tls, ssl, downstream-tls-context, upstream-tls-context, alpn, sni, session-resumption, crl]
level: practitioner
status: docs-checked
description: "Configure TLS termination in Envoy listeners and TLS origination to clusters, including ALPN, SNI, verification and session resumption."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/security/ssl.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls termination and origination
Envoy performs TLS termination in listeners (`DownstreamTlsContext` on a filter chain transport socket) and TLS origination toward clusters (`UpstreamTlsContext`). Features in the docs: configurable ciphers and protocol versions, client certificates for upstream, certificate verification (chain, subject name, hash pinning), CRL checking if a list is provided, ALPN on listeners (the HCM uses it to choose HTTP/1.1 or HTTP/2), SNI on both sides, session resumption via TLS tickets (can work across hot restarts and parallel Envoys), and BoringSSL private key methods for offloading signing and decryption.

```yaml
transport_socket:
  name: envoy.transport_sockets.tls
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.DownstreamTlsContext
    common_tls_context:
      alpn_protocols: [h2, http/1.1]
      tls_certificates:
      - certificate_chain: { filename: /etc/envoy/tls.crt }
        private_key: { filename: /etc/envoy/tls.key }
```
Gotchas: by default the directories containing secrets are watched for filesystem move events (`watched_directory` sets this explicitly), and SDS rotates certificates without a restart. Certificate verification, upstream or downstream, is not enabled unless the validation context names one or more trusted CA certificates. Verify with `GET /certs` on the admin port.

## Checked

2026-11-03. Confirmed against: ssl.rst (features, SNI, verification only with trusted CAs) and secret.rst (watched directories). Removed or corrected: the file-read-at-load claim, the sni-less failure claim and the openssl verify step.

Method: documentation only; no commands were run.
