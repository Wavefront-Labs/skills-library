---
id: computing-software.networking-hardware-and-wireless.apache-httpd.rewrite-recipes-redirect-and-canonical-host
name: rewrite-recipes-redirect-and-canonical-host
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-rewrite, canonical-hostname, trailing-slash, redirect, recipes]
level: practitioner
status: docs-checked
description: "Apply documented rewrite recipes: trailing-slash handling, canonical hostname, multi-directory lookup, moved resources and canonical URLs, with simpler alternatives."
sources:
  - https://httpd.apache.org/docs/2.4/rewrite/remapping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rewrite recipes: redirects and canonical forms
## Canonical hostname
Preferred: a dedicated vhost.
```apache
<VirtualHost *:80>
  ServerName undesired.example.com
  ServerAlias example.com notthis.example.com
  Redirect "/" "http://www.example.com/"
</VirtualHost>
```
Or `<If "%{HTTP_HOST} != 'www.example.com'">` with `Redirect`. mod_rewrite fallback for `.htaccess`:
```apache
RewriteCond "%{HTTP_HOST}" "!^www\.example\.com" [NC]
RewriteCond "%{HTTP_HOST}" "!^$"
RewriteRule "^/?(.*)" "http://www.example.com/$1" [L,R,NE]
```

## Trailing slash
Add: conditions `-d` and `!/$`, then `RewriteRule "^(.*)$" "$1/" [R=301,L]`. mod_dir already does this when `DirectorySlash` is on (default).

## Search multiple directories
```apache
RewriteCond "%{DOCUMENT_ROOT}/dir1/%{REQUEST_URI}" -f
RewriteRule "^(.+)" "%{DOCUMENT_ROOT}/dir1/$1" [L]
RewriteRule "^" "-" [PT]
```
Alias or symlinks suit permanent setups.

## Moved or canonical
Prefer `Redirect`/`RedirectMatch` for moved resources and canonical URLs:
```apache
RedirectMatch "^/(puppies|canines)/(.*)" "/dogs/$2"
```

## Moved root
`RewriteRule "^/$" "/about/" [R]` affects only `/`; if all content moved, change `DocumentRoot`.

## Time-based
`%{TIME_HOUR}%{TIME_MIN}` comparisons work but caching makes them unreliable.

## Checked

2026-11-08. Canonical hostname vhost, If and rewrite forms, trailing-slash conditions and the DirectorySlash note, multi-directory lookup, RedirectMatch for canonical URLs, the moved-root note and the time-based caching caveat confirmed against the Redirecting and Remapping page.

Method: documentation only; no commands were run.
