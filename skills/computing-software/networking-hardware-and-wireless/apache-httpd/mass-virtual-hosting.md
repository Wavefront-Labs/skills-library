---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mass-virtual-hosting
name: mass-virtual-hosting
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, virtual-hosts, mass-hosting, vhost-alias, virtualdocumentroot, usecanonicalname]
level: advanced
status: docs-checked
description: "Serve many sites without per-site config using mod_vhost_alias VirtualDocumentRoot, UseCanonicalName, name-part selectors and shared logging."
sources:
  - https://httpd.apache.org/docs/2.4/vhosts/mass.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic mass virtual hosting
Build the document root from the request so adding a site needs only a directory and DNS entry, with no restart. Trade-off: per-vhost log files are impractical.

## Canonical names
- `UseCanonicalName Off`: name from the `Host:` header (name-based hosting).
- `UseCanonicalName DNS`: reverse DNS of the IP (IP-based).
- `ServerName` is the fallback.

## mod_vhost_alias
```apache
UseCanonicalName Off
LogFormat "%V %h %l %u %t \"%r\" %s %b" vcommon
CustomLog "logs/access_log" vcommon
VirtualDocumentRoot "/www/hosts/%0/docs"
VirtualScriptAlias  "/www/hosts/%0/cgi-bin"
```
`%0` is the whole name; `%2` picks a part. For `www.user.example.com`, `VirtualDocumentRoot "/www/hosts/%2/docs"` gives `/www/hosts/user/docs`.

IP-based: `UseCanonicalName DNS`, `VirtualDocumentRootIP`, `VirtualScriptAliasIP`, and `%A` in the log format.

## Mixing
Normal `<VirtualHost>` blocks can scope different schemes to different IPs. Always give a `ServerName`.

## Logging
Per-vhost files hit descriptor limits. Log `%V` (name) or `%A` (IP) to one file or pipe and split with `split-logfile`.

## Alternatives
`mod_rewrite` (with `RewriteMap`) or `mod_macro`. mod_vhost_alias and mod_rewrite are both disabled by default: enable one when configuring and building httpd. Neither sets `DOCUMENT_ROOT`, so CGIs and SSI that read it get a misleading value.

## Checked

2026-11-08. UseCanonicalName Off vs DNS and the ServerName fallback, the VirtualDocumentRoot and VirtualScriptAlias example, the %0 and %2 selectors, IP-based variants with %A, mixing with VirtualHost blocks, the per-vhost log descriptor warning with split-logfile, and the rewrite and macro alternatives confirmed against the mass virtual hosting page.

Method: documentation only; no commands were run.
