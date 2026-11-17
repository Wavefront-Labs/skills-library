---
id: computing-software.cloud-infrastructure-engineering.aws.aws-api-throttling-and-sdk-retry-configuration
name: aws-api-throttling-and-sdk-retry-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-throttling, request-rate-limit, retry-mode, exponential-backoff, sdk]
level: practitioner
status: docs-checked
description: "Tune AWS SDK retry mode, max attempts and backoff for throttling errors (ThrottlingException, RequestLimitExceeded), and reduce call volume."
sources: ["https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS API throttling and retries

**Goal:** stop throttling errors from failing automation by choosing the right SDK retry mode and cutting call volume.

## Opt in first
Per the SDK Reference page, the retry behaviour it describes requires opting in until it becomes the default:
set `AWS_NEW_RETRIES_2026=true`. Without it, your SDK uses pre-2026 retry behaviour, which differs in backoff timing,
retry quota costs and service-specific defaults. Support varies by SDK (the page has a per-SDK table; AWS CLI v2
is listed as "See tracking issue").

## Retry settings
| Setting | Environment variable | Config file key (`~/.aws/config`) | Default per page |
|---|---|---|---|
| Retry mode | `AWS_RETRY_MODE` | `retry_mode` | `standard` |
| Max attempts (includes the initial request) | `AWS_MAX_ATTEMPTS` | `max_attempts` | 3 |

- 3 max attempts means one initial request and up to two retries; 1 disables retries. DynamoDB and DynamoDB Streams
  clients default to 4.
- Precedence, highest first: explicit client configuration in code, environment variable, shared config file, SDK default.

## Modes
- `standard`: the default; exponential backoff with jitter, plus a retry quota. Use it unless you have a specific reason.
- `adaptive`: standard plus a client-side rate limiter per SDK client instance; it can delay the initial request.
  Suited to a client targeting a single resource that is throttled often; not for a client that serves multiple resources
  or tenants, nor when you need predictable initial-request latency.
- `legacy`: pre-standard per-SDK behaviour, kept for backward compatibility; the page says to switch to standard.

## How the SDK backs off (per the page)
- Errors are classified as transient, throttling or non-retryable. Throttling codes include `Throttling`,
  `ThrottlingException`, `TooManyRequestsException`, `RequestLimitExceeded`, `EC2ThrottledException` and `SlowDown`.
  `AccessDeniedException` and `ValidationException` are not retried.
- Delay = `random(0,1) x min(20,000 ms, base_delay x 2^retry)`; base delay 50 ms for transient errors, 1,000 ms for throttling.
  DynamoDB uses 25 ms for transient errors.
- Retry quota: 500-token bucket; a transient retry costs 14 tokens, a throttling retry 5; when it is empty the SDK returns
  the error without retrying.
- If a service sends an `x-amz-retry-after` header (milliseconds), the SDK uses it, clamped between the computed backoff and
  the computed backoff plus 5,000 ms.
- Long-polling operations (`SQS.ReceiveMessage`, `SFN.GetActivityTask`, `SWF.PollForActivityTask`,
  `SWF.PollForDecisionTask`) still back off when the quota is empty.

## Reduce the calls
1. Paginate and filter server-side where the API supports it.
2. Cache results that change slowly; prefer event-driven updates over polling.
3. Stagger scheduled jobs.
4. Use one caller per workflow; clients that all poll the same API compete for the same limits.

## Verify
- [ ] `AWS_NEW_RETRIES_2026=true`, `AWS_RETRY_MODE` and `AWS_MAX_ATTEMPTS` are set where intended, and a client-level
  setting is not silently overriding them (precedence above).
- [ ] Your SDK is listed as supported in the page's table; if it says "See tracking issue", read that issue.

## Checked
Date: 2026-11-07. Read in full: SDK Reference "Retry behavior" page (retry modes, settings table, precedence, error
classification, backoff formula, x-amz-retry-after, retry quota, DynamoDB and long-polling sections, SDK support table).
Removed because that page does not state them and no other page was read: per-service token-bucket claim, the statement
that these limits are not raised through Service Quotas, `BatchGetItem`/`--filters`/`--query` advice, the CloudTrail
`errorCode` query and the `ThrottledRequests` metric, and the earlier "max_attempts = 8" example.
Method: documentation only; no commands were run.
