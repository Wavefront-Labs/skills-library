---
id: computing-software.systems-network-administration.incus.authorization-client-routing
name: authorization-client-routing
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, authorization, openfga, scriptlet, tls-restricted, client-routing, security-tags]
level: advanced
status: docs-checked
description: "Control Incus API authorization: the authorization.client.* routing options, built-in defaults, restricted TLS certificates, OpenFGA and scriptlet methods, and lockout warnings."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/authorization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorization and client routing

Unix socket: `incus-admin` members get full access; `incus` members are limited to their own project. Network methods: TLS, OpenFGA, scriptlet.

Routing options and built-in values: `authorization.client.unix` (allow), `.tls` (allow), `.tls-restricted` (tls), `.oidc` (allow), `.default` (deny). Values: `allow`, `deny`, `tls` (tls-restricted only), `openfga`, `scriptlet`.
```
incus config set authorization.client.oidc=openfga
incus config set authorization.client.tls-restricted=scriptlet
```

- TLS: `incus config trust edit <fingerprint>`, set `restricted: true` and `projects`; an empty list means no projects. Restricted clients cannot change global config or their project limits.
- OpenFGA: run your own server; all `authorization.openfga.*` options must be set. Incus writes the model and the tuple `server:incus#authenticated@user:*`. It does not route anything until client routing says so. Do not grant untrusted users `server` admin/operator/can_edit/can_create_*, `certificate` or `storage_pool` can_edit, or `project` admin.
- Scriptlet: `authorization.scriptlet` defines `authorize(details, object, entitlement)` returning a boolean.
- `security.tags` on instances show up in OpenFGA as `security_tag` objects.

Warnings: routing `tls-restricted` away from `tls` drops project restrictions. Set `.default` last; a bad method or `deny` can lock out remote clients. `root` on the Unix socket always works for recovery.

## Checked

2026-11-09. Confirmed against the Incus Authorization page: Unix socket groups, routing options, values and built-in routes, restricted TLS certificates, OpenFGA requirements and model/tuple, relations not to grant, scriptlet authorize signature, security.tags and security_tag objects, both warnings. Nothing removed.
Method: documentation only; no commands were run.
