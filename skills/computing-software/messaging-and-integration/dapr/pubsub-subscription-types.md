---
id: computing-software.messaging-and-integration.dapr.pubsub-subscription-types
name: pubsub-subscription-types
category: computing-software
field: messaging-and-integration
product: dapr
tags: [pubsub, subscription, declarative, streaming, programmatic, routes, scopes, hot-reload]
level: practitioner
status: docs-checked
description: "Choose between declarative, streaming and programmatic Dapr pub/sub subscriptions: the v2alpha1 Subscription YAML, route rules and streaming limits."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/pubsub/subscription-methods.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dapr offers three subscription types with the same features.

Declarative: defined in an external file, so app code has no Dapr dependency. Example:

```yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: order
spec:
  topic: orders
  routes:
    default: /orders
  pubsubname: pubsub
scopes:
- orderprocessing
```

The subscription `order` reads topic `orders` from the `pubsub` component, delivers every message to the app's `/orders` endpoint, and is limited by `scopes` to app ID `orderprocessing`. Self-hosted, point at the folder with `dapr run --app-id myapp --resources-path ./myComponents -- python3 app.py`; on Kubernetes use `kubectl apply -f subscription.yaml`. Hot reload of declarative subscriptions is a preview feature behind the `HotReload` feature gate; in-flight messages are unaffected.

Streaming: defined in code, dynamic (start and stop at runtime). The app pulls messages from Dapr, so no endpoint is needed and no app port must be configured on the sidecar. There are no routes and no bulk subscriptions. Only a single pubsub/topic pair per application may be subscribed at a time. Each message must be answered success, retry or drop.

Programmatic: defined in code, static. The app serves `GET /dapr/subscribe` returning JSON with `pubsubname`, `topic` and `routes` (a `rules` list of `match` expression plus `path`, and a `default`). It is read once at startup, so subscriptions cannot be added dynamically.

## Checked

2026-11-08. Three subscription types, the Subscription YAML, run and apply commands, HotReload note, streaming properties (no endpoint, no routes or bulk, single pubsub/topic pair) and the programmatic dapr/subscribe format confirmed on the subscription types page. All claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
