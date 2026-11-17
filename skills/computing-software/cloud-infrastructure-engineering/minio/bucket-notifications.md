---
id: computing-software.cloud-infrastructure-engineering.minio.bucket-notifications
name: bucket-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, bucket-notifications, mc-event-add, notify-webhook, sqs-arn, sync-events, queue-limit, event-targets]
level: practitioner
status: docs-checked
description: "Send MinIO bucket events to webhook, Kafka and other targets using notify_webhook config, the SQS ARN and mc event add, plus sync versus async delivery and queue limits."
sources: ["https://github.com/minio/docs/blob/main/source/administration/monitoring/bucket-notifications.rst", "https://github.com/minio/docs/blob/main/source/administration/monitoring/publish-events-to-webhook.rst", "https://github.com/minio/docs/blob/main/source/administration/monitoring/publish-events-to-kafka.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO bucket notifications

MinIO publishes S3-style bucket and object events to external services. Targets: AMQP (RabbitMQ), MQTT, NATS, NSQ, Elasticsearch, Kafka, MySQL, PostgreSQL, Redis and webhook. Event names follow Amazon S3 notifications, e.g. `s3:ObjectCreated:Put`, `s3:ObjectCreated:CompleteMultipartUpload`, `s3:ObjectRemoved:Delete`, `s3:ObjectRemoved:DeleteMarkerCreated`, `s3:ObjectAccessed:Get`, and wildcards `s3:ObjectCreated:*`, `s3:ObjectAccessed:*`, `s3:ObjectRemoved:*`.

## Webhook example
Required: `MINIO_NOTIFY_WEBHOOK_ENABLE` and `MINIO_NOTIFY_WEBHOOK_ENDPOINT` (each suffixed `_<IDENTIFIER>`); optional `..._AUTH_TOKEN`, `..._QUEUE_DIR`, `..._QUEUE_LIMIT`, `..._CLIENT_CERT`, `..._CLIENT_KEY`. Or via config (`endpoint` is the only required key):
```
mc admin config set ALIAS/ notify_webhook:PRIMARY endpoint="https://webhook.example.com"
mc admin service restart ALIAS
```
A reused identifier overrides the existing endpoint; list them with `mc admin config get ALIAS/ notify_webhook`. On startup MinIO prints a line such as `SQS ARNs: arn:minio:sqs::primary:webhook`. Use that ARN to bind events:
```
mc event add ALIAS/BUCKET arn:minio:sqs::primary:webhook --event s3:ObjectCreated:Put
mc event ls ALIAS/BUCKET arn:minio:sqs::primary:webhook
```
Test by uploading with `mc cp`. Kafka follows the same pattern with `MINIO_NOTIFY_KAFKA_ENABLE` and `MINIO_NOTIFY_KAFKA_BROKERS` required, and optional topic, SASL, TLS, queue and version settings.

## Async vs sync (since RELEASE.2023-06-23T20-26-00Z)
- Asynchronous (default): fire and continue; faster, but events may be lost if the remote fails in transit.
- Synchronous: wait for the remote to confirm; safer delivery but slower and the queue can fill. Enable for all targets with `MINIO_API_SYNC_EVENTS=on` or config `api.sync_events` set to `on`, then restart.

## Queues
Each remote has a queue of pending events, default limit `100000`, adjustable by the target's `QUEUE_LIMIT` setting. Async delivery allows at most `50000` concurrent send calls.

## Checked

2026-11-03. Confirmed against the MinIO docs source: the bucket notifications page: webhook and Kafka variables, config keys, event names, ARN binding, async and sync behaviour, queue limit. Removed or fixed: nothing.

Method: documentation only; no commands were run.
