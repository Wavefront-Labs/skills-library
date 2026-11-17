---
id: computing-software.messaging-and-integration.dapr.service-invocation-access-control-policies
name: service-invocation-access-control-policies
category: computing-software
field: messaging-and-integration
product: dapr
tags: [service-invocation, access-control, acl, spiffe, trustdomain, configuration, mtls, policies]
level: advanced
status: docs-checked
description: "Restrict which apps can call which operations with accessControl in the called app Configuration: trustDomain, namespace, appId, verb and path rules, priority."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/invoke-allowlist.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The policy sits in the Configuration of the called app's sidecar and matches the caller by the SPIFFE ID in its mTLS cert, `spiffe://<trustdomain>/ns/<namespace>/<appid>`. Dapr asks the Sentry service to generate that SPIFFE ID, which is attached in the TLS cert. Trust domain defaults to `public`.

Properties: `accessControl.defaultAction`, `trustDomain`, `policies`; per policy `appId` (the table says `app`, the examples use `appId`), `namespace`, `trustDomain`, `defaultAction`, `operations`; per operation `name` (wildcard `*`, `**` for multiple path levels), `httpVerb` (list, `*` allowed, unused for gRPC), `action` (`allow` default or `deny`).

Rules:

1. No policy: allow all callers to all methods.
2. No global default and no app policies: same as no policy.
3. No global default but app policies exist: global default becomes deny.
4. Caller credentials cannot be verified: global default applies.
5. Trust domain or namespace mismatch: that app policy is ignored and the global default applies.

Priority: specific HTTP verb (or gRPC operation) action, then app-level default, then global default.

Only `op1` from `app1` allowed:

```yaml
spec:
  accessControl:
    defaultAction: deny
    trustDomain: "public"
    policies:
    - appId: app1
      defaultAction: deny
      trustDomain: 'public'
      namespace: "default"
      operations:
      - name: /op1
        httpVerb: ['*']
        action: allow
```

Allow everything except `/op1/*` from `app1`: use global `defaultAction: allow`, and an operation with `name: /op1/*`, `httpVerb: ['*']`, `action: deny`. Same app ID in different namespaces gets separate policies (ns1 allow, ns2 deny).

## Checked

2026-11-04. Property tables, policy rules, priority order and scenarios 1 to 4 confirmed on the access control list for service invocation page.

Method: documentation only; no commands were run.
