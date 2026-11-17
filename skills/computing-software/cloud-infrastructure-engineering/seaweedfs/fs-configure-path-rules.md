---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.fs-configure-path-rules
name: fs-configure-path-rules
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [fs-configure, filer-conf, locationprefix]
level: practitioner
status: docs-checked
description: "Set per-path collection, replication, TTL, disk type and rack rules with fs.configure, stored in /etc/seaweedfs/filer.conf and reloaded by all filers."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Path-Specific-Configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# fs configure path rules

Rules live in the special file `/etc/seaweedfs/filer.conf`, stored inside SeaweedFS (not on the host disk), so replicated filers share it. Filers reload it on change.

In `weed shell`:
```
> fs.configure                                             # show current
> fs.configure -locationPrefix=/tests/ -collection=special          # preview
> fs.configure -locationPrefix=/tests/ -collection=special -apply   # save
> fs.configure -locationPrefix=/tests/ -delete -apply
```
Without `-apply` it only prints the result.

Configurable per prefix: disk type (`hdd`, `ssd` or a tag), fsync, volume growth count, collection, replication, TTL, data center, rack, data node; also `-readOnly` (disable writes) and `-worm` (written files become read-only). See `fs.configure -h`.

Use cases: a `/scratch/` directory where everything written gets a 7-day TTL (such as CI build artifacts), or a system-wide trash directory with a TTL.

Options apply at write time: a file created elsewhere and then moved into the configured path does not pick them up. You can also write `/etc/seaweedfs/filer.conf` directly.

Verify: re-run `fs.configure` and check the `locations` array; write a file under the prefix and see it land in the configured collection.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Path-Specific Configuration (raw markdown, read in full). Claims about S3 bucket volume growth and bucket quota use were removed as unconfirmed.
