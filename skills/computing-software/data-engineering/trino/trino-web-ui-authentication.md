---
id: computing-software.data-engineering.trino.trino-web-ui-authentication
name: trino-web-ui-authentication
category: computing-software
field: data-engineering
product: trino
tags: [web-ui, web-ui-enabled, fixed-authentication, form-authentication, query-rules]
level: practitioner
status: docs-checked
description: "Secure and configure the Trino Web UI at /ui: authentication types, fixed user, who can view or kill queries, and legacy UI path."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/web-interface.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino web ui authentication

The Web UI on the coordinator is served at `/ui` over the coordinator's HTTP or HTTPS port; the legacy UI stays at `/ui/legacy`. Disable it entirely with `web-ui.enabled=false`. Further options are in the web interface properties.

Authentication is always required in the UI. If Trino itself does not require authentication, any username works, with no password allowed. Users normally sign in with the username they use for queries.

Types:
- Password authentication: when the server uses a password authenticator (LDAP or password file), the UI type is automatically `FORM` and shows a login form.
- `FIXED`: set `web-ui.user` and the UI is open to anyone using that single identity. If a system access control is installed, that user needs permission to view, and possibly kill, queries.
- `CERTIFICATE`, `KERBEROS`, `JWT` and `OAUTH2`: the username comes from the user mapping rules.

Authorization: with no system access control installed, everyone can view and kill any query. Restrict this with query rules in the built-in system access control. Users can always view or kill their own queries.

Query history shown in the UI is governed by `query.min-expire-age` and `query.max-history`. To publish query started or finished events to an external system, use an event listener instead; that is separate from in-memory history.

## Checked

2026-11-09. Pages read in full against this skill:
- https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/web-interface.md

Confirmed (page read as raw markdown): /ui and /ui/legacy paths, web-ui.enabled, authentication behaviour, FORM, FIXED and other types, query rules authorization, query history properties and event listeners.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
