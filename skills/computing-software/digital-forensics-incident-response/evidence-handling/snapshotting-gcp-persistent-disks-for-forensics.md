---
id: computing-software.digital-forensics-incident-response.evidence-handling.snapshotting-gcp-persistent-disks-for-forensics
name: snapshotting-gcp-persistent-disks-for-forensics
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [gcp-disk-snapshot, cloud-snapshot, cloud-evidence, gcp-incident-response, dfir]
level: advanced
status: docs-checked
description: "Preserve GCP Compute Engine disks: snapshot a suspect instance's disks, create a disk and image in a forensic project, export the image, and attach it read-only for analysis."
sources: ["https://cloud.google.com/compute/docs/disks/create-snapshots", "https://cloud.google.com/compute/docs/images/export-image", "https://cloud.google.com/logging/docs/audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshotting GCP persistent disks for forensics

**Goal:** preserve the disks of a suspect Compute Engine instance and move them to a forensic project the attacker cannot reach.

## Snapshot
```bash
gcloud compute instances describe VM --zone Z --format="value(disks[].source)"
gcloud compute snapshots create vm-boot-case014 --source-disk=vm-boot --source-disk-zone=Z \
  --storage-location=eu
```
- `--storage-location` overrides the predefined or customized default location in your snapshot settings; use it only when you need to override that default. A regionally scoped snapshot (preview) uses a scope region instead and cannot be combined with `--storage-location`.
- Required permissions on the project include `compute.snapshots.create` and, for a zonal disk, `compute.disks.createSnapshot`; the Compute Instance Admin (v1) role contains them.
- Admin Activity audit logs record user-driven API calls that modify resources and are always written (they cannot be disabled or excluded). Export the entries for your snapshot actions into the evidence register.

## Move to forensic project
```bash
# create a disk in the forensic project from the snapshot
gcloud compute disks create evid-boot-case014 --project FORENSIC --zone Z \
  --source-snapshot=projects/VICTIM/global/snapshots/vm-boot-case014
# optional: export to an image file in a Cloud Storage bucket
gcloud compute images create evid-img --project FORENSIC --source-disk=evid-boot-case014 --source-disk-zone=Z
gcloud compute images export --project FORENSIC --image evid-img --destination-uri gs://forensic-evid/case014/boot.tar.gz
```
- The export `--destination-uri` is a Cloud Storage URI (the page's examples use `.tar.gz` and `.vmdk` names). Restrict access to the bucket and hash the exported file after download.
- The cross-project source-snapshot path, image creation from a disk and the read-only attach below are command forms checked against the gcloud reference; the pages above do not describe forensic use of them.

## Analyse
Attach the evidence disk to an isolated analysis VM as a secondary disk in read-only mode:
`gcloud compute instances attach-disk ANALYSIS --disk evid-boot-case014 --mode ro`.

## Verify
Snapshot and export identifiers, hashes and audit log entries are in the evidence register.

## Checked
Confirmed against the Compute Engine snapshot page (snapshot create command, `--storage-location` rule, required permissions), the export-image page (`gcloud compute images export --destination-uri`) and the Cloud Audit Logs page (Admin Activity logs always written); all gcloud commands were also checked against the gcloud reference (no missing commands or flags). Removed claims the pages do not give: crash-consistent and `--guest-flush` VSS behaviour, the `compute.snapshots.insert` audit method name, `compute.snapshots.useReadOnly`, the `--labels` flag, bucket retention policy and lock, CMEK key access, local SSD behaviour and boot disk auto-delete.

Method: docs-only read of cited pages, 2026-11-08
