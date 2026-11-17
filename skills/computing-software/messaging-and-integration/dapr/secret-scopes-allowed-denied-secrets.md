---
id: computing-software.messaging-and-integration.dapr.secret-scopes-allowed-denied-secrets
name: secret-scopes-allowed-denied-secrets
category: computing-software
field: messaging-and-integration
product: dapr
tags: [secrets, secret-scopes, allowedsecrets, deniedsecrets, defaultaccess, configuration, kubernetes-secret-store]
level: advanced
status: docs-checked
description: "Limit which secrets an app can read with secrets.scopes in a Configuration: storeName, defaultAccess, allowedSecrets, deniedSecrets, priority, denying Kubernetes store."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/secret-scope.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Beyond scoping which apps can use a secret store component, a Configuration can scope individual secrets per store:

```yml
secrets:
  scopes:
    - storeName: kubernetes
      defaultAccess: allow
      allowedSecrets: ["redis-password"]
    - storeName: localstore
      defaultAccess: allow
      deniedSecrets: ["redis-password"]
```

Properties: `storeName` (unique in the list), `defaultAccess` (`allow` default, or `deny`), `allowedSecrets`, `deniedSecrets`. The lists take priority over `defaultAccess`; a non-empty `allowedSecrets` means only those secrets are readable.

Outcome table:

- default only: the default decides.
- `deny` + allowed `["s1"]`: only s1 readable.
- `allow` + denied `["s1"]`: everything except s1.
- `allow` + allowed `["s1"]`: only s1 readable.
- `deny` + denied `["s1"]`: deny.
- either default with allowed `["s1"]` and denied `["s2"]`: only s1.

Deny an app all access to the built-in Kubernetes store (added by default on Kubernetes):

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  secrets:
    scopes:
      - storeName: kubernetes
        defaultAccess: deny
```

Apply with `kubectl apply -f appconfig.yaml`, then annotate the pod with `dapr.io/config: appconfig`.

Allow only some secrets in a store named `vault`: `defaultAccess: deny` with `allowedSecrets: ["secret1", "secret2"]`. Block sensitive ones: `defaultAccess: allow` (the default, can be omitted) with `deniedSecrets: ["secret1", "secret2"]`.

## Checked

2026-11-04. Properties, permission priority table and three example scenarios confirmed on the limit secrets read from secret stores page.

Method: documentation only; no commands were run.
