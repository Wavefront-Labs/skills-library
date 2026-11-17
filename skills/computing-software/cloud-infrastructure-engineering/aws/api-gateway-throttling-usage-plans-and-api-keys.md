---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-throttling-usage-plans-and-api-keys
name: api-gateway-throttling-usage-plans-and-api-keys
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, throttling-limits, usage-plans, burst-limit, api-keys, rate-limiting, http-429]
level: practitioner
status: docs-checked
description: "Set API Gateway throttling at account, stage, method and client level, use usage plans and API keys for quotas, and diagnose 429 Too Many Requests."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-key-source.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-throttling.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway throttling, usage plans and API keys

**Goal:** protect the backend and share capacity fairly between clients, with 429s that are
intentional rather than surprising.

## 1. The layers (most specific wins, all apply)
1. **Account per region**: default 10,000 rps steady, 5,000 burst (token bucket), shared by
   *all* APIs in the account+region (lower in some newer Regions). Raise via Service Quotas; the burst bucket is set by the service team.
2. **Stage / method** throttling: method settings `throttlingRateLimit` and `throttlingBurstLimit`, for all methods or per method.
3. **Usage plan** (REST): per API key rate/burst plus a **quota** per day/week/month, and
   optional per-method overrides.
HTTP APIs: stage and route-level throttling (it cannot exceed the account-level limits); API keys and usage plans are REST API features.
Throttles and quotas are best-effort targets, not guaranteed ceilings.

## 2. Usage plan with keys
```bash
PLAN=$(aws apigateway create-usage-plan --name partner-gold \
  --api-stages apiId=$API,stage=prod \
  --throttle rateLimit=50,burstLimit=100 --quota limit=1000000,period=MONTH --query id --output text)
KEY=$(aws apigateway create-api-key --name acme --enabled --query id --output text)
aws apigateway create-usage-plan-key --usage-plan-id $PLAN --key-id $KEY --key-type API_KEY
aws apigateway get-usage --usage-plan-id $PLAN --start-date 2026-10-01 --end-date 2026-10-16
```
Methods must require an API key; clients send the `x-api-key` header (`apiKeySource=HEADER`). Keys can also come from a
Lambda authorizer (`apiKeySource=AUTHORIZER`, return `usageIdentifierKey` at the root of the authorizer response).

## 3. Reading 429s
- Gateway response `THROTTLED` (429): usage plan, method, stage or account throttling limits exceeded.
- Gateway response `QUOTA_EXCEEDED` (429): the usage plan quota for that key is exhausted.
- Access log field `$context.status` = 429 and `$context.error.responseType` shows `THROTTLED` or `QUOTA_EXCEEDED`; CloudWatch `4XXError` rises.

## Gotchas
- **API keys are identification, not authentication** — keys leak in client apps; always pair
  with an authorizer.
- Throttling and quotas are applied on a best-effort basis; for hard per-tenant limits enforce in the backend too.
- One noisy API can exhaust the account-level bucket for every API in the region; set stage
  limits below the account limit on each API.
- Clients should resubmit 429s in a rate-limited way (exponential backoff with jitter).

## Verify
- [ ] A load test above the configured rate shows 429s at roughly the limit and backend invocations capped.
- [ ] A key over quota gets the `QUOTA_EXCEEDED` 429; `get-usage` shows its count.
- [ ] Account-level quota and current peak rps are recorded with headroom.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot), the current quotas page and the botocore `apigateway` model.
Confirmed: 10,000 RPS and 5,000 burst per account per Region (lower in newer Regions); best-effort throttles; token bucket; `X-API-Key` header and `apiKeySource` HEADER or AUTHORIZER with `usageIdentifierKey`; quota periods DAY, WEEK, MONTH; `THROTTLED` and `QUOTA_EXCEEDED` gateway responses; HTTP APIs have route-level throttling and no API keys; `get-usage` parameters; method settings `throttlingRateLimit` and `throttlingBurstLimit`.
Removed as unconfirmed: the stage-level JSON-patch paths, the literal 429 body messages, the per-node overshoot claim and the SDK retry claim.

Method: documentation only; no commands were run.
