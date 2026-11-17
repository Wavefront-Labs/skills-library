---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-headers
name: mod-headers
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-headers, header, requestheader, response-headers, always, env-condition]
level: practitioner
status: docs-checked
description: "Set, add, append, merge, unset and edit request and response headers with mod_headers, including always vs onsuccess, env= and expr= conditions and ordering."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_headers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_headers
`Header [condition] action header [value [replacement]] [early|env=[!]var|expr=expr]` changes response headers after the content handler and output filters. `RequestHeader` changes request headers just before the content handler.

## Actions
- `set` replaces; `append` joins with a comma (not for `Set-Cookie`, use `add`); `add` may duplicate.
- `merge` appends only if absent (case-sensitive).
- `unset`; `edit`/`edit*` regex replace once/all (RequestHeader needs both value and replacement).
- `echo` (Header only); `setifempty` (2.4.7+); `note` (Header only).

## always vs onsuccess
`onsuccess` is the default; `always` also covers errors and internal redirects. CGI and mod_proxy_fcgi headers live in the always table, so:
```apache
Header onsuccess unset X-Foo
Header always set X-Foo "baz"
```

## Conditions
```apache
Header always set CustomHeader my-value "expr=%{REQUEST_URI} =~ m#^/special_path.php$#"
Header merge Cache-Control no-cache env=CGI
```
`expr=` is evaluated later than `<If>`.

## Order
Directives apply in config order: `append` then `unset` leaves the header unset.

## early
Test aid, server or vhost context only; fails in Directory or Location.
```apache
RequestHeader edit Destination ^https: http: early
```
Prefer `set` over `setifempty` for Content-Type.

## Checked

2026-11-08. Header and RequestHeader actions, always vs onsuccess, early, env= and expr= conditions, ordering and the setifempty Content-Type note confirmed against the full mod_headers page.

Method: documentation only; no commands were run.
