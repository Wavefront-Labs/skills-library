---
id: computing-software.networking-hardware-and-wireless.apache-httpd.environment-variables-setenvif
name: environment-variables-setenvif
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, environment-variables, setenv, setenvif, browsermatch, passenv, require-env]
level: practitioner
status: docs-checked
description: "Set and use httpd environment variables with SetEnv, SetEnvIf, BrowserMatch and PassEnv, the special-purpose variables, and their use in logs and access control."
sources:
  - https://httpd.apache.org/docs/2.4/env.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables
## Setting
- `SetEnv` unconditional; `PassEnv` copies from the starting shell; `UnsetEnv` removes.
- `SetEnvIf` / `SetEnvIfNoCase` and `BrowserMatch` set from request attributes.

```apache
BrowserMatch "Mozilla/2" nokeepalive
SetEnvIf Request_URI \.(gif|jpg|png)$ image-request
```

## Caveats
- `SetEnv` runs late, so `SetEnvIf` and `RewriteCond` cannot see its variables.
- Standard CGI variables cannot be overridden.
- Names may contain letters, digits, underscores; others become underscores.
- Variables are internal to httpd and become OS environment only for CGI or SSI.

## Special variables
| Variable | Effect |
|---|---|
| `nokeepalive` | disable KeepAlive |
| `downgrade-1.0` | treat as HTTP/1.0 |
| `force-response-1.0` | HTTP/1.0 response to 1.0 clients |
| `no-gzip` | disable DEFLATE |
| `redirect-carefully` | careful redirects |

## Use
```apache
CustomLog "logs/access_log" common env=!image-request
<Directory "/web/images">
    Require env local_referal
</Directory>
```
`%e` logs variables. The page recommends `<If>` and `Require expr` with `reqenv` as the modern alternative.

## Checked

2026-11-08. SetEnv, PassEnv, SetEnvIf, caveats, special-purpose variables, conditional logging and Require env examples confirmed against the full env page.

Method: documentation only; no commands were run.
