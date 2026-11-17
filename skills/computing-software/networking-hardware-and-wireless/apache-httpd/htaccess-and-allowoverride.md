---
id: computing-software.networking-hardware-and-wireless.apache-httpd.htaccess-and-allowoverride
name: htaccess-and-allowoverride
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, htaccess, allowoverride, allowoverridelist, accessfilename, per-directory]
level: practitioner
status: docs-checked
description: "Decide when to use .htaccess, enable it with AllowOverride or AllowOverrideList, understand its performance cost and precedence, and debug it."
sources:
  - https://httpd.apache.org/docs/2.4/howto/htaccess.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .htaccess and AllowOverride
A directive in `/www/htdocs/example/.htaccess` equals one in `<Directory "/www/htdocs/example">`, applying to that directory and below. The name comes from `AccessFileName`.

## Use sparingly
Prefer the main config when you have root. Use `.htaccess` when content owners lack root (shared hosting, control panels, CMS-shipped files).
- Performance: every directory in the path is checked and the file is reread on every request.
- Security: users can change behaviour; document what you allow.

## Enabling
The default is `AllowOverride None`, so `.htaccess` files are ignored. Grant by category (`FileInfo`, `Options`, `AuthConfig`) or per directive:

```apache
AllowOverride None
AllowOverrideList Redirect RedirectMatch RewriteEngine RewriteRule RewriteCond
```
Directives not listed cause a server error.

## Precedence
`.htaccess` overrides `<Directory>`, but `<Location>` in main config overrides `.htaccess`, which lets you enforce settings.

## Troubleshooting
- No effect at all: `AllowOverride None` is probably in force. Add a nonsense word; no HTTP 500 means overrides are off.
- 500 errors: read the error log, e.g. `DirectoryIndex not allowed here`.
- The docs call CGI legacy; consider mod_proxy_fcgi.

## Checked

2026-11-08. Default AllowOverride None, AllowOverrideList behaviour, precedence against Directory and Location, performance and troubleshooting text confirmed against the full .htaccess how-to.

Method: documentation only; no commands were run.
