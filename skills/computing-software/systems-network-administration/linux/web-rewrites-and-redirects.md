---
id: computing-software.systems-network-administration.linux.web-rewrites-and-redirects
name: web-rewrites-and-redirects
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, mod-rewrite, rewrite-rules, rewriterule, rewritecond, nginx-rewrite, nginx-return, redirect-301, canonical-host, http-to-https, try-files, web-server, sysadmin]
level: practitioner
status: verified
description: "Write URL redirects and rewrites in nginx and Apache: return vs rewrite, RewriteRule/RewriteCond flags, canonical host and HTTPS, front-controller routing, and avoiding loops."
sources:
  - https://github.com/nginx/nginx.org/blob/main/xml/en/docs/http/ngx_http_rewrite_module.xml
  - https://github.com/nginx/nginx.org/blob/main/xml/en/docs/http/ngx_http_core_module.xml
  - https://github.com/apache/httpd/blob/trunk/docs/manual/mod/mod_rewrite.xml
  - https://github.com/apache/httpd/blob/trunk/docs/manual/rewrite/flags.xml
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Rewrites and redirects (nginx and Apache)

**Goal:** move URLs without breaking links or SEO, route pretty URLs to an app, and never
ship a redirect loop.

## 1. Redirect vs rewrite
- **Redirect**: server tells the client a new URL (301 permanent, 302/307 temporary, 308 permanent keeping method). The browser URL changes.
- **Rewrite**: server maps the URL internally; the client never sees it.
Prefer the simplest tool: nginx `return`, Apache `Redirect`/`RedirectMatch`; reach for
`rewrite`/`mod_rewrite` only when you need conditions or captures.

## 2. nginx
```nginx
server { listen 80; server_name example.com www.example.com; return 301 https://example.com$request_uri; }
server { listen 443 ssl; server_name www.example.com; return 301 https://example.com$request_uri; }  # canonical host

location = /old-page { return 301 /new-page; }
location ~ "^/blog/(\d{4})/(.*)$" { return 301 /posts/$1/$2; }   # quote regexes containing { }
rewrite ^/products/([0-9]+)$ /product.php?id=$1 last;        # internal

location / { try_files $uri $uri/ /index.php?$query_string; }  # front controller (Laravel, WordPress)
```
`rewrite` flags: `last` (re-run location matching with the new URI), `break` (stop rewriting, stay in this location),
`redirect` (302), `permanent` (301). `$request_uri` is the full original request URI including arguments; `$uri` is the normalized current URI without them.
Many redirects: a `map $request_uri $new_uri { /a /b; ... }` + `if ($new_uri) { return 301 $new_uri; }`.

## 3. Apache
```apache
Redirect permanent /old-page /new-page
RedirectMatch 301 ^/blog/(\d{4})/(.*)$ /posts/$1/$2

RewriteEngine On
# HTTP → HTTPS and canonical host in one hop
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\. [NC]
RewriteRule ^ https://example.com%{REQUEST_URI} [R=301,L,NE]
# front controller
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.php [L,QSA]
```
Flags: `L` last, `R=301` redirect, `NC` case-insensitive, `QSA` append query, `QSD` discard query,
`NE` don't escape, `P` proxy, `END` stop all further rounds (avoids .htaccess loops).
In `.htaccess`/`<Directory>` the pattern matches the path **without the leading slash**; in vhost context it has one.

## 4. Debug
```bash
curl -sI http://example.com/old-page | grep -i '^location\|^HTTP'
curl -sIL https://example.com/x | grep -i '^HTTP\|^location'    # follow chain; > 1 hop = fix it
```
Apache trace: `LogLevel alert rewrite:trace3` (error log). nginx: `rewrite_log on;` + `error_log ... notice;`.

## Gotchas
- Test with 302 first; browsers cache 301 aggressively and hide your fixes.
- Behind a TLS-terminating proxy `%{HTTPS}`/`$scheme` is "off/http" → infinite loop; test `X-Forwarded-Proto` instead.
- `return` with code 307 or 308 needs nginx 1.1.16/1.0.13 or 1.13.0 respectively to be treated as a redirect; older versions send them as plain responses.

## Verify
- [ ] Every old URL returns a single 301 hop to the right target with the query string intact.
- [ ] `curl -sIL` on http/www variants reaches the canonical HTTPS URL in one redirect, no loops.

## Checked

Checked 2026-10-26 against nginx/nginx.org (last commit 2026-10-21: ngx_http_rewrite_module.xml, ngx_http_core_module.xml variables) and apache/httpd docs (mod_rewrite.xml, rewrite/flags.xml; last commit 2026-10-25). Confirmed: return codes and redirect forms (301, 302, 307, 308 with version notes), rewrite flags last, break, redirect, permanent, rewrite_log at notice level, $request_uri versus $uri, Apache END and QSD flags, LogLevel alert rewrite:trace3, [OR] condition flag. Removed: the nginx if-inside-location safety claim (it comes from the nginx wiki, not the reference docs).

Run 2026-11-01 on nginx 1.30.6 (Windows, 127.0.0.1 only, curl): `nginx -t` passes for every nginx block in section 2; observed 301 for `return 301`, `rewrite ... permanent` (301) and `redirect` (302), 307 and 308 returned as redirects, the quoted `{4}` regex location, the `map` + `if ($new_uri)` redirect, the `https://example.com$request_uri` redirect keeping the query string, `try_files` falling back to `/index.php?$query_string` with the arguments intact, and the internal `rewrite ... last` leaving `$request_uri` as `/products/42` while `$uri` becomes `/product.php`. The Apache section was not run (no Apache binary) and stays confirmed from the documentation only.
