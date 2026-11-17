---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-recursive-loop-detection
name: lambda-recursive-loop-detection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, recursive-loop-detection, recursion-prevention, s3-lambda-loop, sqs, sns, cost-runaway]
level: practitioner
status: docs-checked
description: "Prevent and detect Lambda recursive loops: how loop detection works for SQS, SNS, S3, EventBridge and Lambda, the RecursiveLoop setting, design patterns to avoid loops, and alarms."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda recursive loop detection and prevention
**The incident:** a function writes to the same bucket/queue/topic that triggers it; it
invokes itself millions of times and the bill arrives before anyone notices.

## 1. What Lambda does automatically
Detection uses X-Ray tracing headers carried in event metadata (X-Ray active tracing is not required, there is no
charge, and it is on by default). The count of invocations of the function in one chain of requests travels with
the event. When the same function has been invoked about **16 times** in one chain, Lambda stops the next
invocation. It detects loops involving **SQS, S3, SNS, EventBridge custom event buses and Lambda-to-Lambda calls**
(sync or async), but only if the function uses a minimum AWS SDK version (for example boto3 1.24.46 or later,
JavaScript SDK v3 3.105.0 or later, Java 17 SDK 2.20.81 or later; see the page for the full table).
- If the function has an on-failure destination or async dead-letter queue, the stopped event is also sent there.
  Do not point those at a resource that also triggers the function.
- For an SQS source, the mapping receives a `RecursiveInvocationException`; the message is retried until the
  queue's `maxReceiveCount` is exceeded and then goes to the DLQ configured on the **source queue** (not on the function).
- You are notified by the Health Dashboard, an email (at most one per function per 24 hours, up to 3.5 hours
  late) and the `RecursiveInvocationsDropped` CloudWatch metric.
```bash
aws lambda put-function-recursion-config --function-name thumbnailer --recursive-loop Terminate   # default
aws lambda put-function-recursion-config --function-name thumbnailer --recursive-loop Allow
```
Set `Allow` only for intentional, bounded recursion. `RecursiveInvocationsDropped` is not emitted when `Allow` is set.

## 2. Design rules
- **Different input and output locations**: trigger on an `uploads/` bucket, write to a `thumbnails/` bucket (or
  a prefix excluded by the notification filter).
- Do not use the same variable value for a function's event source and its target.
- SQS consumers: configure the DLQ on the source queue rather than re-sending to the source queue.
- Set **reserved concurrency** on risky functions to cap the blast radius.

## 3. Alarms
- `RecursiveInvocationsDropped` greater than 0 (per function).
- CloudWatch alarms on concurrency and invocations, a billing alarm or AWS Cost Anomaly Detection (the page
  recommends these because detection does not cover every service).

## 4. Stopping an active loop
Reduce the function's concurrency to zero (the console Throttle button sets reserved concurrency to 0), remove or
disable the trigger or event source mapping (`aws lambda update-event-source-mapping --uuid <UUID> --no-enabled`),
then fix the code that writes back to the trigger resource and restore concurrency.

## Gotchas
- Loops that involve other services (for example DynamoDB) are not detected.
- Loops through S3 still incur S3 request charges up to the detection point.

## Verify
- [ ] The console Concurrency and recursion detection tab shows Terminate on all functions not intentionally recursive.
- [ ] Notification filters prevent the function's own outputs from triggering it.
- [ ] A `RecursiveInvocationsDropped` alarm and reserved concurrency are in place for S3/SQS-triggered writers.

## Checked
Date 2026-10-23. Lambda Developer Guide, recursive loop detection page (current release). Confirmed: about 16 invocations,
X-Ray header mechanism without active tracing, Terminate and Allow with the CLI commands, metric name, notification
timings, minimum SDK versions, DLQ placement guidance, supported services. Wrong in the old text: the supported
list omitted EventBridge custom event buses, and the claim that SQS events go to the function DLQ (documented:
the source queue's DLQ via maxReceiveCount). Removed the unconfirmed get-function-recursion-config command and the object-metadata code hint.
Method: documentation only; no commands were run.
