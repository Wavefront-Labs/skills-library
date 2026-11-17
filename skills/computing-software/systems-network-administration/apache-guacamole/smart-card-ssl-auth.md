---
id: computing-software.systems-network-administration.apache-guacamole.smart-card-ssl-auth
name: smart-card-ssl-auth
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, smart-card, client-certificate, ssl-auth, ssl-auth-uri, x-client-certificate, ssl-client-auth, mutual-tls, sso]
level: advanced
status: docs-checked
description: "Certificate or smart-card login for Guacamole: ssl-auth-uri and ssl-auth-primary-uri, proxy headers X-Client-Certificate/X-Client-Verified, Apache and Nginx client-auth config."
sources:
  - https://guacamole.apache.org/doc/gug/ssl-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smart card / client certificate auth

Install: `ssl/guacamole-auth-sso-ssl-1.6.0.jar` into `GUACAMOLE_HOME/extensions/`; Docker: `SSL_AUTH_ENABLED=true`.

Required:
```
ssl-auth-uri: https://*.auth.guac.example.net
ssl-auth-primary-uri: https://guac.example.net
```
`ssl-auth-uri` is a wildcard domain where the proxy demands client certs; the primary domain does not.

Optional (default): `ssl-auth-client-certificate-header` (`X-Client-Certificate`, URL-encoded PEM), `ssl-auth-client-verified-header` (`X-Client-Verified`: `SUCCESS`, `FAILED: <reason>` or `NONE`), `ssl-auth-max-token-validity` (5 min), `ssl-auth-max-domain-validity` (5 min), `ssl-auth-subject-username-attribute`, `ssl-auth-subject-base-dn`.

Flow: user clicks "Certificate / Smart Card", Guacamole redirects to a temporary subdomain, the proxy does client auth and passes the headers, Guacamole returns to the primary domain; the username comes from the certificate subject.

Proxy for the wildcard host (Nginx):
```nginx
ssl_client_certificate /path/to/client-auth-ca-certs.crt;
ssl_verify_client optional;
location /guacamole/ {
    proxy_pass http://localhost:8080;
    proxy_buffering off;
    proxy_http_version 1.1;
    proxy_set_header Host $http_host;
    proxy_set_header X-Client-Verified $ssl_client_verify;
    proxy_set_header X-Client-Certificate $ssl_client_escaped_cert;
}
```
Apache equivalent: `SSLVerifyClient optional`, `ProxyPreserveHost on`, and `RequestHeader set` for both headers. The wildcard block needs no websocket-tunnel location; the normal domain keeps the standard config with Host passed through.

Verify: the certificate login lands on the primary domain as the certificate's user.

## Checked

2026-11-04. Confirmed against the Guacamole manual page ssl-auth: two-domain design with a wildcard client-auth subdomain, the Certificate / Smart Card login option and temporary subdomain flow, X-Client-Verified values (SUCCESS, FAILED: reason, NONE) and X-Client-Certificate as URL-encoded PEM, the two required URI properties, token and domain validity defaults of 5 minutes, subject username and base DN properties, SSL_AUTH_ENABLED, the Nginx and Apache client-auth settings (the Nginx block here is a shortened form of the manual's), and the omitted websocket-tunnel location. Nothing removed.

Method: documentation only; no commands were run.
