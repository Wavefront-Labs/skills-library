---
id: computing-software.cloud-infrastructure-engineering.knative.parallel-flow
name: parallel-flow
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [parallel, branches, filter-subscriber, ingresschannelstatus, fan-out]
level: practitioner
status: docs-checked
description: "Fan one CloudEvent out to several branches, each with an optional filter, subscriber and reply."
sources:
  - https://knative.dev/docs/eventing/flows/parallel/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send the same event to multiple independent processing branches.

The Parallel CRD defines a list of branches, each receiving the same CloudEvent sent to the Parallel ingress Channel. A branch typically has a filter function guarding the execution of its subscriber. Parallel creates Channels and Subscriptions under the hood.

Spec parts:
1. `branches`: a list of `filter` and `subscriber` pairs, plus an optional `reply` per branch.
   - The optional `filter` is evaluated; when it returns an event, the `subscriber` runs. Both must be Addressable.
   - The event returned by the `subscriber` goes to the branch `reply`. When the branch `reply` is empty, the event goes to `spec.reply`.
2. `channelTemplate` (optional): template for the Channels it creates.
3. `reply` (optional): where each branch result goes if the branch has no `reply` of its own.

Status parts:
- `conditions`: overall status.
- `ingressChannelStatus` and `branchesStatuses`: status of the underlying Channel and Subscription resources.
- `address`: lets Parallel be used wherever an Addressable can; sending to it targets the Channel fronting the Parallel, the same as `ingressChannelStatus`.

Illustrative spec (the service names are examples, not from the page):

```yaml
spec:
  branches:
    - filter:
        ref: {apiVersion: serving.knative.dev/v1, kind: Service, name: is-even}
      subscriber:
        ref: {apiVersion: serving.knative.dev/v1, kind: Service, name: handle-even}
  reply:
    ref: {apiVersion: eventing.knative.dev/v1, kind: Broker, name: default}
```

## Checked

2026-11-04. Confirmed against the Parallel page (knative/docs source): branches receiving the same CloudEvent, the optional filter guarding the subscriber, both being Addressable, Channels and Subscriptions created under the hood, the three Spec parts (`branches` with optional `reply`, optional `channelTemplate`, optional `reply`), the reply fallback to `spec.reply`, and the three Status parts (`conditions`, `ingressChannelStatus` with `branchesStatuses`, `address`). The YAML example is illustrative and is now labelled so. Nothing removed.

Method: documentation only; no commands were run.
