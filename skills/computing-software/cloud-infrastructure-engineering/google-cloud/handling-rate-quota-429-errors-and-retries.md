---
id: computing-software.cloud-infrastructure-engineering.google-cloud.handling-rate-quota-429-errors-and-retries
name: handling-rate-quota-429-errors-and-retries
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, quotas, rate-quota-429, quota-exceeded-errors, resource-exhausted, exponential-backoff, rate-limit-exceeded]
level: practitioner
status: docs-checked
description: "Diagnose GCP quota errors (429, 403 QUOTA_EXCEEDED, ResourceExhausted), set the quota project, retry only idempotent calls with exponential backoff, and raise quota."
sources: ["https://docs.cloud.google.com/docs/quotas/troubleshoot", "https://docs.cloud.google.com/storage/docs/retry-strategy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling rate-quota 429 errors and retries

## Identify which limit
Per the "Troubleshoot quota errors" page, the error depends on how you called the service:
| Access path | Error when a quota value is exceeded |
|---|---|
| HTTP/REST request | HTTP `429 TOO MANY REQUESTS` |
| Compute Engine (API, REST or gRPC) | typically `403 QUOTA_EXCEEDED`; for a rate quota `403 RATE_LIMIT_EXCEEDED` |
| gRPC | a `ResourceExhausted` error (appearance depends on the service) |
| gcloud CLI | quota-exceeded message and exit code 1 |

Rate quotas reset after a service-specific interval, so waiting or backing off helps; an
allocation-style quota (a fixed maximum) needs a quota increase, and retrying does not help.
During a quota rollout the audit-log `QUOTA_EXCEEDED` status can carry a `futureLimit`; the
cited values are correct even if the console differs.

## Quota project
If the quota (billing) project is not set, calls fail with errors such as "User credentials not
supported by this API", "API not enabled in the project" or "No quota project set". Fix it with
`--billing-project` on a gcloud command or `gcloud config set billing/quota_project <PROJECT_ID>`.

## Retry correctly
- Cloud Storage's retry guidance treats `408`, `429` and `5xx` as retryable and says to consider idempotency first: retrying non-idempotent requests can cause races and conflicts. Use preconditions or ETags where the API offers them.
- Use exponential backoff. Cloud Storage client defaults in its docs start at a 1 second delay with a multiplier of 2; the gcloud CLI uses truncated binary exponential backoff. Add jitter and a maximum delay of your own choosing.
- Do not stack your own retry loop on top of a client library that already retries; configure the library's retry policy instead.

## Reduce calls
- Batch requests where the API supports it, cache `get`/`list` results, and spread scripts over time.

## Raise
```bash
gcloud alpha services quota list --service=compute.googleapis.com --consumer=projects/<PROJECT_ID>
```
Request more quota through the Quotas and System Limits page in the console (the troubleshoot page links to "request a quota adjustment").

## Verify
- [ ] Load test shows retries succeed without amplified errors; no permanent 429s in logs.

## Checked
2026-10-31. Confirmed against "Troubleshoot quota errors" (status codes, Compute 403 codes, ResourceExhausted, gcloud exit code 1, quota project errors and `--billing-project`, `billing/quota_project`, futureLimit, quota adjustment) and the Cloud Storage retry strategy page (408/429/5xx retryable, idempotency, 1 second initial delay and multiplier 2 in client defaults, gcloud truncated binary exponential backoff). Removed: ErrorInfo field names, the 32-64 s cap and jitter formula, GCS per-object write rate, stockout/ZONE_RESOURCE_POOL_EXHAUSTED rows, `requestId`, `QuotaPreference` and the net_usage metric name (not in fetched pages).
Method: documentation only; no commands were run.
