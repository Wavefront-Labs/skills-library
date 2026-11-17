---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventsource-filtering-expressions
name: argo-events-eventsource-filtering-expressions
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, filter, expression, expr, kafka, eventsource, jsonbody]
level: practitioner
status: docs-checked
description: "Drop unwanted messages at the EventSource with a filter expression evaluated by the expr library, such as a Kafka body condition."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/filtering.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventsource filtering expressions

Some EventSources (for example Kafka) ingest every message from the source. A `filter` with an `expression` lets the EventSource decide whether to publish or skip each event. The string is evaluated with the `expr` package, which offers a wide set of operators and comparators.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: kafka
spec:
  kafka:
    example:
      url: kafka.argo-events:9092
      topic: topic-2
      jsonBody: true
      partition: "1"
      filter:
        expression: "(body.id == 4) && (body.name != 'Joe')"
      connectionBackoff:
        duration: 10s
        steps: 5
        factor: 2
        jitter: 0.2
```

The example expression reads fields as `body.id` and `body.name` with `jsonBody: true`. Producing `{"id": 4, "name": "John", ...}` to the topic (the page uses `kcat`) passes the filter, and the EventSource pod logs `dispatching event on the data channel...` followed by `succeeded to publish an event`. A message with `"id": 2` fails the filter conditions.

## Checked

2026-11-04. Confirmed against the Filtering EventSources page: purpose, the Kafka YAML, `expr` evaluation, the passing and failing example messages and the success log lines. Removed the claim that `jsonBody` is what makes `body.<field>` addressable, the statement that the failing message is "never published" (the page shows only the success logs) and the comparison with Sensor-side filters, none of which the page states.
Method: documentation only; no commands were run.
