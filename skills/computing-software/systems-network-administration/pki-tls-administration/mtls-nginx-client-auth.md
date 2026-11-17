---
id: computing-software.systems-network-administration.pki-tls-administration.mtls-nginx-client-auth
name: mtls-nginx-client-auth
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [mtls-nginx-client-auth, pki-nginx, nginx, ssl_verify_client, mtls, client-certificates, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Require client certificates on nginx with ssl_verify_client, restrict trust to a private CA, check CRL or OCSP and pass identity upstream."
sources:
  - https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_verify_client
  - https://nginx.org/en/docs/http/configuring_https_servers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mutual TLS on nginx
Goal: only holders of certificates from your CA reach the service.
```
ssl_client_certificate /etc/nginx/clients-ca.pem;   # CA(s) that sign clients
ssl_verify_client on;                                # or optional / optional_no_ca
ssl_verify_depth 2;
ssl_crl /etc/nginx/clients.crl;
location / {
  proxy_set_header X-Client-DN $ssl_client_s_dn;
  proxy_set_header X-Client-Verify $ssl_client_verify;
  proxy_set_header X-Client-Cert $ssl_client_escaped_cert;
  proxy_pass http://app;
}
```
- `ssl_verify_client` takes `on | off | optional | optional_no_ca` (default `off`); the result is in `$ssl_client_verify`: `SUCCESS`, `FAILED:reason` (reason string since 1.11.7) or `NONE` when no certificate was presented.
- `ssl_client_certificate` names the trusted CAs and the list is sent to clients; `ssl_trusted_certificate` verifies the same way but the list is not sent. `ssl_verify_depth` defaults to 1.
- `ssl_crl` is a PEM CRL file for client certificates; with intermediates, put their CRLs in the same file. `ssl_ocsp on|off|leaf` (1.19.0) validates the client chain by OCSP and needs `ssl_verify_client` on or optional plus a `resolver`; only `http://` responders are supported.
- `optional` requests a certificate and verifies it only if present, so unauthenticated requests still get through: the application or a `map`/`if` on `$ssl_client_verify` must enforce `SUCCESS`. `optional_no_ca` does not require a trusted CA and is meant for an external verifier.
- `$ssl_client_cert` is deprecated; use `$ssl_client_escaped_cert` (1.13.5). `$ssl_client_s_dn` is RFC 2253 format since 1.11.6.
- Error codes usable with `error_page`: 495 (verification error), 496 (no required certificate), 497 (plain HTTP sent to the HTTPS port).
- On name-based servers, a client that sends no SNI is handled by the default server's configuration; add `ssl_reject_handshake on` there (see nginx-sni-multiple-certs).
Verify:
- [ ] A request without a certificate is refused (nginx error 496).
- [ ] A certificate from another CA is rejected and `$ssl_client_verify` shows `FAILED:reason`.

## Checked
Confirmed 2026-11-08 against ngx_http_ssl_module (ssl_verify_client, ssl_client_certificate, ssl_trusted_certificate, ssl_verify_depth, ssl_crl, ssl_ocsp, variables, error codes) and "Configuring HTTPS servers" (client certificates and SNI). Removed (not on the pages): the 400 response text, EKU and lifetime advice, header-spoofing advice, curl example.
Method: docs-only read of cited pages, 2026-11-08
