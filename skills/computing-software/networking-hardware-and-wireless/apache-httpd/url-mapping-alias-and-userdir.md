---
id: computing-software.networking-hardware-and-wireless.apache-httpd.url-mapping-alias-and-userdir
name: url-mapping-alias-and-userdir
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, url-mapping, documentroot, alias, scriptalias, userdir, symlinks]
level: intro
status: docs-checked
description: "Map URLs to files: DocumentRoot, Alias and ScriptAlias for content outside the root, symlinks, UserDir home directories, and the other mapping tools."
sources:
  - https://httpd.apache.org/docs/2.4/urlmapping.html
  - https://httpd.apache.org/docs/2.4/mod/mod_userdir.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL to filesystem mapping
## DocumentRoot
The URL path is appended to `DocumentRoot "/var/www/html"`. A directory request uses `DirectoryIndex`, falling back to a listing if mod_autoindex permits.

## Outside the root
- Symlinks are followed only with `Options FollowSymLinks` or `SymLinksIfOwnerMatch`.
- `Alias "/docs" "/var/web"` maps a path; `ScriptAlias` treats everything there as CGI.
- `AliasMatch`/`ScriptAliasMatch` use regex:
```apache
ScriptAliasMatch "^/~([a-zA-Z0-9]+)/cgi-bin/(.+)" "/home/$1/cgi-bin/$2"
```

## User directories
`UserDir public_html` maps `/~bob/one/two.html` to `~bob/public_html/one/two.html`; also `UserDir /usr/web`, `UserDir /home/*/www`, or a redirect URL (must be last in a list).
```apache
UserDir disabled
UserDir enabled user1 user2
UserDir disabled root
```
The docs strongly recommend `UserDir disabled root`, since `UserDir ./` maps `/~root` to `/`. UserDir lets users share one origin.

## Other tools
`Redirect`, `ProxyPass`/`ProxyPassReverse`, `mod_rewrite`, `mod_speling` (adds load), `FallbackResource`; otherwise 404, customised by `ErrorDocument`.

## Checked

2026-11-08. DocumentRoot and DirectoryIndex behaviour, symlink Options, Alias, ScriptAlias, AliasMatch, UserDir forms, enabled/disabled keywords, the "UserDir ./" and "UserDir disabled root" warning, redirect-last rule and the same-origin warning confirmed against the urlmapping and mod_userdir pages. Placeholder paths replaced with the documented /home examples.

Method: documentation only; no commands were run.
