---
id: computing-software.cybersecurity-defensive.keycloak.oidc-client-redirect-uris-and-web-origins
name: oidc-client-redirect-uris-and-web-origins
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, redirect-uri, web-origins, cors, oidc-client]
level: practitioner
status: docs-checked
description: "Set strict Valid Redirect URIs and Web Origins on OIDC clients; exact matching, end-only wildcards, and why the full wildcard is unsafe."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/oidc/con-basic-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# oidc client redirect uris and web origins
On an OIDC client's *Settings* tab, *Valid Redirect URIs* is a required field. Exact, case sensitive string matching is used. You can use a wildcard at the end of the pattern, for example `http://host.com/path/*`.

Safety rules stated in the docs:
- If the passed redirect URI contains the userinfo part, or its path manages access to the parent directory (`/../`), no wildcard comparison is performed; exact string matching applies instead.
- The full wildcard `*` allows any http or https redirect URI; the docs say not to use it in production.
- Exclusive redirect URI patterns are typically more secure.

*Web Origins* handles CORS: domain URLs listed are embedded in the access token sent to the client application, which uses them to decide whether to allow a CORS request. Only Keycloak client adapters support this feature.

Other Access settings: *Root URL* (prepended to relative URLs), *Home URL* (default URL to redirect or link back to the client), *Admin URL* (callback endpoint for administrative operations). General: *Client ID* (alphanumeric ID used in OIDC requests and the database), *Name*, *Description*, *Always Display in Console*.

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/oidc/con-basic-settings.adoc. Removed (not on the page): the `app.example.org` example, the "wildcard also admits every path" gotcha, the `allowed-origins`/`web-origins` scope claim detail and the Verify step.
Method: documentation only; no commands were run.
