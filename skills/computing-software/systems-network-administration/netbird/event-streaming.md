---
id: computing-software.systems-network-administration.netbird.event-streaming
name: event-streaming
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, event-streaming, siem, delivery-retries, streaming-cache-ttl]
level: practitioner
status: docs-checked
description: "Stream NetBird audit and traffic events to SIEM destinations: supported targets, delivery and retry behaviour, cache delay, data redaction and audit trail."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/activity/event-streaming/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available in NetBird Cloud and self-hosted with an enterprise licence; not in the open source self-hosted version.

Destinations: Datadog, Amazon S3, Amazon Data Firehose, SentinelOne Data Lake, Generic HTTP, Wazuh.

Delivery:
- Each audit and traffic event is streamed after it is saved; a failed event stays in the audit log or traffic store, so it is not lost.
- Datadog: one attempt, no retry.
- Generic HTTP: two retries after 1 second then 2 seconds, three attempts total before the event is dropped.

Timing: destination settings are cached, so changes can take up to five minutes. After disabling or deleting a destination, events may keep arriving for up to five minutes, including the event recording the change. Self-hosted Enterprise sets this with `NB_EVENT_STREAMING_CACHE_TTL` on the management server and the enricher service.

Data handling: `name` and `email` keys are removed from `meta` before streaming. For many audit events (group, policy, peer changes) the object name is therefore missing; look it up in the audit log via `target_id`.

Audit: creating, updating, deleting, enabling or disabling a destination logs `Integration created`, `Integration updated` or `Integration deleted`.

## Checked

2026-11-04. Confirmed against the NetBird event streaming overview page: availability, destination list, delivery and retry behaviour, five-minute cache, `NB_EVENT_STREAMING_CACHE_TTL`, name and email removal from meta, audit entries. Nothing removed.
Method: documentation only; no commands were run.
