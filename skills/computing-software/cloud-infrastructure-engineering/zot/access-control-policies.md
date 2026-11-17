---
id: computing-software.cloud-infrastructure-engineering.zot.access-control-policies
name: access-control-policies
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, access-control, default-policy, admin-policy, anonymous-policy, repository-glob, disable-anonymous-catalog]
level: practitioner
status: docs-checked
description: "Write Zot accessControl policies: default, user, group, anonymous, metrics and admin policies, glob matching, evaluation order and admin-only routes."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policies live under `http.accessControl.repositories.<pattern>` (before v2.0.0 they sat directly under `accessControl`).

| Policy | Attribute | Purpose |
|---|---|---|
| Default | `defaultPolicy` | Authenticated users matching no user rule |
| User | `policies[].users`, `actions` | Named users |
| Group | `groups`, `actions` | Named groups; defined in `accessControl.groups` |
| Anonymous | `anonymousPolicy` | Unauthenticated users |
| Metrics | `metrics` | Read access to metrics |
| Admin | `adminPolicy` | Global actions on any repository |

Evaluation order: user-specific, group-specific, then default and admin.

- Patterns are explicit paths or globs (`*`, `**`); the longest match wins, and `**` is the fallback. `infra/*` covers only direct children.
- Always include `read`; `create`, `update` and `delete` do not work without it.
- `/v2/_zot/pprof/` profiling and cosign/notation key upload routes need an `adminPolicy` match. With no `accessControl`, nobody can use them. Unauthenticated gets `401`, non-matching `403`.
- Set `accessControl.disableAnonymousCatalog: true` so anonymous `GET /v2/_catalog` returns `401` while permitted anonymous pulls still work (default `false`, hot-reloadable).
- Sessions and API keys also join `accessControl.groups.<name>.users` lists containing their username.

## Checked

2026-11-04. Read against the zot authn-authz article (access control policies, admin-only routes, disableAnonymousCatalog sections); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
