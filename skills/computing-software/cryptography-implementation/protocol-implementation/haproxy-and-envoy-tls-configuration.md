---
id: computing-software.cryptography-implementation.protocol-implementation.haproxy-and-envoy-tls-configuration
name: haproxy-and-envoy-tls-configuration
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, haproxy-tls, haproxy, envoy, tls-configuration, upstream-tls, sds, certificate-reload, tls-server-config]
level: practitioner
status: docs-checked
description: "Configure TLS in HAProxy and Envoy: bind and server SSL options, ssl-default settings, hot certificate updates, and the upstream verification defaults that bite."
sources: ["https://docs.haproxy.org/2.8/configuration.html#5.1", "https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/transport_sockets/tls/v3/tls.proto", "https://www.haproxy.com/documentation/haproxy-runtime-api/reference/set-ssl-cert/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAProxy and Envoy TLS configuration

## HAProxy
The cipher lists below are examples only; choose them from current vendor or Mozilla guidance.
```
global
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-server-options ssl-min-ver TLSv1.2
    ssl-server-verify required

frontend https
    bind :443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1      # directory: one PEM per site (cert+chain+key)
    http-request set-header X-Forwarded-Proto https

backend api
    server s1 10.0.0.10:8443 ssl verify required ca-file /etc/haproxy/ca/internal.pem sni str(api.internal) check-sni api.internal
```
- Certificate selection is by SNI across files in the `crt` directory; `crt-list` adds per-cert options.
- Hot update without reload: Runtime API `set ssl cert /etc/haproxy/certs/site.pem <<\n<pem>\n` then
  `commit ssl cert /etc/haproxy/certs/site.pem`.
- mTLS on bind: `ca-file clients.pem verify required`; pass identity with `%[ssl_c_s_dn]` in headers.
- Old configs often have `verify none` on servers: that disables upstream certificate checks.

## Envoy
Downstream (listener):
```yaml
transport_socket:
  name: envoy.transport_sockets.tls
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.DownstreamTlsContext
    common_tls_context:
      tls_params: {tls_minimum_protocol_version: TLSv1_2}
      tls_certificate_sds_secret_configs: [{name: site-cert, sds_config: {path_config_source: {path: /etc/envoy/sds.yaml}}}]
      alpn_protocols: ["h2", "http/1.1"]
```
Upstream (cluster):
```yaml
    "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext
    sni: api.internal
    common_tls_context:
      validation_context:
        trusted_ca: {filename: /etc/envoy/ca/internal.pem}
        match_typed_subject_alt_names:
          - san_type: DNS
            matcher: {exact: api.internal}
```
**Envoy does not verify upstream certificates unless `validation_context` is set**, and does not check names unless
`match_typed_subject_alt_names` is configured. SDS lets certificates rotate without restarts.

## Verify
- [ ] Upstream with a wrong-name certificate fails in both proxies.
- [ ] Certificate rotation via Runtime API / SDS works without dropping connections.

## Checked

- Date: 2026-11-02.
- Confirmed against: HAProxy 2.8 configuration manual (ssl-min-ver, no-tls-tickets, ssl-default-bind-ciphersuites, ssl-default-server-options, ssl-server-verify [none|required], crt, crt-list, ca-file, verify required, check-sni, sni, alpn, ssl_c_s_dn); HAProxy runtime API page (set ssl cert with a heredoc-style payload, then commit ssl cert); Envoy tls.proto, common.proto and config_source.proto reference (DownstreamTlsContext, UpstreamTlsContext, tls_minimum_protocol_version, tls_certificate_sds_secret_configs, path_config_source, alpn_protocols, validation_context, trusted_ca, match_typed_subject_alt_names with san_type, and that server certificate verification is off unless trusted_ca is configured).
- Removed: nothing; the cipher lists were relabelled as examples because no fetched page endorses them.

Method: documentation only; no commands were run.
