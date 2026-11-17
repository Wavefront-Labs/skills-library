---
id: computing-software.messaging-and-integration.dapr.configuration-component-denylist
name: configuration-component-denylist
category: computing-software
field: messaging-and-integration
product: dapr
tags: [configuration, components-deny, security, denylist, builtin-k8s-secret-store, policy]
level: advanced
status: docs-checked
description: "Block component types with spec.components.deny in a Dapr Configuration, optionally by version, plus the secretstores.kubernetes catch and the built-in store annotation."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/configuration-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `components.deny` in the Configuration spec to forbid component types from being initialized in that sidecar:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: myappconfig
spec: 
  components:
    deny:
      - bindings.smtp
      - secretstores.local.file
```

You can pin a version by appending it to the type: `state.in-memory/v1` stops components of type `state.in-memory` and version `v1` from initializing, without affecting other versions of that type.

Catch: adding `secretstores.kubernetes` to the list prevents creation of additional components of that type, but does not disable the built-in Kubernetes secret store. That store is created by Dapr automatically and is used to hold the secrets referenced by Component specs. To turn the built-in store off, use the pod annotation `dapr.io/disable-builtin-k8s-secret-store` (listed in the arguments and annotations reference).

A deny list combines naturally with other restrictions in the same Configuration: secret scopes (`secrets.scopes`) and `accessControl` policies, as in the page full example, which denies `bindings.smtp` and `secretstores.local.file` while also configuring tracing, an oauth2 HTTP pipeline handler, a secret scope with `deniedSecrets: ["redis-password"]`, and per-app access control.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
