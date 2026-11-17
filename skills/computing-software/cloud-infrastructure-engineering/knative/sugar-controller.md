---
id: computing-software.cloud-infrastructure-engineering.knative.sugar-controller
name: sugar-controller
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [sugar-controller, config-sugar, namespace-selector, trigger-selector, injection]
level: practitioner
status: docs-checked
description: "Auto-create Brokers for labeled Namespaces or Triggers by configuring config-sugar."
sources:
  - https://knative.dev/docs/eventing/configuration/sugar-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have Eventing create a Broker automatically when a labeled Namespace or Trigger appears.

The default `config-sugar` ConfigMap disables the Sugar Controller by setting both `namespace-selector` and `trigger-selector` to an empty string. To enable it:
- For Namespaces, configure the LabelSelector `namespace-selector`.
- For Triggers, configure the LabelSelector `trigger-selector`.

Sample from the page, enabling it on selected Namespaces and Triggers:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-sugar
  namespace: knative-eventing
data:
  namespace-selector: |
    matchExpressions:
    - key: "eventing.knative.dev/injection"
      operator: "In"
      values: ["enabled"]
  trigger-selector: |
    matchExpressions:
    - key: "eventing.knative.dev/injection"
      operator: "In"
      values: ["enabled"]
```

With this configuration the controller only operates on Namespaces or Triggers carrying the label `eventing.knative.dev/injection: enabled`, which also emulates the legacy Sugar Controller behavior for Namespaces.

Edit the ConfigMap in place with:

```bash
kubectl edit cm config-sugar -n knative-eventing
```

The page links to the Knative Eventing Sugar Controller documentation for a worked example. Until a selector is set, the controller does nothing for that kind of object, because the empty-string default disables it.

## Checked

Method: docs-checked 2026-11-09 against https://knative.dev/docs/eventing/configuration/sugar-configuration/ (read in full; defaults, sample ConfigMap, label and edit command match).
