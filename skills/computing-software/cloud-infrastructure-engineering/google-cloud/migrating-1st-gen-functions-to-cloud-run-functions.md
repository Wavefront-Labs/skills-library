---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migrating-1st-gen-functions-to-cloud-run-functions
name: migrating-1st-gen-functions-to-cloud-run-functions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run-functions, functions-gen2-migration, upgrade-1st-gen-functions, cloud-functions-2nd-gen, eventarc-triggers]
level: practitioner
status: docs-checked
description: "Upgrade Cloud Functions 1st gen to Cloud Run functions: trigger and event format changes, URL changes, IAM roles, the upgrade tool or side-by-side redeploy, and traffic cutover."
sources: ["https://docs.cloud.google.com/sdk/gcloud/reference/functions/upgrade", "https://docs.cloud.google.com/functions/docs/concepts/version-comparison"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating 1st gen functions to Cloud Run functions

## What changes
| Area | 1st gen | Cloud Run functions (2nd gen) |
|---|---|---|
| Runtime | Cloud Functions infra | Cloud Run service + Eventarc |
| Event triggers | native (`--trigger-topic`, `--trigger-bucket`) | Eventarc triggers; CloudEvents format |
| Concurrency | 1 concurrent request per instance | up to 1000 per instance |
| Maximum timeout | up to 9 minutes | up to 60 minutes for HTTP functions; up to 9 minutes for event-driven functions created with the Cloud Functions v2 API |
| Event retries | `--retry` at deploy | `--retry` at deploy for functions created with the Cloud Functions v2 API; for Cloud Run Admin API functions, update the retry policy in Eventarc |

## Approaches
1. **In-place upgrade tool**: `gcloud functions upgrade <fn> --setup-config` creates a 2nd gen copy while traffic stays on 1st gen; `--redirect-traffic` sends production traffic to the copy (`--rollback-traffic` returns it); `--commit` finishes the upgrade and permanently deletes the 1st gen copy (it cannot be rolled back); `--abort` undoes the steps done so far. Use one action flag per invocation.
2. **Side-by-side**: deploy `fn-v2` with `--gen2`, test, switch callers/triggers, delete 1st gen.

## Code changes (Python background function)
```python
# 1st gen
def handler(event, context):
    data = base64.b64decode(event["data"])
# 2nd gen
import functions_framework
@functions_framework.cloud_event
def handler(cloud_event):
    data = base64.b64decode(cloud_event.data["message"]["data"])
```
HTTP functions usually need no code change.

## Gotchas
- Use a new name for a side-by-side copy so it does not clash with the 1st gen function.
- Retry configuration differs between generations (see the table); re-check it after migrating.
- Infrastructure-as-code uses a different resource type for 2nd gen functions; plan a state move or import.

## Verify
- [ ] Event-triggered test messages processed once by the new function; 1st gen invocations at zero before deletion.

## Checked

2026-10-24, gcloud functions upgrade reference and the Cloud Run functions version-comparison page on docs.cloud.google.com. Confirmed: upgrade action flags `--setup-config`, `--redirect-traffic`, `--rollback-traffic`, `--commit`, `--abort` and their semantics; concurrency 1 versus up to 1000; timeouts; retry handling. Corrected: the in-place upgrade command is `gcloud functions upgrade` (GA, with `beta` a variant) and the skill said it kept the cloudfunctions.net URL, which is not documented. Removed unconfirmed claims: invoker role and URL rows, event signature row, Eventarc trigger IAM roles, Pub/Sub ack-deadline note.

Method: documentation only; no commands were run.
