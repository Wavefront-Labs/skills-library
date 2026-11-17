---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-functions-memory-concurrency-and-instances
name: cloud-run-functions-memory-concurrency-and-instances
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run-functions, function-min-instances, function-concurrency, cold-starts, max-instances, function-cpu]
level: practitioner
status: docs-checked
description: "Tune Cloud Run functions: memory and CPU pairing, per-instance concurrency, min instances against cold starts, max instances to protect downstreams, and their cost effects."
sources: ["https://docs.cloud.google.com/sdk/gcloud/reference/functions/deploy", "https://docs.cloud.google.com/functions/docs/concepts/version-comparison", "https://docs.cloud.google.com/run/docs/configuring/services/memory-limits", "https://docs.cloud.google.com/run/docs/configuring/cpu", "https://docs.cloud.google.com/run/docs/configuring/concurrency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run functions: memory, concurrency and instances

## Settings
```bash
gcloud functions deploy resize --gen2 --region=<R> --runtime=python312 --source=. \
  --entry-point=handler --trigger-http \
  --memory=1GiB --cpu=1 --concurrency=20 \
  --min-instances=1 --max-instances=50 --timeout=120s
```
- Memory/CPU: `--cpu` is only valid together with `--memory`. Cloud Run's default is 512 MiB per instance and the maximum is 32 GiB; larger memory needs more CPU (more than 512 MiB needs at least 0.5 vCPU, more than 1 GiB needs at least 1 vCPU), and fractional CPU forces concurrency 1.
- **Concurrency** (Cloud Run functions): up to 1000 concurrent requests per instance (Cloud Run services default to 80). Raise it for I/O-bound handlers so one instance serves many requests; code must be thread/async-safe (no global mutable request state).
- **Min instances**: keeps N instances warm, which helps reduce cold starts.
- **Max instances**: caps scale-out to protect databases/APIs (for example keep max instances x pool size below the database connection limit).

## Cold start reduction
- Lazy-load heavy imports; initialise clients globally (reused across invocations).
- Smaller deployment packages; avoid large dependency trees.
- Startup CPU boost (`--cpu-boost` on `gcloud run services update` or `gcloud run deploy`).

## Event-driven functions
Concurrency applies to event triggers too; with Pub/Sub, high concurrency + retries can amplify
load on failures. Set max-instances with retry policies.

## Cost
Billed per instance time (CPU + memory) while handling requests, or for the whole instance lifetime with instance-based billing, plus requests. Check the Cloud Run pricing page for rates.

## Gotchas
- 1st gen functions: 1 concurrent request per instance; migrate for these options.
- Instances that exceed their memory limit are terminated.

## Verify
- [ ] Load test: p95 latency is acceptable and the instance count stays under `--max-instances`.

## Checked

2026-10-24, gcloud functions deploy reference, Cloud Run functions version comparison, Cloud Run memory, CPU and concurrency pages on docs.cloud.google.com. Confirmed: flag names (`--memory`, `--cpu`, `--concurrency`, `--min-instances`, `--max-instances`, `--timeout`), 1000 concurrent requests for Cloud Run functions versus 1 for 1st gen, memory default and maximum, CPU-to-memory minimums, fractional CPU concurrency rule, `--cpu-boost`. Removed unconfirmed claims: 0.583 vCPU per GiB, 1 vCPU needed for concurrency above 1, 429 queueing behaviour, memory-exceeded log text, cost statements.

Method: documentation only; no commands were run.
