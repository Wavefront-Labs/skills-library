---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-eventarc-triggers-and-delivery
name: troubleshooting-eventarc-triggers-and-delivery
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, eventarc, eventarc-troubleshooting, event-delivery, audit-log-triggers, pubsub-transport, dead-letter]
level: practitioner
status: docs-checked
description: "Debug Eventarc triggers that do not fire or deliver: readiness, audit log enablement, filters, Pub/Sub transport, trigger SA IAM, retries and dead letters."
sources: ["https://docs.cloud.google.com/eventarc/docs/troubleshooting", "https://docs.cloud.google.com/eventarc/standard/docs/run/event-routing-options", "https://docs.cloud.google.com/eventarc/docs/retry-events", "https://docs.cloud.google.com/eventarc/docs/understand-locations", "https://docs.cloud.google.com/eventarc/docs/roles-permissions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Eventarc triggers and delivery

## Checklist
```bash
gcloud eventarc triggers describe <T> --location=<L> --format="yaml(conditions,eventFilters,destination,serviceAccount,transport)"
```
1. **Trigger healthy?** `conditions` lists the reasons a trigger is failed; a missing or unknown transport topic shows as `transport.pubsub.topic` with code `NOT_FOUND` (recreate the trigger) or `UNKNOWN` (describe again).
2. **Is the provider producing events?** For audit-log events, check Cloud Audit Logs and confirm the monitored service is writing logs; if logs exist but nothing arrives, contact support. Also check the topic named after the trigger exists (`gcloud pubsub topics list`; `gcloud eventarc triggers list --location=-` lists triggers in all locations).
3. **Event filters right?** Filtering is exact match with no wildcards or regular expressions; for audit logs use `serviceName`, `methodName` and optionally `resourceName`, or `--event-filters-path-pattern` for resource path patterns. Prefer a direct event over an audit-log event when both exist (lower latency, typed format, no extra audit-log cost).
4. **Location** must match the event source. Cloud Storage triggers: single-region, dual-region or multi-region, never `global`, and the trigger location must equal the bucket location (a mismatch returns an error). Audit-log triggers: single regions or `global`, not dual- or multi-region. Pub/Sub triggers: single region only. Compute Engine audit-log events come only from `us-central1` (a known issue), so use `us-central1` or `global`.
5. **IAM**:
   - Trigger service account: `roles/eventarc.eventReceiver` on the project, plus `roles/run.invoker` on an authenticated Cloud Run target.
   - Cloud Storage direct events: `roles/pubsub.publisher` for the Cloud Storage service agent.
   - `Failed to load service details: permission denied`: the Pub/Sub service account needs `roles/iam.serviceAccountTokenCreator`.
   - Creating a trigger can fail with "Permission denied while using the Eventarc Service Agent" soon after first use: wait a few minutes (potentially seven) and retry, then check that `service-PROJECT_NUMBER@gcp-sa-eventarc.iam.gserviceaccount.com` holds the Eventarc Service Agent role.

## Transport
Standard triggers use a Pub/Sub topic and a push subscription (`transport.pubsub.subscription`; generated subscription IDs begin `eventarc-REGION-`). Check:
```bash
gcloud pubsub subscriptions describe <SUB> --format="yaml(pushConfig,ackDeadlineSeconds,retryPolicy,deadLetterPolicy)"
```
Metrics: `topic/send_message_operation_count` shows whether messages reach the topic; `subscription/push_request_count` by `response_code` shows delivery. A non-OK status from the receiving endpoint means the target code is failing.

## Retries and dead letters
Standard delivery is at-least-once through the Pub/Sub retry policy: exponential backoff from a 10-second minimum to a 600-second maximum by default, with 24-hour message retention set by Eventarc. After the retention window an event is discarded unless a dead-letter topic is configured. Set the dead-letter topic on the subscription (not the topic). Change backoff with `gcloud pubsub subscriptions update <SUB> --min-retry-delay=... --max-retry-delay=...` (both from 0 to 600 seconds). Cloud Run targets can be set to a single attempt with no retries, the default for triggers made from the Cloud Run page; the docs recommend that during development. Workflows destinations acknowledge as soon as the execution starts, so later workflow failures are not retried.

## Gotchas
- Duplicates happen: the CloudEvents `source` plus `id` pair identifies an event, so handlers should be idempotent.
- A filter that matches the handler's own writes can trigger indefinitely and cause unexpected charges; set budgets and alerts.
- Pub/Sub push backoff can pause delivery for 100 milliseconds up to 60 seconds after many negative acknowledgements.
- With a CMEK-protected channel the key is not shown in the console; read `kmsKeyName` from `gcloud pubsub topics describe`.

## Verify
- [ ] A test event (for example uploading an object) reaches the target logs with the CloudEvents `ce-type` header.

## Checked
2026-10-28. Confirmed against the Eventarc troubleshooting, event routes, retry events, locations and roles pages, plus the Eventarc and Pub/Sub discovery documents (`Trigger.conditions`, `eventFilters`, `transport`; `Subscription` fields). Removed: a two-minute activation and lost-events claim, case sensitivity of method names, mandatory Data Access logs, `workflows.invoker`, an IAP-target and ingress claim, and the unsupported bucket-prefix remark.
Method: documentation only; no commands were run.
