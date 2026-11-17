---
id: computing-software.cloud-infrastructure-engineering.knative.sequence-flow
name: sequence-flow
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [sequence, flows, channeltemplate, steps, reply, hairpin]
level: practitioner
status: docs-checked
description: "Chain ordered processing steps with a Sequence, which builds Channels and Subscriptions for you."
sources:
  - https://knative.dev/docs/eventing/flows/sequence/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run functions in a fixed order, each able to modify, filter or create events.

The Sequence CRD defines an in-order list of functions to invoke. It creates Channels and Subscriptions under the hood.

Requirement: a Sequence needs hairpin traffic, meaning your pod can reach itself through the service IP. If that is not available, ask your cluster administrator, since it is typically a CNI setting.

Spec parts:
1. `steps`: the in-order list of subscribers, specified like a Subscription's subscriber (`messaging.v1.SubscriberSpec`). Each step must be Addressable.
2. `channelTemplate`: the template used to create the Channels between steps.
3. `reply` (optional): where the result of the final step goes.

Status parts:
- `conditions` for the overall state.
- `channelStatuses`: one entry per step; the first is the Channel before the first step.
- `subscriptionStatuses`: one entry per step; the first wires the first Channel to the first step.
- `address`: lets the Sequence be used wherever an Addressable can be; sending to it targets the Channel fronting the first step.

Illustrative spec (the service names are examples, not from the page):

```yaml
spec:
  channelTemplate:
    apiVersion: messaging.knative.dev/v1
    kind: InMemoryChannel
  steps:
    - ref: {apiVersion: serving.knative.dev/v1, kind: Service, name: first}
    - ref: {apiVersion: serving.knative.dev/v1, kind: Service, name: second}
  reply:
    ref: {apiVersion: serving.knative.dev/v1, kind: Service, name: event-display}
```

## Checked

2026-11-04. Confirmed against the Sequence page (knative/docs source): an in-order list of functions where each step can modify, filter or create events, Channels and Subscriptions created under the hood, the hairpin traffic requirement and the cluster-administrator (CNI) note, the three Spec parts (`Steps` using `messaging.v1.SubscriberSpec` and each Addressable, `ChannelTemplate`, optional `Reply`) and the four Status parts (conditions, ChannelStatuses, SubscriptionStatuses, AddressStatus targeting the Channel before the first step). The YAML example is illustrative and is now labelled so. Nothing removed.

Method: documentation only; no commands were run.
