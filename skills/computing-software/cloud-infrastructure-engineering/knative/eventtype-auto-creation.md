---
id: computing-software.cloud-infrastructure-engineering.knative.eventtype-auto-creation
name: eventtype-auto-creation
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [eventtype, eventtype-auto-create, config-features, discoverability, event-registry]
level: practitioner
status: docs-checked
description: "Auto-create EventType objects from events a Broker or Channel receives by enabling one flag."
sources:
  - https://knative.dev/docs/eventing/features/eventtype-auto-creation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make event types discoverable without hand-written manifests.

With the `eventtype-auto-create` feature (Alpha, disabled by default), Knative creates `EventType` resources for the events received and ingressed by Broker and Channel implementations. Without it, you would write EventType YAML next to the application code that talks to the Broker or Channel API.

Enable it in `config-features` in `knative-eventing`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-features
  namespace: knative-eventing
data:
  eventtype-auto-create: "enabled"
```

To check the feature the page creates a simple Broker, with either of:
- `kn broker create my-broker`
- a Broker YAML applied with `kubectl`.

It then sends events to the Broker (the page shows `kn event send` and a `curl` pod; creation is triggered by processed events) and lists them with `kubectl get eventtypes.eventing.knative.dev -A`. The page presents this as getting EventTypes on the Broker or Channel ingress for free. The flag name is `eventtype-auto-create`, and the persona is Developer. The feature is opt-in. The page strongly recommends creating `EventType` manifests for every event your deployments produce, as part of a GitOps pipeline, rather than relying on auto-creation.

The upstream tracking issue is number 7044 in knative/eventing.

## Checked

2026-11-04. Confirmed against the EventType auto creation page (knative/docs source): flag name `eventtype-auto-create`, Alpha and disabled by default, tracking issue 7044, Developer persona, the `config-features` ConfigMap in `knative-eventing` with the value `enabled`, the Broker creation options, that creation is triggered by processed events, and the listing command. Replaced the unsupported advice about leaving it off with the page's own recommendation to keep EventType manifests in GitOps.

Method: documentation only; no commands were run.
