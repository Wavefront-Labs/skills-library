---
id: computing-software.devops-ci-cd.helm.values-schema-validation
name: values-schema-validation
category: computing-software
field: devops-ci-cd
product: helm
tags: [values-schema, json-schema, values-schema-json, validation, skip-schema-validation, required]
level: practitioner
status: docs-checked
description: "Validate chart values with values.schema.json (JSON Schema): when it runs, subchart enforcement and the skip flag."
sources:
  - "https://helm.sh/docs/topics/charts/"
  - "https://helm.sh/docs/helm/helm_install/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A chart can include `values.schema.json` at its root. It is a JSON Schema (the docs use a draft-07-style example) that structures and validates `values`.

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "properties": {
    "image": {
      "type": "object",
      "properties": {
        "repository": {"type": "string"},
        "tag": {"type": "string"}
      }
    }
  },
  "required": ["image"]
}
```

Validation runs during `helm install`, `helm upgrade`, `helm lint` and `helm template`. If the values break the schema the command fails.

The merged final values are checked: values from `values.yaml`, `-f`, `--set` and subcharts. A subchart's own `values.schema.json` is enforced too, so a parent cannot get around a subchart's restrictions.

Pass `--skip-schema-validation` ("disables JSON schema validation") to `helm install`, `helm upgrade`, `helm template` or `helm lint`. The chart docs say it is useful in air-gapped environments when the schema contains remote references.

Tips:

- The example schema marks required keys with a `required` array and sets `"minimum": 0` on an integer.
- `--set-string` forces a string value and `--set-json` sets scalars, objects or arrays, which gives control over types.

## Checked

2026-11-08. Read the Charts topic, helm install, helm upgrade, helm template and helm lint pages (options sections in full). Removed unsupported claims (violation listing, quantity-string and enum tips); confirmed --skip-schema-validation exists on install, upgrade, template and lint.

Method: documentation only; no commands were run.
