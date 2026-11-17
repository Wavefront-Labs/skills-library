---
id: computing-software.messaging-and-integration.dapr.component-namespaces-and-app-scopes
name: component-namespaces-and-app-scopes
category: computing-software
field: messaging-and-integration
product: dapr
tags: [components, namespaces, scopes, namespace-env, self-hosted, kubernetes, access-control]
level: practitioner
status: docs-checked
description: "Restrict Dapr components by namespace (NAMESPACE variable or Kubernetes namespace) and by application using the scopes list of app IDs on the Component resource."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/components/component-scopes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dapr components are namespaced: a sidecar only loads components from its own namespace and ignores the rest.

Self-hosted: set the `NAMESPACE` environment variable. If it is set, Dapr does not load any component that lacks the same `metadata.namespace`.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: production
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
```

```bash
export NAMESPACE=production
# run Dapr as usual
```

On Windows use `setx NAMESPACE "production"`. On Kubernetes the same component is only visible to sidecars running in the `production` namespace.

A component in one namespace can still point at a backing service deployed in another; for example a Redis component in `production-A` may use a Redis host from namespace B. The multi-namespace pub/sub page shows this.

Application scopes narrow access further: add a top-level `scopes` list of app IDs.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: production
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
scopes:
- app1
- app2
```

Only apps `app1` and `app2` can use `statestore`.

## Checked

2026-11-08. NAMESPACE variable behaviour, namespaced component matching, cross-namespace backing service note and the scopes example confirmed on the Scope components page. Changed: dropped the closing remark on secret scopes, which the page only lists as a related link. Other claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
