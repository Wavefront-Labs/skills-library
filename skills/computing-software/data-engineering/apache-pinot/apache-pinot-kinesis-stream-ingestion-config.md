---
id: computing-software.data-engineering.apache-pinot.apache-pinot-kinesis-stream-ingestion-config
name: apache-pinot-kinesis-stream-ingestion-config
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, kinesis, stream-ingestion, shard, sharditeratortype, maxrecordstofetch, requests-per-second-limit, stream-kinesis-topic-name, aws-credentials]
level: practitioner
status: docs-checked
description: "Kinesis realtime ingestion: streamType and region keys, shardIteratorType (LATEST default), fetch limits, credential chain preference, resharding detection and flush limits."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/stream-ingestion/amazon-kinesis.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinesis stream ingestion config

Kinesis uses the same `streamConfigs` map (inside `tableIndexConfig` of a REALTIME table) with `streamType` set to `kinesis`:
```
"streamType": "kinesis",
"stream.kinesis.topic.name": "<your kinesis stream name>",
"region": "<your region>",
"shardIteratorType": "AFTER_SEQUENCE_NUMBER",
"stream.kinesis.fetch.timeout.millis": "30000",
"stream.kinesis.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
"stream.kinesis.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory",
"realtime.segment.flush.threshold.rows": "1000000",
"realtime.segment.flush.threshold.time": "6h"
```

Details:
- `shardIteratorType` is the AWS shard iterator type Pinot passes through to the Kinesis client when opening a shard iterator. Default `LATEST`.
- `maxRecordsToFetch`: maximum records per getRecords call, 1 to 10,000 (the Kinesis API limit); default is the max, 10000. Lower it only under memory constraints.
- `requests_per_second_limit`: maximum Kinesis read requests per second per shard, applied to both getRecords and getShardIterator; fractional values such as 0.25 are accepted; default **1.0**. The docs suggest dividing Kinesis's 5 getRecords requests per second per shard across Pinot replicas, Pinot tables and other consumers. On ProvisionedThroughputExceededException Pinot backs off and retries until the fetch timeout.
- Authentication uses the AWS DefaultCredentialsProviderChain: environment variables (recommended), Java system properties, web identity token, the credentials profile file, the EC2 container service, then the instance profile. Pinot needs read-level permissions on the stream. Setting `accessKey` and `secretKey` in the table config is not recommended outside non-production proofs of concept.
- Resharding is detected by the hourly periodic task RealtimeValidationManager, and only after the parent shards are fully ingested. Until then the ideal state can show all segments ONLINE. The task can be invoked manually for faster pickup.
- Limitations: the numeric part of `shardId-000000000001` becomes the integer partitionId (overflow beyond Integer.MAX_VALUE), and segment size based completion thresholds do not work because partition 0 is assumed to exist.

## Checked

Confirmed against the Pinot docs page "Ingest streaming data from Amazon Kinesis": config keys and example, shardIteratorType default, maxRecordsToFetch range and default, requests_per_second_limit default and semantics, credential chain, resharding and limitations. Corrected the validation task name to RealtimeValidationManager and removed the unsourced TRIM_HORIZON advice.

Method: docs-only read of cited pages, 2026-11-08
