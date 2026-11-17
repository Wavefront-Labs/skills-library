---
id: computing-software.cloud-infrastructure-engineering.google-cloud.eventarc-triggers-and-eventarc-advanced
name: eventarc-triggers-and-eventarc-advanced
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, eventarc, eventarc-triggers, eventarc-audit-log-trigger, eventarc-advanced, message-bus, eventarc-pipelines, cloudevents]
level: advanced
status: docs-checked
description: "Route events with Eventarc Standard triggers (direct, Pub/Sub, audit-log path patterns) and Eventarc Advanced buses, enrollments and pipelines with CEL filters."
sources: ["https://docs.cloud.google.com/eventarc/standard/docs/run/route-trigger-cloud-audit-logs", "https://docs.cloud.google.com/eventarc/standard/docs/event-providers-targets", "https://docs.cloud.google.com/eventarc/advanced/docs/overview", "https://docs.cloud.google.com/sdk/gcloud/reference/eventarc", "https://docs.cloud.google.com/eventarc/docs/understand-locations", "https://docs.cloud.google.com/eventarc/docs/roles-permissions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eventarc triggers and Eventarc Advanced

## 1. Standard triggers
```bash
SA=eventarc-trg@<P>.iam.gserviceaccount.com   # needs roles/eventarc.eventReceiver (project) + roles/run.invoker (on the Cloud Run service)
# Direct event: GCS object finalized
gcloud eventarc triggers create on-upload --location=europe-west2 \
  --destination-run-service=ingest --destination-run-region=europe-west2 --destination-run-path=/events \
  --event-filters=type=google.cloud.storage.object.v1.finalized --event-filters=bucket=<B> \
  --service-account=$SA
# Audit-log event with a path pattern
gcloud eventarc triggers create on-csv-write --location=global \
  --destination-run-service=ingest --destination-run-region=europe-west2 \
  --event-filters=type=google.cloud.audit.log.v1.written \
  --event-filters=serviceName=storage.googleapis.com --event-filters=methodName=storage.objects.create \
  --event-filters-path-pattern=resourceName='/projects/_/buckets/<B>/objects/landing/*.csv' \
  --service-account=$SA
# Existing Pub/Sub topic
gcloud eventarc triggers create on-msg --location=<R> --destination-run-service=ingest --destination-run-region=<R> \
  --event-filters=type=google.cloud.pubsub.topic.v1.messagePublished --transport-topic=projects/<P>/topics/orders --service-account=$SA
```
- Filters are exact match; use `--event-filters-path-pattern` for resource path patterns.
- Prefer direct events when one exists: lower latency, strongly typed format, collection-ID filtering and no extra cost from enabling audit logs. For audit-log triggers the monitored service must be writing audit logs, and the related API must be enabled.
- Destinations: Cloud Run, Cloud Run functions, GKE services, internal HTTP endpoints in a VPC, and Workflows.
- The Cloud Storage example needs `roles/pubsub.publisher` on the Cloud Storage service agent.

## 2. Eventarc Advanced (bus model)
For many producers and consumers, filtering and transformation: a **bus** receives events, an **enrollment** matches them with a CEL expression and names a **pipeline**, and the pipeline delivers to one destination, optionally transforming the payload.
```bash
gcloud eventarc message-buses create orders-bus --location=<R>
gcloud eventarc pipelines create to-billing --location=<R> \
  --destinations=http_endpoint_uri='https://<TARGET_HOST>/events',google_oidc_authentication_service_account=$SA
gcloud eventarc enrollments create orders-to-billing --location=<R> --message-bus=orders-bus \
  --cel-match="<CEL_EXPRESSION>" \
  --destination-pipeline=to-billing
gcloud eventarc google-api-sources create gcp-events --location=<R> --destination-message-bus=orders-bus
```
- Destinations a pipeline can target: Cloud Run, Cloud Run functions, HTTP endpoints in a VPC, a Pub/Sub topic, Workflows, or another Advanced bus.
- Publish to a bus with `gcloud eventarc message-buses publish` or the Publishing API. Events arrive in CloudEvents format as HTTP binary content mode.
- The edition is fully regional: enrollments and pipelines read only from a bus in their own region.
- Default retention is 24 hours with exponential backoff (one-second start, doubling, up to 60 seconds and 5 attempts). There is no ordering guarantee.
- Eventarc Advanced is not covered by the certifications that Eventarc Standard supports; an organisation policy can disable Advanced resources.

## Gotchas
- Trigger location must match the event source: Cloud Storage triggers use the bucket's location and cannot be `global`; audit-log triggers use a single region or `global`, never dual- or multi-region; Pub/Sub triggers use a single region.
- Eventarc Standard delivers at least once through Pub/Sub retries; handlers must be idempotent (CloudEvents `source` plus `id` identifies an event).
- A service-agent permission error when creating a trigger soon after first use can take a few minutes (potentially seven) to clear.

## Verify
- [ ] `gcloud eventarc triggers describe <T> --location=<R>` shows no failed `conditions`; uploading a test object reaches the service.
- [ ] Enrollment only forwards messages matching its CEL expression (check pipeline logs).

## Checked
2026-10-28. Confirmed against the audit-log routing page (exact match, path pattern flag, locations, known Compute Engine issue), the event routes page (direct events preferred and why), the providers and targets page (destinations), the Advanced overview (bus, enrollment, pipeline, destinations, regionality, retry defaults, ordering, compliance note), the locations and roles pages, and the Eventarc discovery document (`Enrollment.celMatch`, `messageBus`, `destination`). Removed: the specific CEL attribute names in the example (not documented in the fetched pages), the Data Access log requirement, and a made-up Cloud Run hostname.
Method: documentation only; no commands were run.
