---
id: computing-software.data-science-and-analytics.apache-superset.public-dashboards
name: public-dashboards
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [public-role, anonymous-access, public-role-like, standalone, iframe]
level: practitioner
status: draft
description: "Expose Superset dashboards without login: AUTH_ROLE_PUBLIC, PUBLIC_ROLE_LIKE, per-dashboard grants, ENABLE_VIEWERS and the standalone iframe parameter."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/networking-settings.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/security.mdx
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: share selected dashboards to anonymous viewers.

Mechanism: unauthenticated visitors get the role named by `AUTH_ROLE_PUBLIC` (usually `Public`).

Steps:
1. Set `AUTH_ROLE_PUBLIC = "Public"` in `superset_config.py`.
2. Give that role a base permission set. `PUBLIC_ROLE_LIKE = "Gamma"` makes Public copy Gamma permissions each time `superset init` runs; a more restrictive custom role is safer.
3. Grant the role access to the specific datasets or dashboards to expose, rather than everything.
4. Run `superset init` to re-sync built-in roles.

`ENABLE_VIEWERS` on the same page controls viewer-style access for sharing; check how it interacts with your role setup before relying on it.

Embedding in an iframe: append `standalone=1` to the dashboard URL to hide the Superset chrome (navigation and header). Anonymous embedding in another site also needs the Talisman `frame-ancestors` and CORS settings allowing that origin.

Cautions:
- Public means anyone with the URL can query the underlying data through the permitted datasets; use row level security or a restricted database user.
- For per-user control in an application, prefer embedded dashboards with guest tokens over the Public role.
