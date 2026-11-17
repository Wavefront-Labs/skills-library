---
id: computing-software.systems-network-administration.audiobookshelf.reverse-proxy-traefik-cors-warning
name: reverse-proxy-traefik-cors-warning
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [reverse-proxy, traefik, cors, middleware, login-error]
level: practitioner
status: docs-checked
description: "Avoid the Traefik CORS middleware headers that make Audiobookshelf login fail with Unknown Error."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/6.traefik.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/cors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Traefik page is short but carries one important warning: middleware relating to CORS will cause the app to report **Unknown Error** when logging in.

Do not apply any of these headers to the router for the Audiobookshelf site:

- `accessControlAllowMethods`
- `accessControlAllowOriginList`
- `accessControlMaxAge`

For Traefik configuration itself the page just points to the Traefik documentation.

If another tool needs cross-origin access to the API, grant it in Audiobookshelf's "Allowed CORS Origins" setting (see the CORS skill) instead of via the proxy.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Traefik page and the CORS page.

Method: documentation only; no commands were run.
