---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-timeouts-oom-and-throttling-troubleshooting
name: lambda-timeouts-oom-and-throttling-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, lambda-timeout, lambda-throttling, out-of-memory, report-line, troubleshooting, toomanyrequestsexception]
level: practitioner
status: docs-checked
description: "Diagnose Lambda failures from the REPORT line and metrics: timeouts, memory exhaustion, 429 throttles, with the quota facts that explain each and the fix levers."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html", "https://docs.aws.amazon.com/lambda/latest/dg/invocation-sync.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda timeouts, OOM and throttling

## 1. Read the REPORT line
Every invocation ends with a REPORT line carrying `Duration`, `Billed Duration`, `Memory Size` and `Max Memory
Used` (retrieve the tail of the log with `aws lambda invoke --log-type Tail`, see the invocation page):
```
REPORT RequestId: 57f231fb-... Duration: 79.67 ms Billed Duration: 80 ms Memory Size: 128 MB Max Memory Used: 73 MB
```
Compare `Max Memory Used` to `Memory Size`, and `Duration` to the configured timeout.

## 2. Timeouts
The function timeout defaults to 3 seconds and can be raised to 900 seconds (15 minutes). Functions behind
event source mappings for MSK, self-managed Kafka, DocumentDB and Amazon MQ support at most 14 minutes.
Symptom: Duration equals the timeout. Levers:
- **Downstream call hanging**: set client timeouts shorter than the function timeout and log before and after
  external calls.
- **VPC function without egress**: calls to AWS APIs or the internet hang until timeout when there is no NAT
  or endpoint. Add VPC endpoints or NAT.
- **Cold start plus heavy init**: initialization work counts toward the first invoke; move work out of init
  or raise memory (CPU scales with memory).
- Extensions share CPU and extend the invoke phase: the function duration includes the time until all extensions
  call `Next`; check the `PostRuntimeExtensionsDuration` metric.
- Raising the timeout is valid for batch work, but check every service in front of the function for its own
  integration timeout.

## 3. Memory exhaustion
Symptom: `Max Memory Used` reaches `Memory Size`. Levers: raise memory (also raises CPU; range 128 to 10,240 MB),
stream large payloads rather than loading them, check for leaks in values kept across warm invocations. `/tmp`
is separate: ephemeral storage can be configured from 512 MB to 10,240 MB.

## 4. Throttling (429)
Metrics: `Throttles` and `ConcurrentExecutions` (per function and account). Reasons:
- The account concurrency limit (default 1,000 per Region) is reached.
- The function's **reserved concurrency** is reached, or set to 0 (which intentionally throttles it).
- The scaling rate: each function can add 1,000 execution environment instances every 10 seconds.
- Requests per second above 10x the concurrency quota.
Fixes: request a quota increase; reserve concurrency for critical functions so others cannot starve them;
provisioned concurrency for predictable bursts; smooth producers. For SQS consumers limit consumption with
`MaximumConcurrency` on the mapping rather than reserved concurrency (see the concurrency skills).

## Verify
- [ ] Alarms on `Errors`, `Throttles` and duration near the timeout exist per critical function.
- [ ] REPORT lines show `Max Memory Used` comfortably below `Memory Size` at peak.
- [ ] SDK client timeouts are shorter than the function timeout (code review).

## Checked
Date 2026-10-23. Lambda Developer Guide quotas, concurrency, reserved concurrency, synchronous invocation and extensions API pages. Confirmed:
timeout default 3 s (API reference) and 900 s maximum, 14 minute cap for MSK, Kafka, DocumentDB and MQ mappings,
memory range, `/tmp` 512 to 10,240 MB, REPORT field names from the documented sample, throttling causes, 1,000 per
10 s scaling rate, 10x RPS cap, reserved concurrency 0, `PostRuntimeExtensionsDuration`. Removed unconfirmed claims:
the Logs Insights query, `Status: timeout` and `Init Duration` REPORT fields, the 10 s init cap, Node.js event loop
and boto3 timeout advice, `Runtime.OutOfMemory` strings, the API Gateway 29 s figure and 502 response format, and the
"async retried up to 6 hours" claim.
Method: documentation only; no commands were run.
