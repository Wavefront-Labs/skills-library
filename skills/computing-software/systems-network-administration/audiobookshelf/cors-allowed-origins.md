---
id: computing-software.systems-network-administration.audiobookshelf.cors-allowed-origins
name: cors-allowed-origins
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [cors, origins, settings, third-party-tools, same-origin]
level: practitioner
status: docs-checked
description: "Add the correct origin to Audiobookshelf Allowed CORS Origins so a browser-based tool can call your server."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/cors.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/migration-os.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/6.traefik.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Audiobookshelf only accepts requests from the same origin. To let a browser-based tool at another domain call the server, add the tool's origin to **Allowed CORS Origins** on the Settings page.

Valid origin format: protocol, domain and port if applicable, with no path and no trailing slash.

- Valid: `https://example.com`
- Invalid: `https://example.com/test` (has a path)
- Invalid: `https://example.com/` (trailing slash)

Add both `http` and `https` versions if you want to support both protocols.

Add the origin of the **tool**, not your server. If the tool is at `https://myawesometool.tld` and Audiobookshelf is at `https://myaudioshelf.tld`, add only `https://myawesometool.tld`.

The migration guide uses this too: the ABS Toolbox page must be added to the allowed origins of both the old and the new server.

The `ALLOW_CORS` environment variable (`'1'`) allows Cross-Origin Resource Sharing globally. Traefik middleware for CORS headers causes an Unknown Error at login (see the Traefik page).

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: CORS page, Migration page, Environment Configuration page and Traefik page.

Method: documentation only; no commands were run.
