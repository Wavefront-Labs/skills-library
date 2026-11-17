---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-cloud-storage-driver
name: bacula-cloud-storage-driver
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula-cloud, bacula, s3-backup, cloud-cache, bareos-droplet, object-storage-backup]
level: advanced
status: draft
description: "Back up Bacula volumes to S3-compatible object storage with the cloud driver: Cloud resource, cache and part sizes, upload and truncate policies, and bconsole cloud commands."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/New_Features_in_9_0_0.html
  - https://www.bacula.org/whitepapers/CloudBackup.pdf
  - https://docs.bareos.org/TasksAndConcepts/StorageBackends.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bacula cloud storage driver

**Goal:** Bacula volumes stored in S3 (or compatible) with a local cache, restorable without downloading whole volumes.

## How it works
Volumes are split into **parts** (`part.1`, `part.2` ...) in a local cache directory and uploaded as objects. Restore downloads only the parts it needs.

## SD config (bacula-sd.conf)
```
Cloud {
  Name = S3Cloud
  Driver = "S3"
  HostName = "s3.eu-west-2.amazonaws.com"
  BucketName = "acme-bacula"
  AccessKey = "AKIA..."
  SecretKey = "..."
  Protocol = HTTPS
  UriStyle = VirtualHost
  Region = "eu-west-2"
  Truncate Cache = AfterUpload
  Upload = EachPart
}
Device {
  Name = CloudDev1
  Device Type = Cloud
  Cloud = S3Cloud
  Archive Device = /var/lib/bacula/cloudcache
  Maximum Part Size = 100MB
  Media Type = CloudType
  LabelMedia = yes
  Random Access = yes
  AutomaticMount = yes
  RemovableMedia = no
  AlwaysOpen = no
}
```
Add a matching `Storage` in bacula-dir.conf (`Media Type = CloudType`). Newer Bacula versions also ship an `Amazon` driver using the AWS SDK/CLI; the S3 driver uses libs3.

## Policies
- `Upload = EachPart` (as parts fill), `AtEndOfJob`, or `Manual`.
- `Truncate Cache = AfterUpload`, `AtEndOfJob`, or `No` (keep local copy for fast restore).

## bconsole
```
cloud list storage=CloudStorage volume=Vol-0001
cloud upload storage=CloudStorage volume=Vol-0001
cloud truncate storage=CloudStorage volume=Vol-0001
```

## Bareos
Bareos uses the `droplet` backend (`Device Type = droplet`, profile file with host/keys/bucket) instead of the Bacula cloud driver.

## Gotchas
- Cache disk must hold at least the parts in flight for all concurrent jobs.
- Volume recycling deletes cloud parts; enable bucket versioning/Object Lock carefully or recycled parts accumulate cost.
- Keep the catalog backup off the same bucket credentials.

## Verify
`cloud list` shows parts uploaded, and a restore after `cloud truncate` pulls parts down successfully.
