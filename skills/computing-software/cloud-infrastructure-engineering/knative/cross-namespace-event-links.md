---
id: computing-software.cloud-infrastructure-engineering.knative.cross-namespace-event-links
name: cross-namespace-event-links
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [cross-namespace-event-links, knsubscribe, rbac, trigger-namespace, subscription-namespace]
level: advanced
status: docs-checked
description: "Allow Triggers and Subscriptions to reference a Broker or Channel in another namespace using the knsubscribe verb."
sources:
  - https://knative.dev/docs/eventing/features/cross-namespace-event-links/
  - https://knative.dev/docs/eventing/features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a team subscribe to a shared Broker or Channel that lives in a different namespace.

The `cross-namespace-event-links` feature (Alpha, disabled by default) allows Triggers and Subscriptions, called event links, to refer to a Broker or Channel in another namespace. Without it, the Trigger or Subscription must sit in the same namespace as the Broker or Channel.

Authorization uses a new RBAC verb, `knsubscribe`. A user must hold it to create a Trigger or Subscription that references a Broker or Channel in another namespace. Example Role in namespace `ns-1`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: example-cross-namespace-role
  namespace: ns-1
rules:
  - apiGroups: ["eventing.knative.dev"]
    resources: ["brokers"]
    verbs: ["knsubscribe"]
```

This Role gives users the ability to create Triggers referring to a Broker in namespace `ns-1` in every namespace where they are able to create Triggers.

Steps:
1. Enable the `cross-namespace-event-links` flag in the `config-features` ConfigMap of Knative Eventing.
2. Create a Role like the one above in the Broker's namespace, so that users who hold `knsubscribe` can create the cross-namespace links.

This keeps users from subscribing to events from another namespace unless they are allowed to.

## Checked

2026-11-04. Confirmed against the Cross Namespace Event Links page and the Eventing features overview (knative/docs source): flag name, Alpha stage and disabled by default, the same-namespace restriction without the feature, the `knsubscribe` verb, the example Role, and that the Role lets users create Triggers referring to a Broker in `ns-1` in every namespace where they can create Triggers. The features overview confirms flags are set in the `config-features` ConfigMap. Removed the step about binding the Role to users, which the page does not describe.

Method: documentation only; no commands were run.
