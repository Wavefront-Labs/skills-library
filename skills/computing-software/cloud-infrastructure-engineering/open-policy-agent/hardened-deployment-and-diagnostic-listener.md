---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.hardened-deployment-and-diagnostic-listener
name: hardened-deployment-and-diagnostic-listener
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [hardening, diagnostic-addr, sidecar, bundle-credentials, security-checklist]
level: advanced
status: docs-checked
description: "Run OPA hardened: localhost HTTPS only, restrictive system.authz allowing POST /, bundle credentials via --set-file, and a separate --diagnostic-addr for health and metrics."
sources:
  - https://www.openpolicyagent.org/docs/security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a minimal-exposure OPA deployment.

Rules from the docs: limit API access to host-local clients executing policy queries; use TLS for localhost TCP or a UNIX domain socket; never pass credentials as command-line arguments; run as a non-root user, ideally in its own account.

Pair a bundle-fed OPA with a restrictive authorisation policy that grants only the default decision, `POST /`:

```rego
package system.authz

default allow := false

allow if {
    input.method == "POST"
    input.path == [""]
}
```

```
opa run \
    --server \
    --authorization=basic \
    --addr=https://localhost:8181 \
    --tls-cert-file=/path/to/server.crt \
    --tls-private-key-file=/path/to/server.key \
    --set=bundles.authz.service=default \
    --set=bundles.authz.resource=myapp_authz_bundle \
    --set=services.default.url=https://control.acmecorp.com \
    --set-file=services.default.credentials.bearer.token=/path/to/secret-bearer-token
```

`--set-file` keeps the token out of the process arguments, but the file holds it in plaintext, so restrict its file permissions.

Monitoring a localhost-only sidecar: remote systems cannot reach `/health` or `/metrics`. Add a diagnostic listener:

```
opa run -s --addr localhost:8181 --diagnostic-addr :8282
```

Port 8282 serves only `/health` and `/metrics`; the REST API stays on `localhost:8181`. Those two endpoints remain available on the normal listener too.

Check: from another host, `curl` port 8282 `/health` succeeds and the data API on 8181 is unreachable.

## Checked

2026-11-04. Confirmed against the OPA docs Security page, including the Hardened Configuration Example and the Secure Health and Monitoring section. Nothing removed.

Method: documentation only; no commands were run.
