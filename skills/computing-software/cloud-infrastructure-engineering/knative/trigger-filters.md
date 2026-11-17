---
id: computing-software.cloud-infrastructure-engineering.knative.trigger-filters
name: trigger-filters
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [trigger, filters, exact, prefix, suffix, cloudevents-attributes]
level: practitioner
status: docs-checked
description: "Route Broker events to subscribers with exact, prefix, suffix, all and any filter dialects."
sources:
  - https://knative.dev/docs/eventing/triggers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deliver only the events a subscriber cares about.

A Trigger represents a desire to subscribe to events from a specific Broker. Its `subscriber` is a Destination: a `ref` plus an optional `uri` such as `/my-custom-path`, used to deliver to a custom path on a Kubernetes Service.

The `filters` field takes these dialects:
- `exact`: attribute value must equal the given string.
- `prefix` and `suffix`: attribute value must start or end with the string.
- `all`: every nested filter must match.
- `any`: at least one nested filter must match.
- `not`: the nested filter must not match.
- `cesql`: a CloudEvents SQL expression must be true. Knative 1.15+ supports only CloudEvents SQL v1.0, so recheck older expressions.

```yaml
spec:
  broker: default
  filters:
    - exact:
        type: dev.knative.foo.bar
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: my-service
```

Rules:
- Matching is case-sensitive, and non-string attributes are compared as strings.
- When several filters are listed, all of them must be true.
- Filtering on the event `data` is not supported.
- The new-style `filters` are supported only by the Apache Kafka Broker and the MTChannelBasedBroker; other brokers use the legacy `filter.attributes` map, which still works for everyone.
- If both `filters` and the legacy `filter` are set, `filters` overrides `filter`. For example, with `exact` type `dev.knative.a` and legacy type `dev.knative.b`, only `dev.knative.a` events are delivered.

## Checked

Method: docs-checked 2026-11-09 against https://knative.dev/docs/eventing/triggers/ (read in full). Added the `not` and `cesql` dialects from the page.
