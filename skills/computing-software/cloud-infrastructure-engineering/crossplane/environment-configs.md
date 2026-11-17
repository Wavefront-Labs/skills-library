---
id: computing-software.cloud-infrastructure-engineering.crossplane.environment-configs
name: environment-configs
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [environmentconfig, function-environment-configs, context, in-memory]
level: practitioner
status: docs-checked
description: "Store shared data in EnvironmentConfigs and select them in a pipeline with function-environment-configs."
sources:
  - https://docs.crossplane.io/latest/composition/environment-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An `EnvironmentConfig` is a cluster-scoped, ConfigMap-like object with a free-form `data` field.

```yaml
apiVersion: apiextensions.crossplane.io/v1beta1
kind: EnvironmentConfig
metadata:
  name: example-environment
data:
  locations:
    us: us-east-2
    eu: eu-north-1
```

Since Crossplane v1.18 the native environment is gone. Use function-environment-configs as a pipeline step. It merges the selected configs, in listed order, into the pipeline context at key `apiextensions.crossplane.io/environment` for later steps.

```yaml
input:
  apiVersion: environmentconfigs.fn.crossplane.io/v1beta1
  kind: Input
  spec:
    environmentConfigs:
    - type: Reference
      ref:
        name: example-environment
    - type: Selector
      selector:
        mode: Multiple
        matchLabels:
        - key: my-label-key
          type: FromCompositeFieldPath
          valueFromFieldPath: spec.parameters.deploy
```

`Reference` selects by name; `Selector` by labels, with each label value `type: Value` (with `value`) or `FromCompositeFieldPath` (with `valueFromFieldPath`). Selector `mode: Single` errors on multiple matches; `Multiple` returns all, bounded by `minMatch` and `maxMatch`, sorted by name or `sortByFieldPath`.

Convert old `spec.environment` compositions with `crossplane beta convert pipeline-composition`.

Reference configs in the order you want them merged; later entries overwrite earlier keys.

## Checked

Checked against the Environment Configs page, read in full. Removed the RBAC advice sentence, which the page does not state.

Method: docs-checked 2026-11-09 against the composition/environment-configs page (docs repo raw markdown).
