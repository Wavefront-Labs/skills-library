---
id: computing-software.cybersecurity-defensive.system-hardening.apache-httpd-hardening
name: apache-httpd-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [web-server-hardening, apache-hardening, httpd, servertokens, mod-security, tls-configuration, module-minimisation]
level: practitioner
status: docs-checked
description: "Harden Apache httpd: minimal modules, ServerTokens Prod, directory restrictions, no indexes or overrides, TLS settings, security headers, request limits and ModSecurity CRS."
sources: ["https://httpd.apache.org/docs/2.4/misc/security_tips.html", "https://httpd.apache.org/docs/2.4/mod/core.html", "https://httpd.apache.org/docs/2.4/mod/mod_ssl.html", "https://httpd.apache.org/docs/2.4/programs/httpd.html", "https://httpd.apache.org/docs/2.4/programs/apachectl.html", "https://coreruleset.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apache httpd hardening

**Goal:** an httpd instance with only needed modules, locked-down directories, modern TLS and no information leaks.

## Modules
List loaded modules: `httpd -M`. Disable modules you do not use (for example `mod_status` or restrict it, `mod_info`, `mod_autoindex`, `mod_userdir`, `mod_dav`, `mod_cgi`, and the proxy modules unless reverse proxying) by removing or commenting their `LoadModule` lines; the mechanism is distribution-specific, so follow your distribution's documentation.

## Global settings
```apache
ServerTokens Prod
ServerSignature Off
TraceEnable Off
FileETag None
Timeout 30
LimitRequestBody 10485760
LimitRequestFields 100
<Directory />
    Options None
    AllowOverride None
    Require all denied
</Directory>
<Directory /var/www/html>
    Options -Indexes -Includes -ExecCGI +FollowSymLinks
    AllowOverride None
    Require all granted
    <LimitExcept GET POST HEAD>
        Require all denied
    </LimitExcept>
</Directory>
<FilesMatch "^\.">
    Require all denied
</FilesMatch>
Header always set X-Content-Type-Options nosniff
Header always set Strict-Transport-Security "max-age=<SECONDS>; includeSubDomains"
Header always unset X-Powered-By
```
Run as a dedicated unprivileged user (set with the `User` directive), with web content not writable by that user.

## TLS (mod_ssl)
```apache
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLHonorCipherOrder off
SSLSessionTickets off
SSLUseStapling on
SSLCompression off
```
Set `SSLCipherSuite` from current published TLS guidance. `SSLProtocol` defaults to `all -SSLv3`, `SSLCompression` to off, and `SSLSessionTickets` to on, so the settings above change the last of those.

## WAF
ModSecurity with the OWASP Core Rule Set: run in detection-only mode first, tune exclusions, then enforce, and choose the paranoia level deliberately (see the CRS documentation).

## Gotchas
- `AllowOverride All` lets any `.htaccess` (including attacker-uploaded) change config; prefer `None`.
- `mod_status` served by `SetHandler server-status` and open to the world leaks request details; restrict it with `Require ip <ADMIN_NETWORK>`.
- `apachectl configtest` before restart or reload.

## Verify
- [ ] Response headers show `Server: Apache` only.
- [ ] `TRACE` requests return 405 (`TraceEnable off`); a directory without an index file returns 403.

## Checked
2026-10-31. Confirmed against the Apache HTTP Server 2.4 docs: `ServerTokens` (Prod, default Full), `ServerSignature` (default Off), `TraceEnable off` returns 405, `FileETag`, `LimitRequestBody` and `LimitRequestFields` (default 100), `AllowOverride None`, `Options` flags, `httpd -M`, `apachectl configtest`, `mod_status`, and the `mod_ssl` directives `SSLProtocol`, `SSLCompression`, `SSLHonorCipherOrder`, `SSLSessionTickets`, `SSLUseStapling` with their defaults. Removed: distribution paths and `a2dismod`, the Mozilla cipher reference, a paranoia-level recommendation, the CIS source, the HSTS lifetime figure.
Method: documentation only; no commands were run.
