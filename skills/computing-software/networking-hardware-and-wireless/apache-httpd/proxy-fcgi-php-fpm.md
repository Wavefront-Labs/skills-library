---
id: computing-software.networking-hardware-and-wireless.apache-httpd.proxy-fcgi-php-fpm
name: proxy-fcgi-php-fpm
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-proxy-fcgi, php-fpm, fastcgi, sethandler, pathinfo]
level: practitioner
status: docs-checked
description: "Connect httpd to PHP-FPM or other FastCGI backends with mod_proxy_fcgi: ProxyPass, ProxyPassMatch, unix sockets, SetHandler, PATH_INFO and ProxyFCGISetEnvIf."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_proxy_fcgi.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_proxy_fcgi and PHP-FPM
Requires mod_proxy. It does not start backends; use `fcgistarter` or the framework's manager.

```apache
ProxyPass "/myapp/" "fcgi://localhost:4000/" enablereuse=on
ProxyPassMatch "^/myapp/.*\.php(/.*)?$" "fcgi://localhost:9000/var/www/" enablereuse=on
ProxyPassMatch "^/(.*\.php(/.*)?)$" "unix:/var/run/php5-fpm.sock|fcgi://localhost/var/www/"
```
`enablereuse=on` needs 2.4.11+ (reuse is off by default); size the FPM pool to cover pooled connections. Unix sockets need 2.4.9+.

## SetHandler form (2.4.10+)
Lets Apache map URI to filename for more accurate PATH_INFO:
```apache
<FilesMatch "\.php$">
    SetHandler "proxy:unix:/path/to/app.sock|fcgi://localhost/"
</FilesMatch>
```

## PATH_INFO and variables
- By default PATH_INFO is not set; env `proxy-fcgi-pathinfo` (values `first-dot`, `last-dot`, `full`, `unescape`) gives a best guess.
- `ProxyFCGIBackendType FPM|GENERIC` (2.4.26+, default FPM): use GENERIC if a non-PHP-FPM backend misreads SCRIPT_FILENAME or PATH_TRANSLATED.
- `ProxyFCGISetEnvIf` overrides variables sent; `!VAR` unsets one.

## Balanced
`BalancerMember "fcgi://localhost:4000"` inside a `balancer://` block.

## Checked
2026-11-04. Confirmed against the mod_proxy_fcgi reference: examples, version gates (2.4.9, 2.4.10, 2.4.11, 2.4.26), proxy-fcgi-pathinfo values, ProxyFCGIBackendType and ProxyFCGISetEnvIf behaviour. Nothing removed.
Method: documentation only; no commands were run.
