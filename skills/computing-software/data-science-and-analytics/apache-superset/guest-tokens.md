---
id: computing-software.data-science-and-analytics.apache-superset.guest-tokens
name: guest-tokens
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [guest-token, embedding, jwt, rls, service-account]
level: advanced
status: docs-checked
description: "Issue Superset guest tokens server side: /api/v1/security/guest_token/, GUEST_TOKEN_JWT_EXP_SECONDS, JWT secret, per-viewer RLS and token handling."
sources:
  - https://github.com/apache/superset/blob/master/docs/docs/using-superset/embedding.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/securing_superset.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give an embedded viewer scoped access without a Superset account, using the embedded SDK flow.

Flow: the embedded SDK is configured with a `fetchGuestToken` callback. It must return a guest token your server obtains by calling Superset's `/api/v1/security/guest_token/` endpoint with a service account. Do not call this endpoint from client-side code.

Rules from the docs:
- Tokens expire; the lifetime is `GUEST_TOKEN_JWT_EXP_SECONDS`, default 5 minutes. Refresh tokens before they expire using a refresh mechanism in the host app.
- Row-level security: pass `rls` rules in the guest token request to restrict which rows the embedded user sees. Semantic views cannot enforce guest-token SQL clauses, so queries on them are rejected when a global rule or a rule scoped to that view applies.
- Datasource scope: access is bound to the datasource type and identifier; when the optional guest-token datasets allowlist is present, only the listed SQL datasets are reachable.
- Guest tokens give access to data sources reachable through their authorised dashboards, not to SQL Lab queries or ad hoc SQL.
- Allowed Domains: set per dashboard in the Embed settings modal; Superset checks the Referer header against the list, and an empty list allows any origin, so configure it for production.
- API responses to a guest report a generic "An error occurred while fetching the data." instead of engine errors; the full error is in the server logs.
- `GUEST_TOKEN_JWT_SECRET` signs guest tokens. A forged token means unauthorised dashboard and data access; the security guide suggests rotating it quarterly and after incidents, and notes that rotating it invalidates outstanding guest tokens. (`PREVIOUS_JWT_SECRET` is described only for rotating the websocket secret, not this one.)
- Optional `GUEST_TOKEN_HEADER_MAX_BYTES` (default None) sets a diagnostic budget for the token header size, since proxies may reject large tokens; it does not raise any proxy limit. Large inline RLS ID lists can be replaced by a compact entitlements-table subquery.
- `show_download` on embedded permalinks is opt-in; with the `GRANULAR_EXPORT_CONTROLS` feature flag it needs the `can_export_data` permission, otherwise `can_csv`.

## Checked

Confirmed against the Superset docs pages "Embedding" and "Securing Superset": endpoint, service account rule, expiry default, rls, allowlist, Allowed Domains, header budget and secret rotation. Corrected the earlier claim that `PREVIOUS_JWT_SECRET` rotates the guest token secret and removed `GUEST_ROLE_NAME` and the request body field list, which these pages do not give.

Method: docs-only read of cited pages, 2026-11-08
