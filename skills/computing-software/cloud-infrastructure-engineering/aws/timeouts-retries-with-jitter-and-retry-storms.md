---
id: computing-software.cloud-infrastructure-engineering.aws.timeouts-retries-with-jitter-and-retry-storms
name: timeouts-retries-with-jitter-and-retry-storms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, jitter, retry-storm, exponential-backoff-jitter, timeouts, retry-budget, builders-library]
level: advanced
status: docs-checked
description: "Set timeouts and retries that help availability: timeout choice from latency percentiles, capped backoff with full jitter, SDK retry modes and quota, single-layer retries."
sources: ["https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/", "https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_limit_retries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeouts, retries with jitter, and retry storms

## 1. Timeouts first
- The Builders' Library practice: set a timeout on any remote call, and generally on any call across
  processes, including both a connection timeout and a request timeout. Prefer the timeouts built into
  well-tested clients.
- Too high a timeout wastes the resources held while waiting; too low increases backend traffic and
  latency through extra retries, and a small latency rise can become an outage as all requests retry.
- For calls within an AWS Region, pick an acceptable false-timeout rate (the article's example is 0.1%) and
  use the matching downstream latency percentile (p99.9 in that example).
- That approach fails over the internet (add reasonable worst-case network latency) and for services
  with tight latency bounds where p99.9 is close to p50 (add padding).
- Check what the timer covers: the article's example had a ~20 ms timeout that included establishing a
  new secure connection, causing timeouts after deployments; the fix was to open connections at process
  start before taking traffic. Some implementations do not cover DNS or TLS handshakes.

## 2. Retries: when
- Retries are "selfish": they spend more server time for a better chance of success. Under overload they
  can make things worse and delay recovery.
- Only retry safely: APIs with side effects are not safe to retry unless idempotent. Read-only APIs
  are typically idempotent; EC2 `RunInstances` offers a token for idempotency.
- Client (4xx) errors should generally not be retried with the same request and server errors may succeed,
  but eventual consistency blurs the line: a client error can turn into success as state propagates.

## 3. Backoff with full jitter
The SDK reference describes the formula as `delay = random(0, 1) x min(20,000 ms, base_delay x 2^retry)`,
with retry starting at 0. Base delay is 50 ms for transient errors and 1,000 ms for throttling errors.
```python
import random, time
def call_with_retries(fn, max_attempts=3, base=0.05, cap=20.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            time.sleep(random.uniform(0, min(cap, base * 2 ** attempt)))   # full jitter
```
Without jitter, clients that failed together retry together. Backoff alone does not help much when
failures come from overload or contention because of that correlation. Limit retry count too:
capped backoff leaves all clients retrying constantly at the cap.

## 4. Retry storms and amplification
A five-deep stack with three retries at each layer raises load on the database 243x (retries multiply),
per the article. Retrying only at the top wastes work from earlier calls. For low-cost control-plane and
data-plane operations the stated best practice is to retry at a single point in the stack. The
Well-Architected page (REL05-BP03) lists retrying at multiple layers as an anti-pattern.
- **Token bucket:** the article says limiting retries locally with a token bucket lets calls retry while
  tokens last and then retry at a fixed rate; it notes circuit breakers add modal behaviour that is hard to
  test and can add recovery time.
- Set a maximum number of retries or elapsed time to avoid backlogs and metastable failures.
- Do not retry non-retryable errors such as permission or configuration errors, monitor and alert on
  repeated failures, and test retry scenarios rather than assuming the SDK covers them.

## 5. AWS SDK settings
From the SDK reference page (which says the behaviour it documents needs `AWS_NEW_RETRIES_2026=true`
until it becomes the default; without it the SDK uses pre-2026 behaviour):
- Modes: `standard` (default, recommended), `adaptive`, `legacy`.
- `standard` has a retry quota: a token bucket of 500 tokens; a transient retry costs 14, a throttling
  retry costs 5; a success restores 1 token, or restores the last retry's cost after a retry. When
  empty, the SDK returns the error without retrying.
- `adaptive` adds a client-side rate limiter per client instance and can delay the initial request. Use
  it for a client targeting a single resource with frequent throttling; avoid it for multi-resource or
  multi-tenant clients or when you need predictable initial-request latency.
- `max_attempts` counts the initial request: default 3 (one initial request plus up to two retries),
  1 disables retries. DynamoDB and DynamoDB Streams clients default to 4 with a 25 ms transient base delay.
- Settings: `AWS_RETRY_MODE`/`retry_mode`, `AWS_MAX_ATTEMPTS`/`max_attempts`. Precedence: client
  configuration in code, then environment variable, then shared config file, then default.
```ini
# ~/.aws/config
[default]
retry_mode = standard
max_attempts = 3
```
- If the response carries `x-amz-retry-after`, the SDK uses it, clamped between the computed backoff and
  that plus 5,000 ms, without jitter.
- SQS `ReceiveMessage` and similar long-polling operations still back off when the quota is empty.
- Language-specific retry APIs vary; see each SDK's guide.

## Verify
- [ ] Every outbound client has explicit connect and request timeouts, chosen from downstream latency percentiles.
- [ ] Retries use capped exponential backoff with jitter and a maximum count, at a single layer.
- [ ] Retried operations are idempotent; retry scenarios have been tested.

## Checked
Checked 2026-11-08 against the Builders' Library article, the AWS SDKs and Tools "Retry behavior" page and
Well-Architected REL05-BP03. Removed: the API Gateway 29 s / Lambda 25 s budget example, the boto3 and Java
client-option names, Lambda, Step Functions `JitterStrategy` and SQS visibility-timeout notes, and the FIS
load-test item, none of which those pages state.
Method: docs-only read of cited pages, 2026-11-08
