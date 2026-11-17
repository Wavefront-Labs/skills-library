---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.server-authn-and-authz
name: server-authn-and-authz
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [authentication, authorization, bearer-token, client-certificates, system-authz]
level: advanced
status: docs-checked
description: "Protect the OPA API with --authentication token or tls and --authorization=basic, how input.identity is set, and the mandatory system.authz policy."
sources:
  - https://www.openpolicyagent.org/docs/security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make OPA verify who calls its API and what they may reach.

Both are flags, and both default to `off`: `--authentication=<scheme>` and `--authorization=<scheme>`. Client-side verification of the OPA endpoint itself is handled with TLS.

Authentication:
- `--authentication=token`: OPA extracts the Bearer token and passes it to the authorisation handler. You must supply an authorisation policy that checks tokens. With no token the `input.identity` value is undefined when the policy evaluates.
- `--authentication=tls`: every client must present a certificate, verified against the CA given by `--tls-ca-cert-file`. On success `input.identity` is the certificate subject. This mode does not disable non-HTTPS listeners, so also require `input.identity` to be set in the authorisation policy.

Authorisation: `--authorization=basic` makes OPA evaluate Rego before serving requests. A minimal policy must be provided at startup, in the reserved `system.authz` package:

```rego
package system.authz

default allow := false

allow if {
    input.method == "POST"
    input.path == [""]
}
```

The `system` namespace is reserved for internal use, and the authorisation policy must be defined under `system.authz`. Tokens and rights can be defined in policy or pushed into OPA as data.

The docs include a worked token-based example and a TLS example with a client ACL that you can adapt.

Check: start with `--authorization=basic`, call `/v1/data` without credentials, and confirm it is refused while the permitted path succeeds.

## Checked

Authentication and authorization flags, the identity values, the system.authz requirement and the worked examples were confirmed against the Security page.

Method: docs-checked 2026-11-09 against the OPA docs security page (docs/docs/security.md in the OPA repository, full file read).
