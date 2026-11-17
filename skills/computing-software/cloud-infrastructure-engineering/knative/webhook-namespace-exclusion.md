---
id: computing-software.cloud-infrastructure-engineering.knative.webhook-namespace-exclusion
name: webhook-namespace-exclusion
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [webhook, webhooks-knative-dev-exclude, namespace-exclusion, upgrade]
level: advanced
status: docs-checked
description: "Label namespaces so the Knative webhook skips them, avoiding upgrade issues."
sources:
  - https://knative.dev/docs/serving/webhook-customizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: prevent a non-responsive Knative webhook from blocking operations in system namespaces.

The Knative webhook examines resources that are created, read, updated or deleted. That includes system namespaces, which can cause trouble during an upgrade if the webhook becomes non-responsive. Cluster administrators may want the webhook disabled on those namespaces.

Label a namespace with `webhooks.knative.dev/exclude` set to `"true"` so it bypasses the webhook:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: knative-dev
  labels:
    webhooks.knative.dev/exclude: "true"
```

The label goes on the Namespace object, as in the manifest above. The page is aimed at system namespaces, where a non-responsive webhook can cause issues during an upgrade.

## Checked

Method: docs-checked 2026-11-09 against the Exclude namespaces from the Knative webhook page (raw markdown in knative/docs, read in full). Dropped the kubectl label command and the advice about when to apply the label, which the page does not state.
