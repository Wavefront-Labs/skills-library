---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-web-tls-server-config
name: prometheus-web-tls-server-config
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, web-config, tls-server-config, cipher-suites, min-tls-version, http-server-config, security-headers, exporter-toolkit, node-exporter]
level: practitioner
status: gated
description: "Serve Prometheus and exporters over TLS with web.yml: tls_server_config (min_version, ciphers, curves, cert reload), http2 and security headers."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/https/", "https://github.com/prometheus/exporter-toolkit/blob/master/docs/web-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS server config (web.yml)

Same file format for Prometheus, Alertmanager, Pushgateway, node_exporter and every exporter built on
exporter-toolkit; pass it with `--web.config.file=web.yml`.

```yaml
tls_server_config:
  cert_file: /etc/prometheus/tls/tls.crt       # full chain, server cert first
  key_file: /etc/prometheus/tls/tls.key
  min_version: TLS12                           # TLS10..TLS13; default TLS12
  max_version: TLS13
  cipher_suites:                               # only applies to TLS1.2; TLS1.3 suites are fixed by Go
    - TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
    - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    - TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256    # required while http2 is true, see below
  curve_preferences: [X25519, CurveP256]
  prefer_server_cipher_suites: true            # deprecated: accepted and ignored (docs)
http_server_config:
  http2: true                                  # default true; cannot be changed on the fly (docs)
  headers:
    Strict-Transport-Security: max-age=31536000
    X-Content-Type-Options: nosniff
    X-Frame-Options: deny
    Content-Security-Policy: "default-src 'self'"
```

With `http2: true` (the default) a `cipher_suites` list without an AES-128-GCM suite stops the server from starting. Run on 3.15.1 with only the two AES_256 suites: `Fatal error err="error starting web server: http2: TLSConfig.CipherSuites is missing an HTTP/2-required AES_128_GCM_SHA256 cipher (need at least one of TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 or TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256)"`, although `promtool check web-config` still printed SUCCESS. Either include one of those suites (the example above does) or set `http2: false`. With the three suites above the server started, negotiated TLS 1.2 `ECDHE-RSA-AES128-GCM-SHA256` and TLS 1.3 `TLS_AES_128_GCM_SHA256`, and returned the four configured headers (`Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`).

## Operating it
- Cert and key files are re-read on every new connection, so cert-manager/rotation needs no restart (run: swapping `tls.crt` changed the serial seen by the next `openssl s_client`). The web.yml file itself is also re-read live (run: raising `min_version` to TLS13 made the next TLS 1.2 handshake fail with `tlsv1 alert protocol version`, no SIGHUP).
- Validate: `promtool check web-config web.yml`; it catches a missing cert file and an unknown version (`unknown TLS version: TLS09`, run) but not the HTTP/2 cipher problem above.
- After enabling TLS, every client must change: scrapes of this server use `scheme: https` with a
  `tls_config.ca_file` (run: self-scrape worked); a plain `http://` request to the TLS port returns `400 Client sent an HTTP request to an HTTPS server`; Grafana data source URL becomes https; readiness probes need `scheme: HTTPS` (gated: unconfirmed, source is paywalled or blocked; no Kubernetes or Grafana here).
- Prometheus still self-scrapes `localhost:9090` in the default config; update that job too.

## Gotchas
- `cipher_suites` only applies up to TLS 1.2 (docs); with `min_version: TLS13` it does not restrict anything.
- Kubernetes probes on HTTPS don't verify certs and httpGet with `scheme: HTTP` will fail (gated: unconfirmed, source is paywalled or blocked; no cluster here).
- Exporters behind a service mesh with mTLS usually don't need this; double TLS wastes CPU (opinion, not measured).

## Verify
- [ ] `openssl s_client -connect host:9090 -tls1_2` succeeds. Testing a lower version with `-tls1_1` fails on OpenSSL 3 for client-side reasons (`no protocols available`), so prove enforcement by setting `min_version: TLS13` and checking that `-tls1_2` is rejected.
- [ ] `curl -sI https://host:9090/-/healthy --cacert ca.crt` shows the configured headers (add `-u user:pw` when basic auth is on, and `--ssl-no-revoke` for the Windows Schannel curl build).
- [ ] `up` for scrapes of this endpoint stays 1 after the switch.

## Checked
Prometheus 3.15.1 and promtool (windows-amd64), OpenSSL 3.2.3 and curl run locally against a private CA: the skill's web.yml as written (fails to start: HTTP/2 cipher error, exact message captured), the corrected version (started; TLS 1.2 and 1.3 handshakes, headers, 401/200 with basic auth), live web.yml re-read, certificate swap seen by the next connection, `min_version: TLS13` rejecting TLS 1.2, plain HTTP to the TLS port (400). Docs read: exporter-toolkit docs/web-configuration.md (prefer_server_cipher_suites ignored, http2 not changeable on the fly, accepted header values). Not run: Alertmanager, node_exporter, Pushgateway with the same file; Kubernetes probes; TLS 1.0/1.1.
