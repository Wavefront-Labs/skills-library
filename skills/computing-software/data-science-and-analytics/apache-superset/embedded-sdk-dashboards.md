---
id: computing-software.data-science-and-analytics.apache-superset.embedded-sdk-dashboards
name: embedded-sdk-dashboards
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [embedding, embedded-sdk, embed-dashboard, allowed-domains, iframe]
level: practitioner
status: docs-checked
description: "Embed a Superset dashboard with @superset-ui/embedded-sdk: EMBEDDED_SUPERSET flag, embedDashboard options, guest tokens, URL parameters, allowed domains."
sources:
  - https://github.com/apache/superset/blob/master/docs/docs/using-superset/embedding.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: show a dashboard inside your web app.

Prerequisites: the `EMBEDDED_SUPERSET` feature flag is enabled (without it embedDashboard fails to load and the guest token endpoint is unavailable), and an admin has configured the embedding domain and allowed origins.

```bash
npm install @superset-ui/embedded-sdk
```

```js
import { embedDashboard } from '@superset-ui/embedded-sdk';

embedDashboard({
  id: 'dashboard-uuid-here', // from Dashboard > Embed
  supersetDomain: 'https://superset.example.com',
  mountPoint: document.getElementById('superset-container'),
  fetchGuestToken: () => fetchTokenFromYourBackend(),
  dashboardUiConfig: {
    hideTitle: true,
    filters: { expanded: false },
  },
  resolvePermalinkUrl: ({ key }) => `https://myapp.example.com/dashboard?permalink=${key}`,
});
```

- `fetchGuestToken` must return a guest token your server obtains by calling `/api/v1/security/guest_token/` with a service account. Never call that endpoint from client code.
- `resolvePermalinkUrl` lets the host app return a URL on its own domain for a copied permalink; returning null or omitting it falls back to the Superset URL.
- URL parameters can be passed via `urlParams` in `dashboardUiConfig` or appended to the iframe URL: `standalone` (0 normal, 1 hide nav, 2 hide nav and title, 3 hide nav, title and tabs), `show_filters` (0 or 1) and `expand_filters` (0 or 1).
- `DISABLE_EMBEDDED_SUPERSET_LOGOUT` hides the Logout menu item in the embedded view.

Security notes from the page:
- Guest tokens expire; the lifetime is `GUEST_TOKEN_JWT_EXP_SECONDS` (default 5 minutes), so refresh them from the host app.
- Allowed Domains is set per dashboard in the Embed settings modal; Superset checks the request Referer against it, and an empty list allows any origin, so set it for production.
- Pass `rls` rules in the guest token request to restrict visible rows.
- Guest tokens reach data through their authorized dashboards, not SQL Lab queries or ad hoc SQL.
- API responses to a guest report a generic "An error occurred while fetching the data." instead of the underlying engine error; the full error stays in server logs.
- Embedding a single chart by permalink (`/explore/p/<permalink-key>/?standalone=1&show_download=1`) is a separate session-authenticated flow, not the SDK. Cross-site iframes also need `SESSION_COOKIE_SAMESITE = "None"` with `SESSION_COOKIE_SECURE = True`, and browsers that block third-party cookies can still force a login redirect.

## Checked

2026-11-08: read embedding.mdx in full; the Snowflake `EMBEDDED_CREDENTIAL_FALLBACK`, semantic-view and header-size sections are out of scope. Removed `hideChartControls`, tab toggles and Talisman `frame-ancestors` advice for the SDK, which are not on the page.
Method: documentation only; no commands were run.
