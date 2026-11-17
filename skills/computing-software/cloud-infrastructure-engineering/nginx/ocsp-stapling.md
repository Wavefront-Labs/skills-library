---
id: computing-software.cloud-infrastructure-engineering.nginx.ocsp-stapling
name: ocsp-stapling
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, ssl-stapling, ocsp, ssl-stapling-verify, resolver]
level: advanced
status: docs-checked
description: "Enabling OCSP stapling in nginx with ssl_stapling, ssl_stapling_verify, ssl_trusted_certificate and a resolver, plus ssl_stapling_file and ssl_stapling_responder."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Directives from the `ngx_http_ssl_module` page:

- `ssl_stapling on | off;` (default `off`) enables stapling of OCSP responses by the server.
- `ssl_stapling_verify on | off;` (default `off`) verifies OCSP responses. For this, the server certificate's issuer, the root certificate and all intermediate certificates must be configured as trusted with `ssl_trusted_certificate`.
- `ssl_trusted_certificate file;` names trusted CA certificates (PEM) used to verify client certificates and OCSP responses when `ssl_stapling` is on. Unlike `ssl_client_certificate`, this list is not sent to clients.
- For stapling to work the certificate of the server certificate's issuer must be known: if the `ssl_certificate` file lacks intermediate certificates, the issuer certificate must be in the `ssl_trusted_certificate` file.
- A `resolver` is needed to resolve the OCSP responder host name (`resolver_timeout` defaults to `30s`).
- `ssl_stapling_file file;` takes the stapled response from a file instead of querying the responder named in the certificate.
- `ssl_stapling_responder url;` overrides the responder URL from the certificate's Authority Information Access extension. Only `http://` responders are supported.

```nginx
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/nginx/tls/chain.pem;
resolver 192.0.2.53;
```

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_ssl_module` page (stapling directives) and `ngx_http_core_module` (`resolver`, `resolver_timeout`). Removed: lazy-fetch timing, error message strings, claims about specific CAs ending OCSP (a confirm marker), must-staple advice, the resolver addresses and `valid=` figure, and the openssl Verify step.
Method: documentation only; no commands were run.
