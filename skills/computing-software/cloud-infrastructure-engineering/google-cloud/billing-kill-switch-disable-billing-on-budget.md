---
id: computing-software.cloud-infrastructure-engineering.google-cloud.billing-kill-switch-disable-billing-on-budget
name: billing-kill-switch-disable-billing-on-budget
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, disable-billing, cap-spending, billing-kill-switch, budget-automation, pubsub-budget-notifications, cloud-run-functions, billing-api, spending-cap, sandbox-cost-control, runaway-cost]
level: advanced
status: docs-checked
description: "Build a budget-triggered kill switch: Pub/Sub budget notification to a function that disables project billing, with the IAM needed and the warning about lost resources."
sources: ["https://cloud.google.com/billing/docs/how-to/disable-billing-with-notifications", "https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications", "https://cloud.google.com/billing/docs/reference/rest/v1/projects/updateBillingInfo", "https://cloud.google.com/sdk/gcloud/reference/billing/budgets/create", "https://cloud.google.com/sdk/gcloud/reference/billing/projects/link"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing kill switch: disable billing when a budget is exceeded

**Goal:** a sandbox or student project stops incurring cost when a budget is reached. Budgets
alone only email; this makes them act. It is destructive and not a hard cap.

## 1. How it works
Budget, connected to a Pub/Sub topic, publishes its current status several times a day. A Cloud Run
function compares `costAmount` with `budgetAmount` and, if cost is higher, calls the Cloud Billing
API `projects.updateBillingInfo` with an empty `billingAccountName`. That terminates all Google Cloud
services in the project, including Free Tier services. **Resources might be irretrievably deleted**;
re-enabling billing needs manual configuration and service recovery is not guaranteed.

Limits stated by Google: there is a delay between incurring cost and receiving notifications, so
this does not guarantee spend stays within the budget (set the budget below your available funds);
and a project locked to its billing account cannot have billing disabled.

## 2. Build
```bash
gcloud pubsub topics create budget-alerts
gcloud billing budgets create --billing-account=<BA_ID> --display-name="sbx-cap" \
  --budget-amount=100 --filter-projects=projects/<PROJECT_ID> \
  --threshold-rule=percent=1.0 \
  --notifications-rule-pubsub-topic=projects/<PROJECT_ID>/topics/budget-alerts
```
The budget must be scoped to a single project, and the Cloud Billing API enabled (the tutorial
also enables `billingbudgets`, `cloudfunctions`, `eventarc`, `run`, `pubsub`, `cloudbuild` and
`artifactregistry`). Function (Python, Cloud Run function triggered by the topic; entry point
`stop_billing`), adapted from the tutorial's sample with simulation on:
```python
import base64, json
from google.cloud import billing_v1

client = billing_v1.CloudBillingClient()
SIMULATE_DEACTIVATION = True   # set False only after testing with a test budget

def stop_billing(cloud_event):
    d = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8"))
    if d["costAmount"] <= d["budgetAmount"]:
        return
    name = "projects/<PROJECT_ID>"        # the project to cap
    if not client.get_project_billing_info(name=name).billing_enabled:
        return                            # already off: idempotent
    if SIMULATE_DEACTIVATION:
        print("Billing disabled. (Simulated)")
        return
    client.update_project_billing_info(
        name=name,
        project_billing_info=billing_v1.ProjectBillingInfo(billing_account_name=""))
```
Deploy with the console or `gcloud functions deploy` using `--gen2 --region --trigger-topic
--entry-point --set-env-vars --source --service-account`, as in the tutorial script.

## 3. Make it safe
- The function runs as an automatically created service account unless you set one. The tutorial
  grants that account `roles/billing.admin` on the billing account
  (`gcloud billing accounts add-iam-policy-binding`); `updateBillingInfo` requires the caller to
  be an owner of the project or of the billing account.
- If the function lives in the project it disables, it is disabled too. Run it in another project.
- Cost values are in the budget's `currencyCode`. Scope the budget to exactly the project(s) you cap,
  because `costAmount` covers the whole budget scope.
- Notifications are repeated all period, so check `billing_enabled` first (idempotency).
- Keep `SIMULATE_DEACTIVATION` true until a test budget proves the flow.
- Alert on the function's own errors; a silent failure is a cap that does not exist.

## 4. Recovery
```bash
gcloud billing projects link <PROJECT_ID> --billing-account=<BA_ID>
```
Re-link needs permission to attach the project (`roles/billing.user` on the account combined with
`roles/billing.projectManager` or ownership of the project). Raise the budget first, or the next
notification disables billing again. Do not assume stopped resources come back; check each service.

## Verify
- [ ] With simulation on, a test budget triggers a "Simulated" log entry and no unlinking.
- [ ] After setting simulation off on a throwaway project, `gcloud billing projects describe <PROJECT_ID>` shows it no longer has a billing account.

## Checked
Date: 2026-11-07.
Method: documentation only; no commands were run.
Read in full: "Disable billing usage with notifications" (warning, limitations, full example script, Node.js and Python functions, service account section), REST `projects.updateBillingInfo`, gcloud reference for `billing budgets create`, and the notification format part of "Set up programmatic notifications" (attributes and data table; its permissions section only skimmed). The role statements for `billing.user` and `billing.projectManager` come from the "Cloud Billing access control" role table.
Corrections: the earlier claim "nothing is deleted; re-link to recover" contradicted the page and was reversed; removed the 20-30 minute cadence, "up to a day of lag" and 10-30 % overshoot figures, the `projectManager`-only IAM claim (the tutorial grants billing.admin), the VM-restart recovery step, the Marketplace/support charges and liens gotchas, the `python312` runtime pin and the invented hand-made-message Verify step; the Python sample now follows the tutorial's `billing_v1` client instead of an unverified discovery-client call.
