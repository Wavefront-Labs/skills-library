---
id: computing-software.cloud-infrastructure-engineering.knative.revision-garbage-collection
name: revision-garbage-collection
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [garbage-collection, config-gc, max-non-active-revisions, retain-since-create-time, min-non-active-revisions]
level: practitioner
status: docs-checked
description: "Control how many inactive Revisions are retained with the config-gc ConfigMap."
sources:
  - https://knative.dev/docs/serving/revisions/revision-admin-config-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound how many old Revisions pile up in the cluster.

Cluster administrators set garbage collection in the `config-gc` ConfigMap in `knative-serving`. Settings:
- `retain-since-create-time`: time that must pass since a Revision was created before it is considered for collection.
- `retain-since-last-active-time`: time since the Revision was last active before it is considered.
- `min-non-active-revisions`: minimum number of inactive Revisions to keep.
- `max-non-active-revisions`: maximum number of inactive Revisions to keep.

A Revision is always retained if any of these hold:
- It is active and referenced by a Route.
- It was created within `retain-since-create-time`.
- A Route last referenced it within `retain-since-last-active-time`.
- Fewer Revisions exist than `min-non-active-revisions`.

Examples from the page.

Clean up inactive Revisions immediately:

```yaml
data:
  min-non-active-revisions: "0"
  max-non-active-revisions: "0"
  retain-since-create-time: "disabled"
  retain-since-last-active-time: "disabled"
```

Retain the last ten inactive Revisions:

```yaml
data:
  retain-since-create-time: "disabled"
  retain-since-last-active-time: "disabled"
  max-non-active-revisions: "10"
```

Disable garbage collection: set `retain-since-create-time`, `retain-since-last-active-time` and `max-non-active-revisions` all to `"disabled"`.

Per-Revision garbage collection behaviour is covered by the developer configuration options page.

## Checked

2026-11-04. Confirmed against the Administrator configuration options page and its included garbage collection snippet (knative/docs source): inactive Revisions are cleaned up automatically after a set time, the `config-gc` ConfigMap in `knative-serving`, the four settings and their descriptions, the four always-retained categories, and the three YAML examples (immediate cleanup, retain ten, disable). The snippet also confirms developers can configure garbage collection for a specific Revision, which the closing line relies on. Nothing changed or removed.

Method: documentation only; no commands were run.
