---
id: computing-software.networking-hardware-and-wireless.apache-httpd.security-hardening-tips
name: security-hardening-tips
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, security, hardening, dos, file-permissions, allowoverride, ssi]
level: advanced
status: docs-checked
description: "Apply the official security tips: DoS timeouts and request limits, root-owned ServerRoot, SSI and CGI cautions, deny-by-default Directory, UserDir and dotfiles."
sources:
  - https://httpd.apache.org/docs/2.4/misc/security_tips.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security hardening
## Denial of service
Lower `Timeout` and `KeepAliveTimeout` (or disable `KeepAlive`); set `RequestReadTimeout`; cap input with `LimitRequestBody`, `LimitRequestFields`, `LimitRequestFieldSize`, `LimitRequestLine`, `LimitXMLRequestBody`; tune `MaxRequestWorkers`. Event avoids a thread per connection. A firewall can cap connections per IP but does not stop DDoS.

## Permissions
Apache starts as root, so root-executed files and their parents must not be writable by others (`chown 0`, `chmod 755` on dirs, `chmod 511` on the binary). A writable logs directory lets an attacker symlink a log to a system file.

## SSI and CGI
Use a separate extension such as `.shtml`; `IncludesNOEXEC` blocks `exec cmd`. CGI runs as the server user; prefer ScriptAliased CGI with trusted writers, and suEXEC or CGIWrap.

## Deny by default
```apache
<Directory "/">
    AllowOverride None
    Require all denied
</Directory>
<Directory "/usr/local/httpd">
    Require all granted
</Directory>
UserDir disabled root
<FilesMatch "^\.(?!well-known)">
    Require all denied
</FilesMatch>
```
`AllowOverride None` is the default since 2.3.9. `<Location>` can override `<Directory>`.

## Review
Check logs: a `200` for a file like `.env` means tighten config. Test merged config; modules like mod_access_compat replace rather than merge.

## Checked
2026-11-04. Confirmed against the Security Tips page: DoS directives, ServerRoot permissions (chown 0, chmod 755 and 511), SSI and CGI advice, deny-by-default blocks, AllowOverride None default since 2.3.9, UserDir disabled root, log-reading advice, configuration merging. Nothing removed.
Method: documentation only; no commands were run.
