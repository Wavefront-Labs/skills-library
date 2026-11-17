---
id: computing-software.networking-hardware-and-wireless.apache-httpd.redirects-mod-alias
name: redirects-mod-alias
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, redirect, redirectmatch, alias, mod-alias, status-codes]
level: practitioner
status: docs-checked
description: "Use Redirect, RedirectMatch, Alias and AliasMatch correctly: status keywords, trailing-slash rules, processing order, and permitting aliased directories."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_alias.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_alias redirects and aliases
## Alias
Case-sensitive, whole path segments only.
```apache
Alias "/image" "/ftp/pub/image"
<Directory "/ftp/pub/image">
    Require all granted
</Directory>
```
`/imagefoo.gif` does not match. The target is outside DocumentRoot, so you may need to permit it explicitly. If the URL path ends in `/`, requests must include it. `AliasMatch` does not append the remainder, so capture it: `AliasMatch "^/image/(.*)$" "/ftp/pub/image/$1"`.

## Redirect
`Redirect [status] URL-path URL`

| Status | Code |
|---|---|
| `permanent` | 301 |
| `temp` | 302 (default) |
| `seeother` | 303 |
| `gone` | 410 (omit URL) |

Codes 300-399 need a URL; others must omit it. `RedirectPermanent` and `RedirectTemp` are shortcuts.
```apache
Redirect permanent "/one" "http://example.com/two"
RedirectMatch "(.*)\.gif$" "http://other.example.com$1.jpg"
```

## Order
1. All Redirects run before any Alias.
2. Within a context, config order; first match wins, so list the most specific path first.
3. Directives in `<Location>` take precedence over global ones.

## Checked

2026-11-08. Alias, AliasMatch, Redirect status keywords and codes, trailing-slash rule, processing order and Location precedence confirmed against the full mod_alias page. Softened the claim that aliased directories must be permitted to match the page (may need to be).

Method: documentation only; no commands were run.
