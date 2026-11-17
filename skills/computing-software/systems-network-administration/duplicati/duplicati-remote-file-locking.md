---
id: computing-software.systems-network-administration.duplicati.duplicati-remote-file-locking
name: duplicati-remote-file-locking
category: computing-software
field: systems-network-administration
product: duplicati
tags: [remote-file-locking, object-lock, worm, governance-mode, compliance-mode, set-locks, remote-file-lock-duration]
level: advanced
status: docs-checked
description: "Protect Duplicati backup files from deletion with provider object locking, choosing governance or compliance mode and applying locks to existing versions."
sources: ["https://docs.duplicati.com/detailed-descriptions/security-and-secrets/using-remote-file-locking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remote file locking (object lock) for Duplicati

Since Canary 2.2.0.103 Duplicati can ask a compatible provider to lock uploaded files (dblock, dindex and dlist) so they cannot be deleted, modified or overwritten for a period, even if backup credentials leak. The provider enforces the lock, so a compromised Duplicati machine cannot undo it. Uses: ransomware protection, legal hold and protection from accidental deletion.

Modes: Governance (unlocked) blocks deletion even with leaked credentials, but accounts with high-level permissions can bypass it; good for testing. Compliance (locked) lets nobody delete, even the root account, and the lock cannot be shortened; a 10-year lock means paying for storage for 10 years with no undo, so use with extreme caution.

Prerequisites: the provider and bucket must support object locking, often only enabled at bucket creation; AWS S3 and B2 need bucket versioning before locking. Supported: Amazon S3 and compatible such as IDrive e2, Backblaze B2, Azure Blob, Google Cloud Storage and Duplicati Storage with locking enabled.

Enable per backup with `--remote-file-lock-duration=30D` (units H, D, W, M). Test with governance and a short duration first. Mode options per provider: `--s3-lock-mode=governance|compliance`, `--b2-lock-mode`, `--azure-blob-immutability-policy-mode=unlocked|locked`, `--gcs-retention-policy-mode=unlocked|locked`. Google Cloud Storage also needs `--gcs-service-account-file` or `--gcs-service-account-json`, because the default OAuth flow cannot lock objects.

Existing backups: `duplicati-cli set-locks <storage-url> --remote-file-lock-duration=1M --version=0` locks the files of the most recent version. Locks changed on the server by hand can be synced back to the local database with the CLI.

## Checked

2026-11-04. Confirmed against the Using remote file locking page. Nothing removed.

Method: documentation only; no commands were run.
