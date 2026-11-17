---
id: computing-software.networking-hardware-and-wireless.apache-httpd.rewriterule-flags
name: rewriterule-flags
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-rewrite, rewriterule, flags, end, proxy-flag, passthrough]
level: advanced
status: docs-checked
description: "Pick the right RewriteRule flag: L vs END, R redirect codes, P proxy, PT passthrough, QSA/QSD/QSL, NE, NC, F/G, E, CO, C, S and their interactions."
sources:
  - https://httpd.apache.org/docs/2.4/rewrite/flags.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RewriteRule flags
## Stopping
- `L` stops this pass; in per-directory context the request may be reprocessed, causing loops.
- `END` stops all rewriting including per-directory re-entry; preferred there.
- `N` restarts the ruleset (can loop forever).
- `F` returns 403, `G` returns 410; both imply `L`.

## Redirect and proxy
- `R[=code]`: default 302; accepts a code or `temp`, `permanent`, `seeother`. Use with `L`. Codes outside 300-399 drop the substitution.
- `P`: pass to mod_proxy; implies `L`. Keep scheme and host fixed to avoid SSRF.
- `PT`: pass the result back to URL mapping (Alias, Redirect, ScriptAlias); implies `L`, implied per-directory.

## Query string and escaping
- `QSA` appends the original query; `QSD` discards it (wins over QSA); `QSL` splits at the last `?` (2.4.19).
- `NE` stops escaping of `#` and `?` in redirects.
- `B` escapes back-references (2.4.26: `[B=#?;]`).

## Matching and state
- `NC` case-insensitive; `NS` skips internal subrequests.
- `C` chains to the next rule; `S=N` skips N rules.
- `E=VAR:VAL` sets env (`E=!VAR` unsets); `T=type` forces MIME; `H=` forces a handler.
- `CO=NAME:VALUE:DOMAIN:lifetime:path:secure:httponly:samesite` sets a cookie (lifetime in minutes).
- `DPI` discards PATH_INFO.

```apache
RewriteRule "^(.*)$" "/index.php" [END]
RewriteRule "\.exe" "-" [F]
```

## Checked
2026-11-04. Confirmed against the RewriteRule flags page: L/END per-directory behaviour, N loops, F/G imply L, R codes and symbolic names, P implies L and the SSRF warning, PT implies L and is implied per-directory, QSA/QSD precedence, QSL (2.4.19), NE, B and 2.4.26 character list, NS, C, S, E, T, H, CO and minutes lifetime, DPI. Nothing removed.
Method: documentation only; no commands were run.
