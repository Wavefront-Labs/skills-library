---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-extended-client-large-messages
name: sqs-extended-client-large-messages
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, extended-client, large-messages, claim-check, sqs-s3, message-size-limit, 256kb, 1mb-messages, sns-extended-client, payload-offloading, s3-lifecycle, lambda-large-payload, messaging]
level: practitioner
status: docs-checked
description: "Send payloads beyond the SQS message size limit with the Extended Client Library (claim-check via S3): configure the bucket, thresholds, cleanup, consumer side, and Lambda/SNS interop."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-s3-messages.html", "https://github.com/awslabs/amazon-sqs-java-extended-client-lib", "https://github.com/awslabs/amazon-sqs-python-extended-client-lib", "https://docs.aws.amazon.com/sns/latest/dg/large-message-payloads.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Large SQS messages with the Extended Client (claim check)

**Goal:** publish a 5 MB document through SQS/SNS without the producer or consumer caring
that the body actually lives in S3, and without orphaned objects filling the bucket forever.

## 1. The limit and the pattern
The SQS maximum message size is 1,048,576 bytes (1 MiB; the queue attribute `MaximumMessageSize` can be
set from 1,024 bytes up to that, default 1 MiB). Above that, use the **claim-check** pattern: the producer
writes the payload to S3 and sends a small reference; the consumer fetches it. AWS publishes the Amazon SQS
Extended Client Library for Java and for Python for this (maximum payload 2 GB); the library works only with
synchronous clients. It can store payloads always in S3 or only when a message exceeds 256 KB.

## 2. Producer
```python
from sqs_extended_client import SQSExtendedClient   # pip install amazon-sqs-extended-client
import boto3
sqs = boto3.client("sqs")
sqs.large_payload_support = "my-sqs-payloads"       # bucket
sqs.always_through_s3 = False                       # only offload large messages
sqs.delete_payload_from_s3 = True                   # delete_message also deletes the S3 object
sqs.use_legacy_attribute = False                    # "ExtendedPayloadSize" (current) vs "SQSLargePayloadSize" (legacy)
sqs.send_message(QueueUrl=q, MessageBody=big_json)
```
The S3 bucket must exist first (the Python README creates it with `client.s3_client.create_bucket(...)`).
The library adds a reserved message attribute, `ExtendedPayloadSize` (legacy name `SQSLargePayloadSize`); a
large-payload message may carry at most 10 other message attributes. For the Java client's configuration
methods and defaults, see the repository README linked in `sources`.

## 3. Consumer
Use the same library on the consumer: `receive_message` fetches the object and returns the full body. Set
`delete_payload_from_s3 = True` so that `delete_message` also removes the payload from S3. Consumers that do
not use the library see only the reference message, so they must fetch the S3 object themselves and
clean it up.

## 4. Bucket hygiene
- Objects whose message was never deleted (DLQ'd, expired, consumer crashed) are orphaned.
  Add a lifecycle rule: expire after queue `MessageRetentionPeriod` + DLQ retention (e.g. 30 days).
  Never shorter than retention or a delayed consumer finds a 404.
- Block public access and limit the bucket policy to the producer and consumer roles.

## 5. SNS fan-out
SNS topics now accept payloads up to 1 MiB natively when the topic attribute `MaximumMessageSize` is raised
(1,024 to 1,048,576 bytes; default 262,144), limited to Firehose, SQS and Lambda subscribers and 100
subscriptions; for SQS subscribers the topic's `MaximumMessageSize` is the effective limit, not the queue's.
Above 1 MiB, AWS publishes SNS Extended Client Libraries for Java and Python (up to 2 GB, Standard and FIFO
topics). How an SNS-extended pointer interacts with the SQS Extended Client on a subscription (raw delivery
or envelope) is not documented on the pages checked: test it before relying on it.

## Gotchas
- The library is for synchronous clients only; do not use it with async SDK clients.
- Services that read the queue without the library (for example a Lambda event source mapping) get the
  reference message, not the payload.
- Alternative for Lambda-only consumers: put the object in S3 first and send only the key, and skip the library.

## Verify
- [ ] Sending a 2 MB body succeeds; `aws sqs receive-message` without the library shows a small reference body and an `ExtendedPayloadSize` attribute.
- [ ] Consumer with the library receives the full body and after `delete_message` the S3 object is gone.
- [ ] A 100 KB body (below the 256 KB offload threshold) is sent inline: no S3 object is created.
- [ ] Bucket lifecycle rule exists with expiry ≥ queue retention.

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide, SNS Developer Guide and the amazon-sqs-python-extended-client-lib README.
Confirmed: SQS max message size 1 MiB (the old 256 KB limit was stale); Extended Client for Java and Python, 2 GB payload, synchronous clients only; pip package `amazon-sqs-extended-client`, import `sqs_extended_client`; Python attributes `large_payload_support`, `always_through_s3`, `delete_payload_from_s3`, `use_legacy_attribute`; attribute names `ExtendedPayloadSize` and `SQSLargePayloadSize`; 10-attribute limit; SNS `MaximumMessageSize` 1,024 to 1,048,576 and 262,144 default, supported endpoints, SNS extended libraries up to 2 GB for Standard and FIFO.
Removed (not confirmed in the docs): pointer wire format, Java config method names, receipt-handle rewriting, cleanup defaults, FIFO dedup note, raw-delivery requirement, S3 permission and ownership advice, Step Functions behaviour. Note: the `message_size_threshold` attribute is not in the README (it exposes a module default of 262144), so the line was removed.
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html ; https://github.com/awslabs/amazon-sqs-python-extended-client-lib ; https://github.com/awslabs/amazon-sqs-java-extended-client-lib ; https://docs.aws.amazon.com/sns/latest/dg/large-message-payloads.html

Method: documentation only; no commands were run.
