---
id: computing-software.cloud-infrastructure-engineering.nginx.client-certificate-mtls
name: client-certificate-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, ssl-verify-client, mtls, ssl-client-certificate, client-cert]
level: advanced
status: docs-checked
description: "Requiring client certificates in nginx with ssl_verify_client, ssl_client_certificate, ssl_verify_depth, ssl_crl and the 495/496 error codes."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Mutual TLS in nginx is configured with the `ngx_http_ssl_module` directives.

- `ssl_verify_client on | off | optional | optional_no_ca` (default `off`) turns on client certificate verification; the result is stored in `$ssl_client_verify`. `optional` requests a certificate and verifies it if one is present. `optional_no_ca` requests one but does not require it to be signed by a trusted CA, for use when a service external to nginx does the verification (the certificate is then available in `$ssl_client_cert`).
- `ssl_client_certificate file` names the trusted CA certificates (PEM) used to verify client certificates; the list is sent to clients. Use `ssl_trusted_certificate` instead if the list should not be sent.
- `ssl_verify_depth number` sets the chain depth; the default is `1`.
- `ssl_crl file` names a PEM file of revoked certificates used to verify client certificates; with intermediate certificates, their CRLs go in the same file.

```nginx
ssl_client_certificate /etc/nginx/tls/clients-ca.pem;
ssl_verify_client on;
ssl_verify_depth 2;

location / {
    proxy_set_header X-Client-DN     $ssl_client_s_dn;
    proxy_set_header X-Client-Verify $ssl_client_verify;
    proxy_pass http://app;
}
```

`$ssl_client_verify` is `SUCCESS`, `FAILED:reason` or `NONE` (no certificate presented). `$ssl_client_s_dn` is the subject DN per RFC 2253. `$ssl_client_escaped_cert` returns the PEM certificate urlencoded; `$ssl_client_cert` is deprecated.

The module defines non-standard error codes usable with `error_page`: `495` (error during client certificate verification), `496` (no required certificate presented) and `497` (plain HTTP request sent to the HTTPS port). The redirect happens after the request is fully parsed.

`proxy_set_header` redefines request headers sent to the backend, so setting the identity headers there replaces any value the client sent.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_ssl_module` page (directives, defaults, variables, 495/496/497) and `ngx_http_proxy_module` (`proxy_set_header`). Removed: the "unable to verify the first certificate" and "400 No required SSL certificate" error strings, advice about browsers, curl verification steps and the `error_page 495 496` snippet's file name.
Method: documentation only; no commands were run.
