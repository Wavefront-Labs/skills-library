---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pubsub-topics-subscriptions-and-delivery
name: pubsub-topics-subscriptions-and-delivery
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, pubsub, pub-sub, cloud-pubsub, topics, subscriptions, pull-subscription, push-subscription, bigquery-subscription, gcs-subscription, dead-letter-topic, retry-policy, exponential-backoff, ack-deadline, exactly-once-delivery, ordering-keys, message-retention, seek-and-replay, snapshots, schemas, pubsub-lite, flow-control, streaming-pull]
level: practitioner
status: docs-checked
description: "Design Pub/Sub for production: pull vs push vs BigQuery/GCS subscriptions, ack deadlines, dead-letter topics and retry backoff, ordering keys, exactly-once, retention and replay, schemas, IAM."
sources: ["https://docs.cloud.google.com/pubsub/docs/overview", "https://docs.cloud.google.com/pubsub/docs/handling-failures", "https://docs.cloud.google.com/pubsub/docs/ordering", "https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery", "https://github.com/googleapis/googleapis/blob/master/google/pubsub/v1/pubsub.proto", "https://docs.cloud.google.com/sdk/gcloud/reference/pubsub/subscriptions/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub topics, subscriptions and delivery

**Goal:** messages are delivered at least once to every consumer that needs them, poison
messages end in a dead-letter topic instead of a retry storm, and you can replay a week of history after a bad deploy.

## 1. Topology
- One **topic** per event type/domain (`orders.created`), many **subscriptions** (one per consumer system; each gets every message). A subscription is the unit of retention, retry, DLQ and IAM.
- Publishers get `roles/pubsub.publisher` on the topic; consumers `roles/pubsub.subscriber` on *their* subscription (not the topic); the subscription's push/BigQuery writer identity is the Pub/Sub service agent or a chosen SA.
```bash
gcloud pubsub topics create orders.created --message-retention-duration=7d --schema=orders-v1 --message-encoding=json
gcloud pubsub subscriptions create orders-fulfilment --topic=orders.created \
  --ack-deadline=60 --message-retention-duration=7d --retain-acked-messages \
  --dead-letter-topic=orders.created.dlq --max-delivery-attempts=5 \
  --min-retry-delay=10s --max-retry-delay=600s --enable-exactly-once-delivery \
  --expiration-period=never
```
Grant the Pub/Sub service agent (`service-<PROJECT_NUMBER>@gcp-sa-pubsub.iam.gserviceaccount.com`) `pubsub.publisher` on the DLQ topic and `pubsub.subscriber` on the source subscription, or dead-lettering silently does nothing.

## 2. Subscription types
| Type | When | Notes |
|---|---|---|
| **Pull** (streaming pull via client libs) | services/workers, highest throughput | client **flow control** (`max_messages`, `max_bytes`), lease management extends ack deadline automatically |
| **Push** (HTTPS POST) | Cloud Run/Functions, serverless | `--push-endpoint` + `--push-auth-service-account` (OIDC token; optional `--push-auth-token-audience`, and the endpoint must check the token's audience); no client flow control |
| **BigQuery** | land events in a table with no code | `--bigquery-table`, `--use-table-schema`/`--use-topic-schema`, `--write-metadata`; grant the Pub/Sub service agent write access on the table |
| **Cloud Storage** | batch files every N min/MB | `--cloud-storage-bucket`, `--cloud-storage-file-prefix`, `--cloud-storage-max-duration` |

## 3. Delivery semantics
- **At-least-once** always; design idempotent consumers keyed on `message_id` or a business key. `--enable-exactly-once-delivery` (pull subscriptions only, including StreamingPull; not push or export subscriptions) guarantees an acknowledged message is not resent and a message is not resent before its ack deadline expires; copies published twice by a publisher have distinct `message_id`s, so still dedupe.
- **Ack deadline** 10-600 s (API bounds): set it to cover typical processing time; client libraries extend leases automatically, but a crashed consumer holds the message until the deadline expires.
- **Ordering keys**: `--enable-message-ordering` on the subscription and publish with `ordering_key`; order is per key, per region; publish throughput per ordering key is limited to 1 MBps. A redelivery triggers redelivery of all later messages for that key, even acknowledged ones.
- **Retry policy** (`--min-retry-delay` default 10 s, `--max-retry-delay` default 600 s, each 0-600 s; best effort) gives exponential backoff instead of immediate redelivery; **DLQ** after `--max-delivery-attempts` (5-100, default 5). Monitor `subscription/dead_letter_message_count`.

## 4. Replay and retention
- Subscription retention keeps *unacked* messages (default 7 d, 10 min to 31 d); `--retain-acked-messages` keeps acked too so you can **seek**: `gcloud pubsub subscriptions seek orders-fulfilment --time=2026-10-14T08:00:00Z` (re-deliver from then) or `--snapshot=pre-deploy`.
- **Topic retention** (`--message-retention-duration` on the topic, billed to the topic project) lets *new* subscriptions seek back into history — enable on core topics.
- **Snapshots** (`gcloud pubsub snapshots create pre-deploy --subscription=…`) before a risky consumer release; a snapshot expires no later than 7 days after creation.

## 5. Schemas, size, cost
- Topic **schema** (Avro/Protobuf) rejects malformed publishes; revisions allow evolution (`--first-revision-id/--last-revision-id` on the topic).
- Maximum message size is 10 MB; batch publishes with client batch settings.
- Metrics that page: `subscription/oldest_unacked_message_age` (consumer behind), `num_undelivered_messages` (backlog), `push_request_count` by `response_class`.

## Gotchas
- A subscription with no connected subscriber for the expiration TTL (default 31 days, minimum 1 day) is **deleted** with its backlog; `--expiration-period=never` disables expiry.
- Push to Cloud Run needs the push service account to have `roles/run.invoker`.
- Ordering + DLQ: order might not be preserved when messages are written to a dead-letter topic (forwarding is best effort).
- With exactly-once delivery, check the result of the client library's ack-with-response call (for example `ackWithResponse()` in Node.js) to know the ack succeeded.
- Cross-project: publisher in project A, topic in B — IAM on the topic, and VPC-SC perimeters must include both.

## Verify
- [ ] A consumer that always nacks sends the message to the DLQ after 5 attempts; the `delivery_attempt` field counts up.
- [ ] `subscriptions seek --time` re-delivers yesterday's messages to a test subscription.
- [ ] The push endpoint verifies the OIDC token and rejects requests without a valid one.
- [ ] An alert on `oldest_unacked_message_age` fires when the consumer is scaled to zero.

## Checked
Checked 2026-10-24 against the googleapis `google/pubsub/v1/pubsub.proto` (ack deadline 10-600 s, max_delivery_attempts 5-100, retry backoff defaults, retention 10 minutes to 31 days with a 7-day default, 31-day expiration default, snapshot 7-day expiry, 10 MB limit), the gcloud `pubsub subscriptions create` reference, and the exactly-once, ordering and handling-failures documentation (docs.cloud.google.com). Removed the Pub/Sub Lite/Kafka row, pricing minimum, push timeout and status-code behaviour, autoscaler advice and the Cloud Storage flag semantics beyond flag names.
Method: documentation only; no commands were run.
