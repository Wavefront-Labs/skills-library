---
id: computing-software.systems-network-administration.duplicati.duplicati-point-in-time-restore
name: duplicati-point-in-time-restore
category: computing-software
field: systems-network-administration
product: duplicati
tags: [remote-point-in-time, bucket-versioning, delete-marker, ransomware-recovery, read-only-destination]
level: advanced
status: draft
description: "Recover a Duplicati backup after remote files were deleted or damaged by reading a versioned bucket as it looked at an earlier time."
sources: ["https://docs.duplicati.com/detailed-descriptions/security-and-secrets/restoring-from-a-point-in-time"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Restoring a Duplicati backup from a point in time

If the destination keeps old versions of each object, Duplicati can read the destination as it was at an earlier moment, which helps after ransomware, leaked credentials or accidental deletion. This is separate from the backup versions Duplicati manages itself. It was introduced in Canary 2.4.0.105.

With bucket versioning on, the provider never really overwrites or deletes: uploading an existing name creates a new version, and deleting adds a delete marker over the earlier versions. The `--remote-point-in-time` option makes Duplicati list and download each file as it was at the given time, using the version current at that time and ignoring files deleted before it.

While the option is set, the destination is read-only: uploads, deletes, renames and locking are refused, so the old state cannot be changed while you restore.

Versioning alone does not stop someone with enough access from deleting old versions. Combine it with object locking (remote file locking) so versions cannot be removed until the lock expires. The page lists the supported destinations and their requirements in a table.
