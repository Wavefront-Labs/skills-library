---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pubsub-backlog-and-oldest-unacked-message-monitoring
name: pubsub-backlog-and-oldest-unacked-message-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, pubsub, pubsub-monitoring, oldest-unacked-message, backlog-alerts, alerting]
level: practitioner
status: docs-checked
description: "Alert on Pub/Sub subscriber health: oldest unacked message age, backlog size, expired ack deadlines, delivery latency health score, dead-letter counts, and how to read each."
sources: ["https://docs.cloud.google.com/pubsub/docs/monitoring", "https://docs.cloud.google.com/pubsub/docs/ordering", "https://docs.cloud.google.com/monitoring/api/metrics_gcp_p_z"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub backlog and oldest unacked message monitoring

## 1. The metrics (`pubsub.googleapis.com/subscription/...`)
| Metric | Meaning |
|---|---|
| `oldest_unacked_message_age` | seconds since the oldest unacked message was published; **the** SLO metric |
| `num_undelivered_messages` | backlog count |
| `num_unacked_messages_by_region` | backlog per `region` label |
| `expired_ack_deadlines_count` | ack deadline expired while a subscriber held the message (by `delivery_type`) |
| `delivery_latency_health_score` | boolean per `criteria` label (`ack_latency`, `expired_ack_deadlines`, `nack_requests`, `seek_requests`, `utilization`) over a rolling 10-minute window |
| `dead_letter_message_count` | messages published to a dead-letter topic |
| `ack_message_count` / `sent_message_count` | throughput |
Topic-side: `topic/send_request_count` by `response_code` shows publish errors; push subscriptions: `push_request_count` by `response_class`.

## 2. Alert policies
- `oldest_unacked_message_age` > your max processing delay for a sustained period, per subscription.
- `num_undelivered_messages` rising over a sustained period with a flat `ack_message_count`: consumers stalled.
- `dead_letter_message_count` > 0: page someone to inspect the DLQ.
Filter: `resource.type="pubsub_subscription" AND metric.type="pubsub.googleapis.com/subscription/oldest_unacked_message_age"`.

## 3. Diagnosis
- Age grows while the backlog is flat: a message may be stuck being redelivered. Add a dead-letter topic.
- Expired ack deadlines rising: raise `--ack-deadline` (10-600 s) or let client lease management extend it; use client flow control to limit outstanding messages.
- Backlog grows evenly: scale consumers.

## Gotchas
- Alerts on very short windows can flap; use a sustained window.
- Ordering keys: a redelivered message triggers redelivery of later messages for that key, which can delay delivery for other keys too.
- `push_request_count` `response_class` values include `ack`, `deadline_exceeded`, `internal`, `invalid`, `remote_server_4xx`, `remote_server_5xx`, `unreachable`.

## Verify
- [ ] Stopping a consumer in staging trips the age alert within the expected window.

## Checked
Checked 2026-10-24 against the Cloud Monitoring Pub/Sub metrics list (metric names, kinds and labels) and the Pub/Sub ordering documentation (docs.cloud.google.com). Confirmed all metric names and label values used above. Removed unconfirmed thresholds, the gcloud policy command, aligner choice, metric-lag figure and autoscaler advice.
Method: documentation only; no commands were run.
