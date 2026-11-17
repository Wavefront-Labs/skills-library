---
id: computing-software.cloud-infrastructure-engineering.google-cloud.transfer-appliance-ordering-and-offline-transfer
name: transfer-appliance-ordering-and-offline-transfer
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, transfer-appliance, transfer-appliance-ordering, offline-transfer, data-migration, storage]
level: practitioner
status: docs-checked
description: "Decide when offline transfer beats the network, order and prepare a Transfer Appliance, copy data with encryption, ship it back, and verify the upload into Cloud Storage."
sources: ["https://docs.cloud.google.com/transfer-appliance/docs/4.0/overview", "https://docs.cloud.google.com/architecture/migration-to-google-cloud-transferring-your-large-datasets", "https://docs.cloud.google.com/sdk/gcloud/reference/storage/hash"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer Appliance ordering and offline transfer

## 1. Decide
Rough online time = data size / usable bandwidth. Google's example: 100 TB over an ideal 1 Gbps link takes about 12 days, and over 100 Mbps more than 100 days.
If online transfer is too slow, or bandwidth is shared with production, order an
appliance. Transfer Appliance 4.0 comes as TA40 and TA300, rackable or freestanding; check the Order page in the console for your country.

## 2. Order and prepare
1. Console → Transfer Appliance → Create order: data size, shipping address, destination bucket, contacts, appliance model.
2. Follow the prerequisites the order page gives for access to the destination bucket and the Cloud KMS key (customer-managed keys protect your data before shipping).
3. Install the appliance (rackable or freestanding model), cable it and set its network address.

## 3. Copy
- Linux and macOS systems mount the appliance's NFS share; Windows systems use SCP, SSH or SMB. Data is protected with the customer-managed key you manage in Cloud KMS.
- Parallelise copies across many streams; many tiny files hurt throughput, so archive them first.
- Keep a manifest (paths + checksums) of what you copied.

## 4. Ship and verify
Ship it back; Google uploads the data to your Cloud Storage bucket, then wipes the appliance. Then:
```bash
gcloud storage ls -r gs://<B>/prefix/** | wc -l
gcloud storage hash gs://<B>/path/file --hex   # compare to source manifest for a sample
```
Run an incremental online transfer (Storage Transfer Service, agent-based) for files changed since the copy.

## Gotchas
- Order early in the migration plan; you are given a set number of days for data capture and return shipping.
- Appliances are wiped after upload (NIST 800-88 erasure; a wipe certificate can be requested); keep the source until verification is complete.

## Checked
2026-10-31. Confirmed against the Transfer Appliance 4.0 overview (TA40 and TA300, rackable and freestanding, NFS for Linux/macOS, SCP/SSH/SMB for Windows, customer-managed Cloud KMS keys, upload then wipe, NIST 800-88 erasure and wipe certificate) and the Google large-dataset transfer guide (100 TB over 1 Gbps about 12 days; over 100 Mbps more than 100 days). Removed unconfirmed: TA7, 1 PB figure, week thresholds, IAM role names, `ta` tool, 10/40 GbE, object-name rule, lead-time claim; dead order and permissions sources.
Method: documentation only; no commands were run.

## Verify
- [ ] Object count and a checksum sample match the manifest; delta transfer completed; wipe certificate requested if your compliance needs it.
