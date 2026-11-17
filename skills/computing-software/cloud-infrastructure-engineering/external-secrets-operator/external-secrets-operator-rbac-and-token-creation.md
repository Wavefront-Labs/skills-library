---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-rbac-and-token-creation
name: external-secrets-operator-rbac-and-token-creation
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [security, rbac, serviceaccount-token, least-privilege]
level: advanced
status: docs-checked
description: "Lock down ESO RBAC, including removing the blanket serviceaccounts/token create permission with per-ServiceAccount Roles."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/security-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ESO can read and write Secrets in all namespaces, so restrict who can use `pods/exec` in the ESO pod, who can touch `(Cluster)ExternalSecret` and `(Cluster)SecretStore`, and who holds the aggregated view/edit/admin ClusterRoles.

By default the controller role has blanket `serviceaccounts/token: create`, needed for `serviceAccountRef` authentication (for example Vault Kubernetes auth). A compromised ESO could mint tokens for any ServiceAccount in scope. Set `rbac.serviceAccountTokenCreate: false` in the chart, then for each referenced ServiceAccount grant a namespaced Role and RoleBinding:

```yaml
rules:
  - apiGroups: ['']
    resources: ['serviceaccounts/token']
    resourceNames: ['<sa-name>']
    verbs: ['create']
```

bound to the ESO service account. The webhook can also be restricted to chosen TLS ciphers with `webhook.extraArgs.tls-ciphers`.

## Checked

2026-11-03. Claims were read against guides/security-best-practices.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
