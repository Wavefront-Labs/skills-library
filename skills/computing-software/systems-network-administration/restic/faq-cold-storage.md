---
id: computing-software.systems-network-administration.restic.faq-cold-storage
name: faq-cold-storage
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, faq, glacier, cold-storage, s3-restore, storage-class]
level: advanced
status: docs-checked
description: "Use S3 Glacier and Glacier Deep Archive with restic through the experimental s3-restore feature, with its restore flags and caveats."
sources:
  - https://restic.readthedocs.io/en/stable/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cold storage classes

Restic does not natively support cold storage. The FAQ describes experimental, alpha-stage support for S3 Glacier and S3 Glacier Deep Archive restores.

## Backup

```
restic backup -o s3.storage-class=GLACIER somedir/
```

## Restore

```
RESTIC_FEATURES=s3-restore restic restore \
  -o s3.enable-restore=1 -o s3.restore-days=7 -o s3.restore-timeout=24h latest
```

Adjust `s3.restore-timeout` if a restore needs longer than 24 hours.

## Caveats from the docs

- The feature is alpha: breaking changes are possible.
- Restores can take roughly 1 to 42 hours; raise `s3.restore-timeout` if they exceed 24 hours.
- Metadata files (config, locks, trees) are kept in the Standard class, so they stay readable.
- Commands known to work: `backup`, `copy`, `prune`, `restore`.

Because restores from cold storage are known to be time-consuming, rehearse a restore to learn the real delay for your storage class and provider.

## Checked

Checked 2026-11-08 against the restic FAQ page (faq), read in full. Confirmed: no native cold storage support, experimental S3 Glacier and Deep Archive restore, the backup and restore commands with s3.storage-class, s3.enable-restore, s3.restore-days, s3.restore-timeout and RESTIC_FEATURES=s3-restore, alpha status, 1 to 42 hour restores, metadata kept in the Standard class, and the commands known to work. Removed: check from the working-commands list, the thaw description, and the separate cold-repository planning advice, which the page does not state.

Method: documentation only; no commands were run.
