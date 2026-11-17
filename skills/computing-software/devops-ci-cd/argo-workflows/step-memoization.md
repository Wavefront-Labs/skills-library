---
id: computing-software.devops-ci-cd.argo-workflows.step-memoization
name: step-memoization
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [memoize, memoization, cache-configmap, max-age, configmap-type]
level: practitioner
status: docs-checked
description: "Cache template outputs in a ConfigMap with memoize key, maxAge and cache.configMap, including the RBAC verbs required and the 1MB ConfigMap limit."
sources: ["https://argo-workflows.readthedocs.io/en/latest/memoization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step level memoization
Memoization records a template's outputs under a key so later runs skip the work. Any step can be memoized, with or without outputs. It is configured per template:

```yaml
memoize:
  key: "{{inputs.parameters.message}}"
  maxAge: "10s"
  cache:
    configMap:
      name: print-message-cache
```

`key` is required and may be a static string, though usually it derives from inputs. `cache.configMap.name` names the cache. `maxAge` is optional, written like `180s` or `24h`; entries older than it are ignored.

Storage is a Kubernetes ConfigMap, so you can inspect or edit entries with `kubectl`. A ConfigMap only works as a cache if it carries the label `workflows.argoproj.io/configmap-type: Cache`, which stops Argo touching unrelated ConfigMaps.

Permissions: add the `create` and `update` verbs on `configmaps` to the controller role. For a cluster install edit the `argo-cluster-role` ClusterRole; for a namespace install edit `argo-role`.

Gotcha: a ConfigMap is capped at 1048576 characters. The error `ConfigMap ... is invalid: Too long: must have at most 1048576 characters` means the cache is full. Remedies listed: delete the ConfigMap or use another cache, shrink the memoized output parameters, or split entries across different keys and cache names so each stays small.

## Checked
2026-11-03. Confirmed against the Argo Workflows Step Level Memoization page: ConfigMap storage and label, key, cache name and maxAge rules, the create and update verbs and role names, and the FAQ error and remedies. Nothing removed.
Method: documentation only; no commands were run.
