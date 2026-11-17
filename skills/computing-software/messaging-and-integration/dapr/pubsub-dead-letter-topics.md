---
id: computing-software.messaging-and-integration.dapr.pubsub-dead-letter-topics
name: pubsub-dead-letter-topics
category: computing-software
field: messaging-and-integration
product: dapr
tags: [pubsub, dead-letter, deadlettertopic, retries, resiliency, subscription, poison-messages]
level: practitioner
status: docs-checked
description: "Route undeliverable Dapr pub/sub messages to a dead letter topic with deadLetterTopic in declarative, streaming and programmatic subscriptions, plus a retry policy."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/pubsub/pubsub-deadletter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A dead letter topic receives messages that Dapr could not deliver to the app, for example after the handler returned an error. Dapr enables this for every pub/sub component even if the broker has no native dead letter feature.

Declarative subscription, scoped to app `checkout`:

```yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: order
spec:
  topic: orders
  routes: 
    default: /checkout
  pubsubname: pubsub
  deadLetterTopic: poisonMessages
scopes:
- checkout
```

Programmatic: add `deadLetterTopic: "poisonMessages"` next to `pubsubname`, `topic` and `route` in the JSON from `/dapr/subscribe`. Streaming: the Go SDK takes `DeadLetterTopic` in `SubscriptionOptions`.

Retries: by default, once a dead letter topic is set, a failing message goes there immediately, so always add a retry policy. This Resiliency resource retries every 5 seconds up to 10 times on the inbound side of the `pubsub` component:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Resiliency
metadata:
  name: myresiliency
spec:
  policies:
    retries:
      pubsubRetry:
        policy: constant
        duration: 5s
        maxRetries: 10
  targets:
    components:
      pubsub:
        inbound:
          retry: pubsubRetry
```

Finally subscribe to `poisonMessages` with a second Subscription (same or another app) whose route handles failed messages, for example path `/failedMessages`.

## Checked

2026-11-04. Subscription settings, retry default and example Resiliency YAML confirmed on the Dead Letter Topics page.

Method: documentation only; no commands were run.
