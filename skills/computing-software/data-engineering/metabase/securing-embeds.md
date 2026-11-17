---
id: computing-software.data-engineering.metabase.securing-embeds
name: securing-embeds
category: computing-software
field: data-engineering
product: metabase
tags: [securing-embeds, guest-embeds, locked-parameters, signed-jwt, embedding-secret-key, sso-embedding]
level: advanced
status: docs-checked
description: "Choose an authentication model for Metabase embeds: public links, signed guest embeds with locked parameters, token refresh, and SSO-based modular or full app embedding."
sources:
  - https://www.metabase.com/docs/latest/embedding/securing-embeds
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three models.

Public embeds: no authentication or authorization. Anyone with the URL sees the data. Parameters such as `?status=active` or `#hide_parameters=status` only preset or hide filters; removing them exposes unfiltered rows.

Guest embeds (signed JWT):
- Your backend signs a JWT with Metabase's embedding secret key. It encodes the resource and any locked parameters.
- Locked parameters are filters, so they enforce row-level restrictions only.
- Unsigned parameters appended to the URL are rejected.
- There are no Metabase user sessions, so permissions and row and column security do not apply. Lock parameters on every embed.
- Filter selections reset when the JWT expires unless refresh is configured through `guestEmbedProviderUri`. The embed calls this endpoint for a new token only when a data request happens after expiry; refusing to issue a token revokes access.
- Usage analytics list this traffic as "External user".
- Identity-based restrictions need your own authentication flow wired to locked parameters.

Modular and full app embedding (SSO): Pro or Enterprise, using JWT or SAML. User attributes map to tables, rows, columns, download permissions and SQL access. A visitor with no valid session is redirected to SSO. The page's example uses a `role` attribute (`tenant` or `customer`), a `primary_id`, and row filters such as `Account ID = primary_id`.

Gotchas: public links and URL filters are not access control; every guest embed needs locked parameters. Not covered: signing algorithm, token lifetime, HTTPS, caching.

## Checked
2026-11-03. Confirmed against the Metabase docs page Embedding, Securing embedded Metabase: public embeds have no authentication, guest embeds use signed JWTs and locked parameters, no sessions so permissions and row/column security do not apply, External user analytics label, guestEmbedProviderUri refresh behaviour, modular and full app embedding via JWT or SAML on Pro/Enterprise, role and primary_id example. Removed the weakest-to-strongest ranking, which the page does not state.
Method: documentation only; no commands were run.
