---
id: computing-software.messaging-and-integration.dapr.pubsub-raw-payloads
name: pubsub-raw-payloads
category: computing-software
field: messaging-and-integration
product: dapr
tags: [pubsub, rawpayload, cloudevents, interoperability, base64, non-dapr, subscription]
level: practitioner
status: docs-checked
description: "Publish and subscribe without CloudEvents for non-Dapr apps using rawPayload metadata, the features this disables, and base64 octet-stream delivery."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/pubsub/pubsub-raw.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Raw payloads let Dapr apps exchange messages with non-Dapr apps that do not expect a CloudEvent envelope.

Publishing: set the `rawPayload` metadata to `true` on the publish request:

```bash
curl -X "POST" http://localhost:3500/v1.0/publish/pubsub/TOPIC_A?metadata.rawPayload=true -H "Content-Type: application/json" -d '{"order-number": "345"}'
```

SDKs pass the same key, for example Python `publish_metadata={'rawPayload': 'true'}` and .NET a metadata dictionary with `rawPayload` and `content-type`.

Warning from the page: not using CloudEvents disables tracing, event deduplication per messageId, content-type metadata and any other feature built on the CloudEvent schema.

Subscribing: Dapr apps can subscribe to messages that were never published as CloudEvents. The subscribing sidecar still wraps them in a CloudEvent before delivery unless you ask otherwise. For a programmatic subscription add a `rawPayload` metadata entry (in .NET the entry is called `isRawPayload`). With raw payloads the message is always base64 encoded with content type `application/octet-stream`.

For a declarative Subscription, put `isRawPayload: "true"` under `spec.metadata` (the page's prose says `rawPayload` but its YAML uses `isRawPayload`), with the app IDs listed in `scopes` (the page uses `app1` and `app2`).

## Checked

2026-11-08. rawPayload publish request, the lost-features warning, subscriber-side wrapping, the .NET isRawPayload name, base64 and octet-stream behaviour and the declarative YAML confirmed on the raw messages page. Changed: dropped the unstated handler advice and noted the page's rawPayload versus isRawPayload inconsistency.

Method: documentation only; every cited page read in full; no commands were run.
