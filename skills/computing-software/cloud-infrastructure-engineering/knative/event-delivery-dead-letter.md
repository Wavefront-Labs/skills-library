---
id: computing-software.cloud-infrastructure-engineering.knative.event-delivery-dead-letter
name: event-delivery-dead-letter
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [delivery, deadlettersink, backoffpolicy, backoffdelay, retry, dead-letter]
level: practitioner
status: docs-checked
description: "Configure retries, backoff and a dead letter sink in the delivery spec of Subscriptions and Brokers."
sources:
  - https://knative.dev/docs/eventing/event-delivery/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make event delivery survive failing subscribers and capture events that never succeed.

A `delivery` spec on a Subscription or Broker holds these fields:
- `deadLetterSink`: where undeliverable events go. It is a reference to a Service or a URI; for a Broker it can be any Addressable that conforms to the sink contract.
- `retry`: number of retries. The initial attempt is not counted, so total attempts equal `retry` + 1.
- `backoffDelay`: ISO 8601 duration, for example `PT1S`.
- `backoffPolicy`: `linear` or `exponential`. Linear increases the delay by the interval on each retry; exponential waits `backoffDelay*2^<numberOfRetries>`. The page words this inconsistently: the Subscription section says the linear delay is "the time interval specified between retries" and gives the exponential formula, while the Broker section says linear is a linearly increasing delay and exponential is a multiplier of the interval without the formula.

```yaml
spec:
  delivery:
    deadLetterSink:
      ref:
        apiVersion: serving.knative.dev/v1
        kind: Service
        name: example-sink
    retry: 3
    backoffPolicy: exponential
    backoffDelay: PT1S
```

Support varies by implementation:
- Broker: the Google Cloud broker needs a Pub/Sub topic URI as `deadLetterSink` and supports exponential backoff only; the Kafka broker and RabbitMQ broker support the parameters; MTChannelBasedBroker depends on its underlying Channel.
- Channels: In-Memory and Kafka support all four parameters, while GCP PubSub and Natss support none.

Depending on the Channel implementation, events sent to the dead letter sink may carry extension attributes: `knativeerrordest`, `knativeerrorcode` (the final HTTP status) and `knativeerrordata` (the response body of the final dispatch attempt; empty if the body is empty, and may be truncated if long).

## Checked

2026-11-04. Confirmed against the Handling Delivery Failure page (knative/docs source): `deadLetterSink`, `retry`, `backoffDelay`, `backoffPolicy` and their meanings, the initial attempt not counted in `retry`, the example, the Broker support table (googlecloud, Kafka, MTChannelBasedBroker, RabbitMQBroker), the googlecloud note (Pub/Sub topic URI, exponential only), the Channel support table (In-Memory and Kafka support all four, GCP PubSub and Natss none), and the three `knativeerror*` extension attributes. Conflict inside the page: the Subscription and Broker sections describe the `linear` and `exponential` policies differently; the skill now says so. Qualified the extension attributes as Channel-implementation dependent, as the page does.

Method: documentation only; no commands were run.
