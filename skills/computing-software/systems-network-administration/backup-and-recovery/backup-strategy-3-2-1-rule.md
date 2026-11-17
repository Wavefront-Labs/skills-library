---
id: computing-software.systems-network-administration.backup-and-recovery.backup-strategy-3-2-1-rule
name: backup-strategy-3-2-1-rule
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup, backup-strategy, 3-2-1, 3-2-1-1-0, backup-copy, backup-copy-job, offsite-backup, independent-copy, failure-domain, backup-media, disk-repository, deduplication-appliance, object-storage, s3, s3-object-lock, azure-immutable-blob, tape, lto, worm, cloud-backup, saas-backup, microsoft-365-backup, shared-responsibility, raid-is-not-backup, sync-is-not-backup, snapshot-is-not-backup, capacity-planning, change-rate, seeding, bandwidth-math, veeam, restic, borg, rclone]
level: practitioner
status: draft
description: "Implement 3-2-1 for real: what counts as a copy, medium and off-site, independent failure domains, topology patterns, capacity and off-site bandwidth maths, SaaS data, and auditing an existing setup."
sources:
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
  - https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview
  - https://www.lto.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup strategy: the 3-2-1 rule — count copies by independent failure domains, not by files

**Goal:** turn "3 copies, 2 media, 1 off-site" (and the modern "+1 immutable/offline,
0 restore errors") into a concrete topology where no single event (disk failure, site
loss, admin mistake, ransomware with domain admin, cloud account loss) destroys every
copy. RPO/RTO tiers, ransomware hardening, GFS retention and drills are in
`computing-software.systems-network-administration.backup-and-recovery.backup-design-and-restore-drills`;
measuring recovery in `...backup-and-recovery.recovery-testing-and-rto-rpo-validation`.

## 1. What counts
| Thing | Counts as a backup copy? | Why |
|---|---|---|
| RAID, erasure coding | no | protects against disk failure only |
| Sync (OneDrive, Dropbox, rsync `--delete`) | no | deletions and encryption sync too |
| Replication / DR replica | no (it is an availability copy) | corruption replicates in seconds |
| Storage/VM snapshot on the same array | no, or at best a short-term local copy | dies with the array, deletable by the same admin |
| Versioned backup on separate storage | **yes** | point-in-time, separate system |
| Copy of that backup to another system/site | **yes** | |
"2 media" today means **two independent storage systems with different failure modes**
(e.g. a local disk repository and object storage or tape), not literally disk vs tape.
"Off-site" means outside the blast radius: a different building, region or provider, far
enough that one fire, flood or power event cannot reach both.

## 2. Independence checklist for each copy
For every pair of copies ask whether they share:
- the same **credentials/identity provider** (one compromised admin deletes both);
- the same **storage system or cloud account** (one account suspension or misconfig);
- the same **backup software catalogue/keys** (lose the server, lose the ability to read
  both; keep catalogue/config backups and encryption keys separately);
- the same **site, power or network**.
At least one copy must be immutable (object lock in compliance mode, WORM tape, hardened
repository) or physically offline.

## 3. Topology patterns
**A. Small office:** NAS or USB repository (fast local restores) → nightly encrypted copy to
cloud object storage with Object Lock (`restic` or `rclone` to S3-compatible storage;
check the provider supports Object Lock), plus monthly offline USB disk taken off-site.

**B. Mid-size, virtualised:** backup server writes to a hardened Linux repository on-site
(immutable for N days) → backup copy job to a second site or to object storage with
Object Lock → optional tape for long retention.

**C. Cloud-native:** native snapshots/backups in the workload account → cross-account,
cross-region copy into a dedicated backup account with a separate root of trust and
vault lock (e.g. AWS Backup Vault Lock, Azure immutable vault). The production account
must not be able to delete the copies.

**SaaS data (Microsoft 365, Google Workspace, Salesforce):** the provider keeps the
service running, not your history. Recycle bins and retention policies are not backups
against admin error or a malicious tenant admin. Use a third-party or provider backup
product writing outside the tenant.

## 4. Size it before you buy it
- **Capacity:** first full + (daily change rate × retention days) ÷ dedupe/compression
  ratio. Typical daily change is 2–5% for file servers and much higher for databases
  and VDI (measure yours from a week of incrementals).
  Example: 20 TB source, 3% change, 30 dailies, 2:1 reduction →
  (20 + 0.6 × 30) / 2 ≈ 19 TB, plus headroom for growth (≥ 30%) and immutability (data
  locked for N days cannot be freed early).
- **Off-site bandwidth:** daily changed data must cross the link inside the window.
  0.6 TB/day over 1 Gb/s at ~70% efficiency ≈ 2 h. The **initial seed** of 20 TB would take
  ~2.6 days at that rate; plan seeding by shipping disks or a provider import service.
- **Restore bandwidth** from off-site is the real test: downloading 20 TB from cloud
  storage may take days and incur egress fees. Know the number; it drives RTO.

## 5. Audit an existing setup against 3-2-1-1-0
For each protected system, fill one row: copies (where), media/system per copy, off-site
copy (where), immutable/offline copy (how), last verified restore date. Any row
without an off-site copy, an immutable copy or a restore in the last quarter is a gap
with an owner and a date. Systems nobody listed at all (SaaS, laptops, network device
configs, IaC state, password vaults, the backup server's own config) are the usual
biggest gaps.

## Verify
- [ ] Every system has ≥ 2 backup copies on independent systems, ≥ 1 off-site, ≥ 1 immutable/offline.
- [ ] No snapshot, RAID, replica or sync target is counted as a copy.
- [ ] Production admins cannot delete the immutable copy (tested with a delete attempt).
- [ ] Capacity and off-site bandwidth maths written down with real change rates.
- [ ] SaaS data and the backup system's own configuration/keys are covered.
- [ ] The audit table has no row with "last restore" older than a quarter.
