---
id: computing-software.database-administration.cockroachdb.changefeed-sinks
name: changefeed-sinks
category: computing-software
field: database-administration
product: cockroachdb
tags: [changefeed-sinks, kafka-sink, sink-uri, cloud-storage-sink, pubsub]
level: practitioner
status: docs-checked
description: "Configure CockroachDB changefeed sink URIs for Kafka (TLS, SASL, OAUTHBEARER, MSK), Google Pub/Sub and cloud storage, plus topic naming and kafka_sink_config."
sources:
  - https://www.cockroachlabs.com/docs/stable/changefeed-sinks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: point a changefeed at the right sink with correct authentication.

Sink URI shape: `scheme://host:port?query_parameters`. Schemes: `kafka`, `gcpubsub`, cloud storage (for example `s3`), and webhook sinks.

Kafka parameters: `topic_name`, `topic_prefix` (so `topic_prefix=bar_` on table `foo` emits topic `bar_foo`), `tls_enabled` (default `false`), `ca_cert` (base64, create with `base64 -w 0 ca.cert`), `client_cert` and `client_key` (base64 PEM), `sasl_enabled` (requires `tls_enabled=true`), `sasl_mechanism` (`SCRAM-SHA-256`, `SCRAM-SHA-512`, `PLAIN`, `OAUTHBEARER`, `AWS_MSK_IAM` for MSK), `sasl_user`, `sasl_password`, and for OAuth `sasl_client_id`, `sasl_client_secret` (base64), `sasl_token_url` (URL-encoded), `sasl_scopes`, `sasl_grant_type`. `insecure_tls_skip_verify` disables certificate verification and is a warning-flagged setting.
Example from the page:
```
kafka://broker.address.com:9092?topic_prefix=bar_&tls_enabled=true&ca_cert=<base64>&sasl_enabled=true&sasl_user={user}&sasl_password={password}
```
Amazon MSK uses the `kafka://` scheme, e.g. `kafka://{cluster_endpoint}/?tls_enabled=true&sasl_enabled=true&sasl_mechanism=SCRAM-SHA-512&sasl_user={user}&sasl_password={password}`.

Topic naming: automatic topic creation needs Kafka's `auto.create.topics.enable=true`. Legal characters are letters, numbers and `[._-]`; avoid mixing `.` and `_` because they can collide in Kafka internals.

Tuning: cluster setting `changefeed.sink_io_workers` sets concurrent Kafka request workers (applies to Kafka sinks created in v24.2.1+, or with `changefeed.new_kafka_sink.enabled` on earlier patch lines). `kafka_sink_config` JSON controls `ClientID`, `CompressionLevel`, and batching via `Flush.MaxMessages` and `Flush.Frequency` (`Flush.Bytes` and `Flush.Messages` exist only as legacy backups of `MaxBytes` and `MaxMessages`). A high `Flush.Frequency` delays delivery on low-traffic changefeeds, and large batches may be rejected by Kafka unless it accepts a high `max.message.bytes`.

Pub/Sub: `gcpubsub://{project name}?region={region}&topic_name={topic name}&AUTH=specified&CREDENTIALS={base64-encoded credentials}`. Cloud storage: `s3://{BUCKET NAME}/{PATH}?AWS_ACCESS_KEY_ID=...&AWS_SECRET_ACCESS_KEY=...`.

Verify: create the changefeed with `INTO` the URI, then check `SHOW CHANGEFEED JOBS;` for status `running` and that messages arrive.

## Checked
2026-11-03. Confirmed on the changefeed sinks page: Kafka query parameters and defaults (`topic_prefix`, `tls_enabled`, `ca_cert` via `base64 -w 0`, `sasl_enabled` needs TLS, `sasl_mechanism` values, OAuth parameters, `insecure_tls_skip_verify` warning), MSK URIs, topic naming rules, `auto.create.topics.enable`, `changefeed.sink_io_workers` version gate, and `kafka_sink_config` fields. Corrected: the Flush field list and latency wording.
Method: documentation only; no commands were run.
