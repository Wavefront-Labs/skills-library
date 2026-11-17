---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-http-server-tls-auth
name: grafana-alloy-http-server-tls-auth
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [http-block, tls, client-auth-type, authbasic, authfilter, authenticate-matching-paths, min-version]
level: advanced
status: docs-checked
description: "Secure the Alloy HTTP server with the http block: basic auth with path filters, TLS certificates, mutual TLS client_auth_type values and the reload caveat."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/config-blocks/http.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Securing the Alloy HTTP server

The `http` block (unlabeled, once) has no arguments, only `auth` and `tls` inner blocks.

## Basic auth with path filter
```alloy
http {
  auth {
    basic {
      username = sys.env("BASIC_AUTH_USERNAME")
      password = sys.env("BASIC_AUTH_PASSWORD")
    }
    filter {
      paths                       = ["/metrics", "/v1"]
      authenticate_matching_paths = true
    }
  }
}
```
`filter.paths` use prefix matching. With `authenticate_matching_paths = false` the listed paths are excluded instead, so `paths = ["/metrics"]` protects everything except `/metrics`.

## TLS
`tls` needs a cert (`cert_file` or `cert_pem`) and a key (`key_file` or `key_pem`); each pair is mutually exclusive. Other arguments: `cipher_suites`, `curve_preferences`, `min_version` and `max_version` (`TLS10` to `TLS13`), `client_ca_file` or `client_ca_pem`.

`client_auth_type` (default `NoClientCert`): `RequestClientCert`, `RequireAnyClientCert`, `VerifyClientCertIfGiven`, `RequireAndVerifyClientCert`. Client CA arguments are only allowed when it is not `NoClientCert`. BoringCrypto builds allow only the RSA and ECDHE AES-GCM suites marked yes in the page's cipher table (not the TLS 1.3 `TLS_AES_*` names or ChaCha20) and curves `CurveP256`, `CurveP384`, `CurveP521` (not `X25519`).

Gotcha: adding or removing `tls` on a live reload does not affect existing connections, which stay plain text or TLS. Configure TLS before starting Alloy.

Windows: `windows_certificate_filter` (with `client` and `server` blocks, `store`, `system_store`, `refresh_interval` default `5m`) takes certificates from the Windows store; defining `cert_pem`, `cert_file`, `key_pem`, `key_file` or the client CA arguments alongside it causes an error.

## Checked

2026-11-04. Confirmed against the Alloy `http` block reference (config-blocks/http.md): block structure, auth basic and filter arguments, tls arguments, client_auth_type values, cipher and curve tables, min/max versions, reload warning, windows_certificate_filter. Fixed: BoringCrypto cipher wording, and windows_certificate_filter conflicts raise an error rather than being silently overridden.

Method: documentation only; no commands were run.
