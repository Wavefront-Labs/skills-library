---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pubsub-cmek-and-message-storage-policy
name: pubsub-cmek-and-message-storage-policy
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, pubsub, pubsub-cmek, message-storage-policy, data-residency, cloud-kms]
level: advanced
status: docs-checked
description: "Keep Pub/Sub messages in approved regions with message storage policies and encrypt them with CMEK, including org-policy resource locations and the publish-time enforcement option."
sources: ["https://docs.cloud.google.com/pubsub/docs/resource-location-restriction", "https://docs.cloud.google.com/pubsub/docs/encryption", "https://docs.cloud.google.com/sdk/gcloud/reference/pubsub/topics/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub CMEK and message storage policy

Pub/Sub is global: by default messages are stored in the region nearest the publisher. Residency
needs a **message storage policy**; key control needs **CMEK**.

## 1. Storage policy
```bash
gcloud pubsub topics create orders \
  --message-storage-policy-allowed-regions=europe-west1,europe-west4 \
  --message-storage-policy-enforce-in-transit
```
- Publishes from outside Google Cloud are routed to the nearest allowed region (with added latency); clients outside Google Cloud or in disallowed regions should use a locational or regional endpoint in an allowed region.
- `--message-storage-policy-enforce-in-transit` (the `enforceInTransit` field in the API) additionally rejects publish, pull and StreamingPull requests received in a region not in the policy with `FAILED_PRECONDITION`; clients in an allowed Google Cloud region may use the global endpoint, others need a locational or regional endpoint. Push delivery is limited to allowed regions.
- The Resource Location Restriction organization policy applies to new topics without an explicit policy; a topic policy may contain only regions the organization policy allows, and changes do not propagate to existing topics (`gcloud pubsub topics update --recompute-message-storage-policy` re-applies it).

## 2. CMEK
```bash
gcloud kms keys add-iam-policy-binding pubsub-key --keyring=msg --location=europe-west1 \
  --member=serviceAccount:service-<NUM>@gcp-sa-pubsub.iam.gserviceaccount.com \
  --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
gcloud pubsub topics create orders --topic-encryption-key=projects/<P>/locations/europe-west1/keyRings/msg/cryptoKeys/pubsub-key \
  --message-storage-policy-allowed-regions=europe-west1
```
- Google recommends global Cloud KMS keys for CMEK topics; use a regional key only when a message storage policy restricts storage to that region with enforce-in-transit, or all clients use the same regional endpoint.
- Cloud KMS encrypts the per-topic data encryption keys (DEKs) that Pub/Sub creates, not the messages directly; Pub/Sub caches keys for roughly 30 minutes.
- If Pub/Sub cannot access the key, publishing and pull delivery fail with `FAILED_PRECONDITION` and push delivery stops; after access is restored, publishing recovers within about 12 hours and delivery within about 2 hours.

## Gotchas
- Changing the topic's key is not retroactive: earlier messages stay under the original key.
- Dead-letter topics are separate topics and need their own storage policy and key settings.

## Verify
- [ ] `gcloud pubsub topics describe orders` shows the message storage policy and the topic's `kmsKeyName`.

## Checked
Checked 2026-10-24 against the Pub/Sub message-storage-location (resource location restriction) and encryption documentation and the gcloud `pubsub topics create` reference (docs.cloud.google.com). Confirmed flags `--message-storage-policy-allowed-regions`, `--message-storage-policy-enforce-in-transit`, `--topic-encryption-key`, the service agent form `service-PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com`, the KMS role, key-location guidance, disabled-key behaviour and non-retroactive key change. Removed the unconfirmed restrictNonCmekServices claim, snapshot/retained-message claim and the exact field names in the verify step.
Method: documentation only; no commands were run.
