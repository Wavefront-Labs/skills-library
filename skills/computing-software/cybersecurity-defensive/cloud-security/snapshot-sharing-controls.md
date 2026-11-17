---
id: computing-software.cybersecurity-defensive.cloud-security.snapshot-sharing-controls
name: snapshot-sharing-controls
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [snapshot-sharing-controls, ebs-snapshots, ami-sharing, block-public-access-snapshots, rds-snapshots, data-exfiltration-prevention, cloud-data-protection]
level: practitioner
status: docs-checked
description: "Prevent snapshot and image leaks: EBS snapshot and AMI block public access, RDS snapshot sharing limits, and GCP snapshot IAM risk."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/block-public-access-snapshots.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sharingamis-intro.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-public-access-to-amis.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ShareSnapshot.html", "https://docs.cloud.google.com/compute/docs/disks/snapshot-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot sharing controls

A shared snapshot or image lets the recipient copy the data, so sharing is an exfiltration path and a common accidental public exposure.

## EBS snapshots
- **Block public access for snapshots** has two modes: *block all sharing* (no new public sharing, and already-public snapshots are treated as private) and *block new sharing* (already-public snapshots stay public).
- It is a per-Region, account-level setting that applies to all users including admins; not available at org level directly. Use a declarative policy to apply it across Regions and accounts (the setting then cannot be changed in the account).
- It does not stop private sharing, does not stop public sharing of EBS-backed AMIs (whose snapshots become readable), and is unsupported for local snapshots on Outposts.
- Under *block all sharing*, snapshot attributes still say public; if you later disable or switch to *block new sharing*, they become public again.

## AMIs
- **Block public access for AMIs** blocks making an AMI public; existing public AMIs remain public. It is per Region and account level (or declarative policy), and can be limited by IAM to an admin.
- Defaults: enabled for new accounts and for existing accounts with no public AMIs; disabled for accounts that had public AMIs on or after 15 July 2023.
- AMIs with encrypted volumes, snapshots of encrypted volumes or product codes cannot be made public, but can be shared with specific accounts. Sharing is via `launchPermission` (`Group=all` is public).

## RDS snapshots
- Manual snapshots can be shared with up to 20 accounts (`aws rds modify-db-snapshot-attribute --attribute-name restore --values-to-add ...`); list with `describe-db-snapshot-attributes`. Automated snapshots must be copied first.
- `all` makes a snapshot public; encrypted snapshots cannot be public, and snapshots encrypted with the default AWS KMS key cannot be shared at all. A shared encrypted snapshot must be copied before restoring. Multi-AZ DB cluster snapshots cannot be shared.

## GCP
The cited best-practices page covers one security point: grant `compute.snapshots.useReadOnly` and `compute.instantSnapshots.useReadOnly` only to trusted principals, because holders can restore the snapshot into a project they control, even in another organisation. Audit who holds them.

## Verify
- [ ] Block public access is set in every Region used (or by declarative policy).
- [ ] No snapshot or AMI shows public attributes (check the attributes, not only availability).

## Checked
Method: 2026-11-08 read the five cited pages (the RDS page body, EBS, AMI sharing and AMI block-public-access pages, GCP best practices) in full. Removed unsupported claims: SCP action-deny lists, KMS key-policy conditions, RCP mention, Azure snapshot settings, GCP trustedImageProjects, CloudTrail detection and Security Hub control IDs. Added the AMI block-public-access page as a source. Other CLI commands and facts unchanged where the pages state them.
