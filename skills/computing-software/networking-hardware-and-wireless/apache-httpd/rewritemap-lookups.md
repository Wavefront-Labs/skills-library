---
id: computing-software.networking-hardware-and-wireless.apache-httpd.rewritemap-lookups
name: rewritemap-lookups
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-rewrite, rewritemap, txt-map, dbm, prg-map]
level: advanced
status: docs-checked
description: "Use RewriteMap for key-value URL lookups: txt, rnd, dbm, int, prg and dbd map types, the ${map:key|default} call syntax and context limits."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RewriteMap lookups
`RewriteMap MapName MapType:MapSource [MapTypeOptions]` is valid only in server and vhost context (the third argument needs 2.4.29+).

| Type | Source |
|---|---|
| `txt` | plain key-value file |
| `rnd` | random pick from a text file |
| `dbm` | DBM hash built with `httxt2dbm` |
| `int` | built-in `toupper`, `tolower`, `escape`, `unescape` |
| `prg` | external program or script |
| `dbd` / `fastdbd` | SQL SELECT lookup |

## Use
Call a map with `${mapname:key|default}`:
```apache
RewriteMap examplemap "txt:/path/to/file/map.txt"
RewriteRule "^/ex/(.*)" "${examplemap:$1}"
```
A missing key gives the default, or the empty string if none is given. Empty values behave as absent keys, so the two cannot be told apart.

## Checked

2026-11-08. RewriteMap syntax, 2.4.29 third argument, server and vhost context, map types and lookup syntax with default confirmed on the RewriteMap section of the mod_rewrite page. Removed the claims about the avoid page and mass.html, which are not among the cited sources.

Method: documentation only; no commands were run.
