---
id: computing-software.systems-network-administration.varnish-cache.wordpress-vcl-config
name: wordpress-vcl-config
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [wordpress, purge-plugin, cms-caching, static-files]
level: practitioner
status: docs-checked
description: "Configure Varnish for WordPress: move the web server off port 80, install a purge plugin, and use VCL that bypasses logged-in and cart traffic and strips static-file cookies."
sources:
  - https://www.varnish.org/docs/tutorials/configuring-varnish-wordpress/
  - https://www.varnish.org/docs/tutorials/change-web-server-port-for-varnish/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# wordpress vcl config

Steps from the guide:
1. Install Varnish on the web server host (or a dedicated machine).
2. Move the web server off the ports Varnish should own (80 and 443) and point the backend at that port.
3. Install a purge plugin; the guide uses Proxy Cache Purge, which sends `PURGE` requests and expects matching VCL.
4. Replace `/etc/varnish/default.vcl` and reload.

Key logic of the guide VCL:
- ACL `purge` limits who may purge; purges are implemented as bans on `obj.http.x-url` and `obj.http.x-host`, with an `X-Purge-Method: regex` variant.
- Normalise: strip empty query strings, remove the port from `Host`, `std.querysort`, `unset req.http.proxy`, set `X-Forwarded-Proto` by port.
- Remove analytics query parameters (`gclid`, `fbclid` and others).
- Cache only GET and HEAD.
- Static file extensions: drop cookies and `return (hash)`.
- Pass when cookies matching the guide's regex (for example `wordpress_`, `wp-postpass`, `woocommerce_cart_hash`, `PHPSESSID`) are present, or `Authorization`, or for URLs like `/wp-admin`, `/wp-login.php`, `/cart`, `/checkout`.
- Remove remaining cookies and hash.
- `vcl_hash` adds `X-Forwarded-Proto`.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the closing tip; corrected the cookie names to the guide's regex.

Method: documentation only; no commands were run.
