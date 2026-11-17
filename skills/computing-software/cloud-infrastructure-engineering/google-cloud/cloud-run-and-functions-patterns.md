---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-and-functions-patterns
name: cloud-run-and-functions-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run, cloud-run-functions, cloud-functions, serverless, containers, concurrency, min-instances, max-instances, cpu-allocation, instance-based-billing, request-based-billing, startup-cpu-boost, cold-start, cloud-run-jobs, worker-pools, eventarc, pubsub-push, dead-letter-topic, cloud-tasks, workflows, revisions, traffic-splitting, ingress, direct-vpc-egress, serverless-vpc-access, iam-invoker, idempotency]
level: practitioner
status: docs-checked
description: "Build on Cloud Run and Cloud Run functions: concurrency and billing mode, min/max instances, services vs jobs, Eventarc/Pub/Sub retry and dead-letter, VPC egress, ingress/IAM and revision rollouts."
sources: ["https://docs.cloud.google.com/run/docs/configuring/concurrency", "https://docs.cloud.google.com/run/docs/configuring/request-timeout", "https://docs.cloud.google.com/run/docs/configuring/cpu", "https://docs.cloud.google.com/run/docs/create-jobs", "https://docs.cloud.google.com/run/docs/securing/ingress", "https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration", "https://docs.cloud.google.com/functions/docs/concepts/version-comparison", "https://docs.cloud.google.com/functions/docs/bestpractices/retries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run and Cloud Run functions — configure the container contract deliberately

**Goal:** serverless services whose concurrency, billing mode and instance bounds match
the workload, whose event paths retry and dead-letter predictably, and whose rollouts
can be split and reverted per revision.

## 1. One platform
Cloud Functions (2nd gen) is now **Cloud Run functions**. Choose a function when you only
want to write a handler (source deploy, buildpacks); a service when you own the
Dockerfile, need multiple endpoints, or custom runtimes. Settings below apply to both.
1st-gen functions allow 1 concurrent request per instance and shorter timeouts; migrate for the newer options.

## 2. Concurrency, CPU and billing
- **Concurrency** (Cloud Run services default to 80; Cloud Run functions allow up to 1000 per instance): requests served at once per instance. Raise it for
  I/O-bound async servers; set **1** only for code that is not thread-safe or is CPU-heavy
  per request. Fractional CPU (below 1 vCPU) requires concurrency 1.
- **Billing mode:** *request-based* (CPU only allocated during requests; background
  work outside request processing is not guaranteed CPU) vs *instance-based* (CPU always
  allocated; billed for the instance lifetime). Background work
  after returning a response under request-based billing is a classic silent bug.
- **Startup CPU boost** (`--cpu-boost`) gives extra CPU during instance start-up to shorten cold starts.
- **Min instances** keeps instances warm for latency-sensitive services.
  **Max instances** caps blast radius on downstreams (e.g. DB connections ≈ max × pool size).

## 3. Services, jobs, worker pools
- **Service:** request timeout defaults to 5 minutes and can be extended up to 60 minutes.
- **Job:** run-to-completion tasks (`--tasks=N --parallelism=M`, `CLOUD_RUN_TASK_INDEX` for
  sharding, `--max-retries` per task from 0 to 10, task timeout up to 168 hours (1 hour for GPU tasks)). Use for batch,
  migrations, scheduled work via Cloud Scheduler.

## 4. Events and retries
- **Eventarc** triggers deliver events to Cloud Run. Pub/Sub's default is to resend a message with exponential backoff; the retry window can be shortened from the default 7 days to as little as 10 minutes, and a **dead-letter topic** can be configured on the Pub/Sub subscription.
- Functions: for functions created with the Cloud Functions v2 API, retries are enabled with `--retry` at deploy; for functions created with the Cloud Run Admin API, update the retry policy in Eventarc. Set an end condition so a deterministic bug does not retry for the whole window, and pair retries with a dead-letter topic.
- Make event handlers idempotent (dedupe on the CloudEvent `id`), because events can be redelivered.
- Need rate limiting or scheduled per-item dispatch? Put **Cloud Tasks** in front. Multi-step orchestration: **Workflows**, not service-to-service chains.

## 5. Networking and access
- **Ingress:** `all`, `internal`, or `internal-and-cloud-load-balancing`. Combine with
  `--no-allow-unauthenticated` and grant `roles/run.invoker` to calling service accounts;
  callers send an ID token with the service URL as audience.
- **Direct VPC egress** is preferred over VPC connectors for best performance when attaching a service to a VPC network.
- Run as a **dedicated service account**, not the Compute Engine default.

## 6. Revisions and rollouts
Every deploy creates an immutable revision. Deploy with `--no-traffic --tag=canary`,
test via the tagged URL, then
`gcloud run services update-traffic <SERVICE> --to-tags=canary=10` and step up;
`--to-latest` or `--to-revisions=<OLD>=100` to move all traffic.

## Gotchas
- The ingress container must listen on the `PORT` Cloud Run injects and become healthy within the startup probe window.
- Instances that exceed their memory limit are terminated, and in-memory volumes count against that limit.
- Watch downstream connection counts: instances x pool size.

## Verify
- [ ] Concurrency, billing mode, min/max instances set per service with a stated reason.
- [ ] No background work after response on request-billed services.
- [ ] Each event trigger has retry behaviour chosen and a DLQ topic with IAM for the Pub/Sub agent; DLQ alert exists.
- [ ] Replaying an event yields one side effect.
- [ ] Internal services: ingress restricted, unauthenticated access off, invoker granted only to caller SAs.
- [ ] A canary revision rollout and rollback have been exercised.

## Checked

2026-10-24, Cloud Run concurrency, request-timeout, CPU, create-jobs, ingress and traffic pages, and the Cloud Run functions version-comparison and retries pages on docs.cloud.google.com. Confirmed: concurrency default 80 and 1000 for Cloud Run functions, request timeout 300 s default and 3600 s maximum, fractional CPU concurrency rule, `--cpu-boost`, job flags and limits (`--max-retries` 0 to 10, 168 h timeout, 1 h for GPU), ingress values, traffic commands, Pub/Sub retry window, `--retry` handling by API type. Removed unconfirmed claims: 2024 rename date, instance-billing price statement, Eventarc subscription retention and DLQ attempt range, DLQ IAM roles, worker pools, Direct VPC flags and subnet sizing, `/tmp` behaviour.

Method: documentation only; no commands were run.
