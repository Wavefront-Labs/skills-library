---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-mutation-location-values-and-pathtests
name: opa-gatekeeper-mutation-location-values-and-pathtests
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, mutation, location, pathtests, frommetadata, list-selector, wildcard]
level: advanced
status: docs-checked
description: "Write Gatekeeper mutator locations with list selectors and wildcards, set values from metadata, and guard changes with MustExist and MustNotExist path tests."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/mutation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper mutation location values and pathtests

`location` is a dotted path. A list element is selected by key: `spec.containers[name: foo].imagePullPolicy` means the container named foo in `spec`. A wildcard value matches all elements: `spec.containers[name: *].imagePullPolicy`. The value under `parameters.assign.value` may be a scalar or a composite object, for example a whole sidecar definition assigned at `spec.containers[name: networking]`.

`fromMetadata` (Assign and AssignMetadata, not ModifySet) copies a metadata field instead of a literal; valid `field` values are `namespace` and `name`:

```yaml
location: "metadata.labels.namespace"
parameters:
  assign:
    fromMetadata:
      field: namespace
```

`pathTests` make a mutation conditional on whether a path exists, to set a default only when a field is undeclared, or to avoid creating an empty sidecar when its parent is missing:

```yaml
parameters:
  pathTests:
    - subPath: "spec.containers[name: foo]"
      condition: MustExist
    - subPath: "spec.containers[name: foo].securityContext.capabilities"
      condition: MustNotExist
```

Example from the docs: set `spec.containers[name:foo].securityContext.privileged` to false in namespace bar, guarded by MustExist on the container.

## Checked

2026-11-08: read the whole of website/docs/mutation.md in the Gatekeeper repo (Intent, fromMetadata, Conditionals and the privileged example). Confirmed every claim; nothing removed.

Method: documentation only; no commands were run.
