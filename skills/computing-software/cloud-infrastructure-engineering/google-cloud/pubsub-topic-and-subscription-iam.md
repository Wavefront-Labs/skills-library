---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pubsub-topic-and-subscription-iam
name: pubsub-topic-and-subscription-iam
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, pubsub, pubsub-iam, topic-permissions, least-privilege, cross-project]
level: practitioner
status: docs-checked
description: "Grant Pub/Sub access per topic and subscription: publisher vs subscriber vs viewer roles, cross-project publishing, push auth service accounts, and the Pub/Sub service agent."
sources: ["https://docs.cloud.google.com/pubsub/docs/access-control", "https://docs.cloud.google.com/pubsub/docs/authenticate-push-subscriptions", "https://docs.cloud.google.com/pubsub/docs/handling-failures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub topic and subscription IAM

## 1. Grant at the resource, not the project
```bash
gcloud pubsub topics add-iam-policy-binding orders \
  --member=serviceAccount:checkout@<APP_P>.iam.gserviceaccount.com --role=roles/pubsub.publisher
gcloud pubsub subscriptions add-iam-policy-binding orders-billing \
  --member=serviceAccount:billing@<P>.iam.gserviceaccount.com --role=roles/pubsub.subscriber
```
| Role | Grants |
|---|---|
| `roles/pubsub.publisher` | publish to the topic only |
| `roles/pubsub.subscriber` | `pubsub.subscriptions.consume`, `pubsub.snapshots.seek` and `pubsub.topics.attachSubscription` |
| `roles/pubsub.viewer` | read-only get and list on topics, subscriptions, snapshots and schemas |
| `roles/pubsub.editor` / `roles/pubsub.admin` | modify topics and subscriptions (both include `pubsub.subscriptions.create` and `pubsub.topics.attachSubscription`); keep for IaC identities |

Project-level `pubsub.subscriber` lets a workload read every subscription in the project: avoid it.

## 2. Cross-project
- Publisher in project A to topic in project B: grant `publisher` on B's topic to A's SA. No other setup.
- Subscription in project C to topic in B: permissions are needed on both sides. The creator needs `pubsub.topics.attachSubscription` on the topic in B (included in `roles/pubsub.subscriber`) and `pubsub.subscriptions.create` in project C (included in `roles/pubsub.editor`).

## 3. Service agent grants
The Pub/Sub service agent `service-<NUM>@gcp-sa-pubsub.iam.gserviceaccount.com` needs:
- `roles/pubsub.publisher` on the dead-letter topic and `roles/pubsub.subscriber` on the source subscription (dead lettering).
- `roles/iam.serviceAccountTokenCreator` on the push auth service account (or an equivalent grant of `iam.serviceAccounts.getOpenIdToken`).
- `roles/cloudkms.cryptoKeyEncrypterDecrypter` on CMEK keys, and write access on the BigQuery table or Cloud Storage bucket for export subscriptions.

## Gotchas
- `gcloud pubsub topics set-iam-policy` replaces the whole policy; prefer add/remove binding.
- VPC Service Controls can block cross-project access even when IAM is right; check audit logs for violations.
- Push endpoints on Cloud Run need the push service account to have `roles/run.invoker` on the service.

## Verify
- [ ] `gcloud pubsub topics get-iam-policy orders` shows only intended publishers; a test publish from an ungranted service account is denied.

## Checked
Checked 2026-10-24 against the Pub/Sub access-control, authenticate-push-subscriptions and handling-failures documentation (docs.cloud.google.com). Confirmed role permissions, the attachSubscription/create split for cross-project subscriptions, the service agent address form, the TokenCreator and run.invoker requirements for push, and the dead-letter grants (publisher on the dead-letter topic, subscriber on the subscription). Removed the claim that newer projects get TokenCreator implicitly and the audit-log field name, which were not confirmed.
Method: documentation only; no commands were run.
