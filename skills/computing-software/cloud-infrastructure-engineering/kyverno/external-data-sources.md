---
id: computing-software.cloud-infrastructure-engineering.kyverno.external-data-sources
name: external-data-sources
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [apicall, configmap-context, globalcontextentry, globalreference, urlpath, refreshinterval]
level: advanced
status: docs-checked
description: "Pull outside data into Kyverno rules: ConfigMap contexts, apiCall to Kubernetes or HTTP services, and GlobalContextEntry caches."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/external-data-sources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ConfigMap context: `context` entry with `name` and `configMap` (`name`, `namespace`); read `{{ <context>.data.<key> }}` at evaluation time. Quote names with `-` or `/`. Arrays stored as strings use `parse_json()` or `parse_yaml()`. Label a ConfigMap `cache.kyverno.io/enabled: "true"` to have Kyverno cache it.

`apiCall`:
- `urlPath`: Kubernetes API path (`/api/v1/namespaces/{{request.namespace}}/pods`); variables and query parameters allowed. Find paths with `kubectl api-resources` and `kubectl api-versions`.
- `jmesPath` transforms the response; `method` defaults to `GET`, `POST` takes `data` key/values; `default` is used if the API errors.
- A named resource that does not exist fails; a list with `fieldSelector` returns empty instead.
- `service`: `url` (exclusive with `urlPath`), `caBundle`, `headers`. JSON responses only. Without an `Authorization` header Kyverno injects a scoped ServiceAccount token.

GlobalContextEntry (`kyverno.io/v2alpha1`):
- `kubernetesResource` (`group`, `version`, `resource` lowercase plural, optional `namespace`; omit for cluster-wide), informer-updated, one kind per entry.
- `apiCall` (`urlPath` or `service`, `refreshInterval`), polled; results wrapped in `items[]`.
- Used via a `context` entry with `globalReference` (`name`, optional `jmesPath`).

Caveats: `apiCall` entries can be stale between refreshes; an entry must be ready or policies referencing it are not processed (and creating such a policy prints a warning); data shape differs between the two entry types so JMESPath must match. Test in the CLI by injecting entries through a values file with `kyverno apply`.

## Checked

2026-11-08. Read the Kyverno External Data Sources page for ConfigMap lookups and caching, Kubernetes API calls (urlPath, method, query parameters, default), service calls (caBundle, url, Authorization handling), and GlobalContextEntry (kubernetesResource, apiCall, refreshInterval, globalReference, readiness and CLI values file). The description was shortened. The service-call example policy and header-variable sections were read only in part.

Method: documentation only; no commands were run.
