---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-functions-triggers-and-retries
name: cloud-run-functions-triggers-and-retries
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run-functions, functions-triggers, http-trigger, event-trigger, functions-retry, retry-on-failure, idempotency, eventarc]
level: practitioner
status: docs-checked
description: "Wire Cloud Run functions to HTTP, Pub/Sub, Cloud Storage and audit-log events, enable retries for event functions, and make handlers idempotent and safe from infinite retry loops."
sources: ["https://docs.cloud.google.com/sdk/gcloud/reference/functions/deploy", "https://docs.cloud.google.com/functions/docs/bestpractices/retries", "https://docs.cloud.google.com/functions/docs/concepts/version-comparison"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run functions: triggers and retries

## 1. Trigger types
```bash
# HTTP
gcloud functions deploy api --gen2 --trigger-http ...
# Pub/Sub topic
gcloud functions deploy on-order --gen2 --trigger-topic=orders ...
# Cloud Storage: object created or overwritten in the bucket
gcloud functions deploy on-upload --gen2 --trigger-bucket=<B> ...
# Any other Eventarc source: matching criteria, location and trigger service account
gcloud functions deploy on-event --gen2 --trigger-location=<R> \
  --trigger-event-filters=<ATTRIBUTE>=<VALUE> \
  --trigger-service-account=fn-trigger@<P>.iam.gserviceaccount.com
```
`--trigger-event-filters` takes the Eventarc matching criteria, `--trigger-location` must be a region or multi-region where the events originate, and `--trigger-service-account` is the service account associated with the Eventarc trigger. See the Eventarc event reference for the exact event types and attributes per source.

## 2. Retries
- `gcloud functions deploy --retry` makes the function be retried in case of failure; without it, whether a failed event is retried depends on the event source and trigger configuration. Pub/Sub's default is to redeliver with exponential backoff.
- Functions created with the Cloud Run Admin API configure retries on the Eventarc trigger (and a dead-letter topic in Pub/Sub) instead.
- The Pub/Sub retry window can be shortened from the default 7 days to as little as 10 minutes.

## 3. Make retries safe
```python
import functions_framework, datetime
from google.cloud import firestore
db = firestore.Client()
MAX_AGE = datetime.timedelta(hours=1)

@functions_framework.cloud_event
def handle(event):
    age = datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(event["time"].replace("Z", "+00:00"))
    if age > MAX_AGE:
        return                       # stop retrying ancient events
    ref = db.collection("processed").document(event["id"])
    if ref.get().exists:             # idempotency on CloudEvent id
        return
    process(event.data)              # raise on transient failure -> retried
    ref.set({"at": firestore.SERVER_TIMESTAMP})
```
Set an end condition to avoid infinite retry loops: raise only for transient errors; for bad input, log and return success (or use a dead-letter topic) so poison messages do not retry for the whole retry window.

## Gotchas
- A function that writes to the bucket that triggers it can loop forever; write to a different bucket.
- Make event handlers idempotent, because retried events are delivered again.

## Verify
- [ ] `gcloud functions describe on-order --region=<R>` shows the trigger configuration.
- [ ] A forced transient error is retried and succeeds; a poison event stops after the age cutoff.

## Checked

2026-10-24, gcloud functions deploy reference, Cloud Run functions retries best-practice page and version comparison on docs.cloud.google.com. Confirmed: `--trigger-http`, `--trigger-topic`, `--trigger-bucket`, `--trigger-event-filters`, `--trigger-location`, `--trigger-service-account`, `--retry`, the Eventarc-trigger retry model for functions created with the Cloud Run Admin API, the 7-day to 10-minute Pub/Sub retry window, the advice to set an end condition. Removed unconfirmed claims: HTTP functions are never retried, no retry by default, the audit-log example, event type strings, trigger service account roles and bucket location rule.

Method: documentation only; no commands were run.
