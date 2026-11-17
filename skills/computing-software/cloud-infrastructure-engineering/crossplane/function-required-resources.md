---
id: computing-software.cloud-infrastructure-engineering.crossplane.function-required-resources
name: function-required-resources
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function, required-resources, requirements, configmap]
level: advanced
status: docs-checked
description: "Give composition functions existing cluster resources via bootstrap requirements or dynamic requests."
sources:
  - https://docs.crossplane.io/latest/composition/compositions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Functions can read existing Kubernetes resources (formerly "extra resources" in v1) to decide desired state.

Bootstrap requirements are declared on the pipeline step and perform better:

```yaml
pipeline:
- step: create-deployment-from-config
  functionRef:
    name: crossplane-contrib-function-python
  requirements:
    requiredResources:
    - requirementName: app-config
      apiVersion: v1
      kind: ConfigMap
      name: app-configuration
      namespace: default
```

The Python SDK reads it with `request.get_required_resource(req, "app-config")`.

Dynamic requests happen at runtime: the function returns the resources it wants (by name or labels, cluster-scoped or namespaced) in its RunFunctionResponse. Crossplane calls it again with those resources, the returned context, and the same input, observed and desired state.

Limits:

- Crossplane stops at 5 iterations.
- The function is satisfied when it returns the identical request twice in a row. Crossplane errors if the requests are not stable after 5 iterations, so request the same resources every time.
- Crossplane must already have RBAC access to the kinds requested.

Bootstrap requirements avoid the extra function calls that dynamic requests need.

## Checked

Checked against the Compositions page, Required resources section and the iteration paragraph, read in full. Removed the unstated claim about requirementName mismatch behaviour.

Method: docs-checked 2026-11-09 against the composition/compositions page (docs repo raw markdown).
