---
id: computing-software.messaging-and-integration.strimzi.authorization-and-superusers
name: authorization-and-superusers
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [kafka-authorization, superusers, simple-authorization]
level: advanced
status: docs-checked
description: "Enable authorization and designate super users."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Authorization and super users

**Goal:** restrict what authenticated clients can do.

Configure `Kafka.spec.kafka.authorization`. If the property is missing, no authorization is enabled and clients have no restrictions. When enabled, it applies to **all** enabled listeners. Set the method in `type`: simple, OAuth 2.0 (with OAuth authentication) or custom.

**Super users** can access all resources whatever the restrictions, with every mechanism. List principals in `superUsers`:

- For mTLS, the username is the certificate subject common name prefixed with `CN=`.
- If you use your own certificates for mTLS without the User Operator, it is the full subject, which can include `CN`, `OU`, `O`, `L`, `ST`, `C`; omit fields that do not apply.

```yaml
spec:
  kafka:
    authorization:
      type: simple
      superUsers:
        - CN=client_1
        - user_2
        - CN=client_3
```

ACLs for normal users go in the `KafkaUser` `spec.authorization.acls`.

**Checklist**

1. Always set `authorization.type` explicitly.
2. Use the `CN=` prefix for mTLS principals.
3. Keep the super user list short.

## Checked

2026-11-03. Confirmed in the authorization sections: spec.kafka.authorization with simple/OAuth/custom types, superUsers semantics, CN= prefix for mTLS, and the full-subject rule without the User Operator. Names in the example are placeholders.

Method: documentation only; no commands were run.
