---
id: computing-software.messaging-and-integration.dapr.pubsub-cloudevents-envelope
name: pubsub-cloudevents-envelope
category: computing-software
field: messaging-and-integration
product: dapr
tags: [pubsub, cloudevents, envelope, metadata, traceparent, datacontenttype, custom-cloudevent]
level: practitioner
status: docs-checked
description: "The CloudEvents 1.0 envelope Dapr wraps around pub/sub messages, overriding id, source and type via cloudevent.* metadata, or publishing your own envelope."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/pubsub/pubsub-cloudevents.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dapr uses the CloudEvents 1.0 specification as the message format for pub/sub, which provides tracing, a content type for deserialization and verification of the sender application. There are three ways to publish.

1. Plain publish: Dapr wraps the payload in an envelope with `id`, `source`, `specversion`, `type`, `traceparent`, `traceid`, `tracestate`, `topic`, `pubsubname`, `time` and optionally `datacontenttype`. In the page's example output `source` is `checkout`, `type` is `com.dapr.event.sent`, and `data` carries the JSON payload such as `{"orderId": 1}`.

2. Override generated attributes through publish metadata:

- `cloudevent.id` replaces `id`
- `cloudevent.source` replaces `source`
- `cloudevent.type` replaces `type`
- `cloudevent.traceid`, `cloudevent.tracestate`, `cloudevent.traceparent` replace the tracing fields

This works with all pub/sub components. The page warns that replacing trace fields may give inconsistent results in tracing tools and recommends OpenTelemetry for distributed traces. In Python: `publish_metadata={'cloudevent.id': 'd99b228f-6c73-4e78-8c4d-3f80a043d317', 'cloudevent.source': 'payment'}`.

3. Your own envelope: serialize the whole CloudEvent as the data and set the content type to `application/cloudevents+json` (Python `data_content_type='application/cloudevents+json'`). If the event lacks the minimum required attributes of the CloudEvents specification, the message is rejected. Dapr adds any of these that are missing: `time`, `traceid`, `traceparent`, `tracestate`, `topic`, `pubsubname`, `source`, `type` and `specversion`. Extra non-spec fields are passed through as-is. Dapr does not deduplicate automatically; the envelope `id` can be used by the app.

## Checked

2026-11-08. Envelope fields, override keys, the tracing warning and the own-envelope rules confirmed on the CloudEvents page. Changed: the list of fields Dapr adds to a custom CloudEvent was incomplete (now nine fields as listed), and a claim that source is the publishing app ID was removed because the page only shows an example value.

Method: documentation only; every cited page read in full; no commands were run.
