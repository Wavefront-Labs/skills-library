---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firestore-triggers-with-eventarc-and-functions
name: firestore-triggers-with-eventarc-and-functions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, firestore, firestore-triggers, firestore-eventarc, cloud-run-functions, event-driven]
level: practitioner
status: docs-checked
description: "React to Firestore document writes with Cloud Run functions via Eventarc: event types, path patterns, protobuf payload decoding, idempotency and infinite-loop traps."
sources: ["https://docs.cloud.google.com/firestore/docs/extend-with-functions-2nd-gen", "https://docs.cloud.google.com/eventarc/docs/run/route-trigger-cloud-firestore", "https://docs.cloud.google.com/eventarc/docs/retry-events", "https://docs.cloud.google.com/sdk/gcloud/reference/functions/deploy", "https://github.com/googleapis/google-cloudevents-python"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firestore triggers with Eventarc and Cloud Run functions

## 1. Event types
`google.cloud.firestore.document.v1.created`, `.updated`, `.deleted`, `.written` (all changes), plus
`.created.withAuthContext` etc. that add authentication information. Triggers apply to documents, not to fields or collections, and each trigger is tied to a single database. Datastore mode databases use `google.cloud.datastore.entity.v1.*` types.

## 2. Deploy a function trigger
```bash
gcloud functions deploy on-order-write --gen2 --runtime=<RUNTIME> --region=<REGION> \
  --entry-point=handle --source=. \
  --trigger-event-filters=type=google.cloud.firestore.document.v1.written \
  --trigger-event-filters=database='(default)' \
  --trigger-event-filters-path-pattern=document='orders/{orderId}' \
  --trigger-service-account=fs-trigger@<P>.iam.gserviceaccount.com --retry
```
- The trigger must be in the same location as the Firestore database (see the Eventarc and Firestore location pages for multi-region databases); `--trigger-location` must be a region or multi-region where the events originate.
- Path patterns must point at a document: `{wildcard}` matches one document ID and does not match documents in subcollections; `{wildcard=**}` also matches subcollection documents. You can use several single-segment wildcards but only one multi-segment wildcard.
- For Cloud Run services use `gcloud eventarc triggers create ... --location=<LOC> --event-filters=type=... --event-filters-path-pattern=document=... --destination-run-service=... --destination-run-region=... --event-data-content-type=application/protobuf`.

## 3. Decode the payload
The CloudEvent data is protobuf (`DocumentEventData`), not JSON; the Google sample parses it with `ParseFromString`:
```python
from google.events.cloud import firestore
import functions_framework
@functions_framework.cloud_event
def handle(ev):
    data = firestore.DocumentEventData()
    data._pb.ParseFromString(ev.data)
    before, after = data.old_value, data.value      # Document with .fields
    order_id = after.name.split("/")[-1]
```

## Gotchas
- **Infinite loops**: writing to the triggering document can fire another event. Use `created` triggers or write only when the value actually changes.
- Delivery is at least once and not ordered: make handlers idempotent (use the event `id`).
- Retries: Eventarc retries within a default 24-hour window with exponential backoff (10 to 600 seconds); the default depends on how the trigger is created (the Cloud Run console flow defaults to a single attempt, while the gcloud CLI enables retries by default). Catch bad data and return success.
- The trigger service account needs Cloud Run Invoker and Eventarc Event Receiver (`roles/run.invoker`, `roles/eventarc.eventReceiver`). Direct Firestore events do not need audit logs enabled.

## Verify
- [ ] Writing a test document produces an invocation in the function's logs; `gcloud eventarc triggers list --location=<R>` shows the trigger.

## Checked
Checked 2026-10-24 against the Firestore extend-with-functions and Eventarc Firestore trigger documentation, the Eventarc retry-events page, the gcloud `functions deploy` reference (docs.cloud.google.com) and the googleapis google-cloudevents-python `DocumentEventData` type. Confirmed event types, path-pattern rules, the `--trigger-event-filters`, `--trigger-event-filters-path-pattern`, `--trigger-location`, `--trigger-service-account` and `--retry` flags, at-least-once and unordered delivery, and the 24-hour retry window. Wrong claim fixed: retries are not always on, because the default depends on how the trigger is created. Removed the multi-region trigger-location details, which the pages do not give, and replaced the example runtime with a placeholder (list runtimes with `gcloud functions runtimes list`).
Method: documentation only; no commands were run.
