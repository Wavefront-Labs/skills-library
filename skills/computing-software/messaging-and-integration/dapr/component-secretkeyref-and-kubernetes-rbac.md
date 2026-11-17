---
id: computing-software.messaging-and-integration.dapr.component-secretkeyref-and-kubernetes-rbac
name: component-secretkeyref-and-kubernetes-rbac
category: computing-software
field: messaging-and-integration
product: dapr
tags: [components, secrets, secretkeyref, auth-secretstore, kubernetes-secret, rbac, role, rolebinding]
level: practitioner
status: docs-checked
description: "Keep credentials out of Component YAML with secretKeyRef and auth.secretStore: the two secret shapes, a Kubernetes example, and the Role and RoleBinding for other namespaces."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/components/component-secrets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Component metadata may hold plain text, but the page says that is not recommended for production. Reference a secret instead, and name the store in `auth.secretStore`. On Kubernetes an empty `auth.secretStore` means the built-in Kubernetes secret store.

Secret with an embedded key (not a whole connection string):

```yml
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key:  redis-password
auth:
  secretStore: <SECRET_STORE_NAME>
```

Secret that is just a string: put the secret name in both `name` and `key`:

```yml
  - name: connectionString
    secretKeyRef:
      name: asbNsConnString
      key: asbNsConnString
```

Kubernetes example for an Event Hubs binding:

```bash
kubectl create secret generic eventhubs-secret --from-literal=connectionString=*********
kubectl apply -f ./eventhubs.yaml
```

with the component using `secretKeyRef` `name: eventhubs-secret`, `key: connectionString`.

Permissions: on installation Dapr defines a Role and RoleBinding for reading Kubernetes secrets in the `default` namespace. For components in other namespaces apply them yourself:

```yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: <NAMESPACE>
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: dapr-secret-reader
  namespace: <NAMESPACE>
subjects:
- kind: ServiceAccount
  name: default
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

In production restrict the Role with `resourceNames`. Secret scoping in a Configuration limits what apps may read.

## Checked

2026-11-08. Plain-text warning, auth.secretStore default on Kubernetes, both secretKeyRef shapes, the Event Hubs example, default-namespace Role and RoleBinding behaviour, the non-default-namespace YAML and the resourceNames note confirmed on the Reference secrets in components page. All claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
