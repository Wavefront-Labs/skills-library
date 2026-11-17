---
id: computing-software.networking-hardware-and-wireless.apache-httpd.when-not-to-use-mod-rewrite
name: when-not-to-use-mod-rewrite
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-rewrite, alternatives, redirect, proxypass, fallbackresource, if]
level: practitioner
status: docs-checked
description: "Replace mod_rewrite with simpler directives: Redirect, Alias, ProxyPass, FallbackResource, If expressions, Require env and balancer, keeping rewrite as last resort."
sources:
  - https://httpd.apache.org/docs/2.4/rewrite/avoid.html
  - https://httpd.apache.org/docs/2.4/rewrite/proxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# When not to use mod_rewrite
It should be a last resort; the main legitimate case is when only `.htaccess` is available.

## Alternatives
- Redirects: `Redirect "/one/" "http://one.example.com/"` (preserves path info).
- Aliasing: `Alias "/cats" "/var/www/virtualhosts/felines/htdocs"` (server or vhost only).
- Proxying: `ProxyPass` + `ProxyPassReverse` instead of `[P]` when no pattern matching is needed.
- Conditions: `<If "req('Host') != 'www.example.com'">`.
- Front controller: `FallbackResource /index.php`.
- Access control:
```apache
SetEnvIfNoCase User-Agent ^NameOfBadRobot goaway
<Location "/secret/files">
    <RequireAll>
        Require all granted
        Require not env goaway
    </RequireAll>
</Location>
```
- Virtual hosting: `<VirtualHost>` blocks, `mod_vhost_alias` or `mod_macro` for many.
- Load balancing: `mod_proxy_balancer`.

## Where rewrite fits
`[P]` is justified for proxying content missing locally, such as a migration. Referer- and User-Agent-based blocking can be circumvented; use a firewall for sustained attacks.

Note: rewrite/proxy.html is a deprecation notice merged into this page.

## Checked

2026-11-08. Last-resort guidance, Redirect path preservation, Alias scope, ProxyPass vs the [P] flag and the migration case, the If example, FallbackResource, SetEnvIfNoCase with Require, vhost and balancer alternatives, and the circumvention warnings confirmed against the avoid page; the proxy page is confirmed as a deprecation notice.

Method: documentation only; no commands were run.
