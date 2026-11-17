---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-event-source-mapping-scaling-and-provisioned-mode
name: lambda-event-source-mapping-scaling-and-provisioned-mode
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, maximum-concurrency, provisioned-mode-esm, event-source-mapping, sqs, kafka, pollers]
level: advanced
status: docs-checked
description: "Control how Lambda event source mappings scale: SQS maximum concurrency, provisioned mode pollers for SQS and Kafka, batch window/size trade-offs, and poller metrics."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-scaling.html", "https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html", "https://docs.aws.amazon.com/lambda/latest/api/API_CreateEventSourceMapping.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event source mapping scaling and provisioned mode

## 1. SQS default scaling
Lambda long-polls the queue and starts with five concurrent invocations. If messages remain, it adds up to 300
more concurrent invocations per minute, to a maximum of 1,250 per mapping. For FIFO queues, concurrency is
capped by the number of active message group IDs (or `MaximumConcurrency`, whichever is lower).

## 2. Maximum concurrency (limit the consumer without throttles)
```bash
aws lambda update-event-source-mapping --uuid <esm-uuid> \
  --scaling-config '{"MaximumConcurrency":50}'
```
Range 2 to 1,000; remove it with `--scaling-config "{}"`. It is a per-mapping setting (two queues on one function
each get their own limit), SQS only, and has no charge. Lambda stops pulling messages at the limit, so they stay
in the queue instead of being received, throttled and returned. Do not set it above the function's reserved
concurrency, and keep reserved concurrency at or above the total `MaximumConcurrency` of all SQS mappings on
the function. It cannot be combined with provisioned mode.

## 3. Provisioned mode
Available for SQS, Amazon MSK and self-managed Kafka mappings. You set a minimum and maximum number of event pollers:
```bash
aws lambda update-event-source-mapping --uuid <esm-uuid> \
  --provisioned-poller-config '{"MinimumPollers":5,"MaximumPollers":100}'
```
Disable with `--provisioned-poller-config '{}'`.
- SQS poller: up to 1 MB/s, 10 concurrent invokes or 10 polling API calls per second. Minimum 2-200 (default 2),
  maximum 2-10,000 (default 200). Provisioned mode scales 3x faster (up to 1,000 concurrency per minute) and
  supports up to 100,000 concurrent invocations.
- Kafka poller: up to 5 MB/s or 5 concurrent invokes. Minimum 1-200 (default 1), maximum 1-2,000 (default 200).
- Costs extra, billed on poller usage. Watch the `ProvisionedPollers` metric. For lowest latency set
  `MaximumBatchingWindowInSeconds` to 0.

## 4. Batching knobs
| Setting | Effect |
|---|---|
| `BatchSize` | SQS standard max 10,000 (default 10), SQS FIFO max 10; Kinesis, DynamoDB, Kafka, MQ and DocumentDB default 100, max 10,000. Payload is capped at 6 MB. |
| `MaximumBatchingWindowInSeconds` | 0-300 seconds. Default 0 for Kinesis, DynamoDB, SQS; 500 ms for MSK, self-managed Kafka, MQ and DocumentDB. Must be at least 1 for streams and SQS when `BatchSize` > 10. |
| `FunctionResponseTypes=ReportBatchItemFailures` | return only the failed item IDs; supported for Kinesis, DynamoDB, MSK, Kafka and SQS |
Larger batches spread the invoke overhead across more records and can raise throughput.

## 5. Monitoring
- Provisioned mode: `ProvisionedPollers` metric.
- Mapping metrics are enabled with `MetricsConfig` (see the event source mapping metrics page for names).
- SQS side: `ApproximateAgeOfOldestMessage`, `ApproximateNumberOfMessagesVisible`.
- Streams: `IteratorAge`.

## Gotchas
- Disabling a mapping (`--no-enabled`) pauses polling and invocation; messages accumulate. Useful as an
  emergency brake for a broken consumer.
- Standard-mode SQS can scale down to as few as 2 concurrent invokes when traffic is low, except when
  `MaximumConcurrency` is set.

## Verify
- [ ] Under load, function `ConcurrentExecutions` plateaus at MaximumConcurrency with zero `Throttles`.
- [ ] Queue age drains within the SLO after a burst; DLQ stays empty.
- [ ] In provisioned mode, `ProvisionedPollers` tracks load between your minimum and maximum.

## Checked
Date 2026-10-23. Lambda Developer Guide SQS scaling and event source mapping pages and the CreateEventSourceMapping API reference. Confirmed:
SQS 5 initial, +300 per minute, 1,250 maximum; MaximumConcurrency 2-1,000 and mutual exclusion with provisioned
mode; poller ranges and per-poller capacity for SQS and Kafka; batch size and window defaults and maxima; the 6 MB
cap; ReportBatchItemFailures sources. Wrong in the old text: "60 per minute" SQS ramp, Kafka and SQS poller
description, FIFO batch size maximum 10 omitted. Removed unconfirmed metric names (EventCount, OffsetLag), the
"6 x timeout" visibility timeout rule and the "batch size change pauses" gotcha.
Method: documentation only; no commands were run.
