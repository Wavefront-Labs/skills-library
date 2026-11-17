---
id: computing-software.cloud-infrastructure-engineering.harbor.garbage-collection
name: garbage-collection
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [garbage-collection, gc, dry-run, untagged-artifacts, harbor]
level: practitioner
status: docs-checked
description: "Run, schedule, dry-run and stop Harbor garbage collection, and understand the two hour upload window and the untagged-artifact option."
sources:
  - https://goharbor.io/docs/main/administration/garbage-collection/
  - https://goharbor.io/docs/main/administration/configure-project-quotas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deleting images in Harbor does not free space. Garbage collection removes blobs no longer referenced by a manifest from storage.

Run it under Administration, **Clean Up**, **Garbage Collection** tab:
- **Workers**: how many GC tasks run in parallel.
- **Allow garbage collection on untagged artifacts**: the next GC deletes untagged artifacts, then collects them.
- **DRY RUN**: prints blobs eligible for deletion and a rough estimate of freed space without removing data. The estimate is in the run logs.
- **GC Now**: runs immediately; limited to once per minute.

Schedule: None, Hourly (start of each hour), Daily (midnight), Weekly (midnight every Saturday) or Custom (`cron`). Set Workers and the untagged option, then **Save**.

Safety: a 2 hour window protects recently uploaded layers, so manifests and blobs with timestamps inside it are not swept. Harbor stays usable while GC runs.

The Garbage Collection History table lists Task ID, Trigger Type (Manual or Schedule), Dry Run, Status, Details, Creation Time, Update time and Logs. To stop runs, tick one or more Task IDs, click **Stop** and confirm. Stopping only prevents further processing; artifacts already collected are not restored.

Project quotas: during garbage collection Harbor frees the storage used by untagged blobs in the project.

## Checked

2026-11-03. Workers, untagged option, DRY RUN, GC Now once-per-minute limit, schedule options, the 2 hour window, History columns and the stop behaviour were read against the Harbor docs page Garbage Collection; the quota statement against Configure Project Quotas. Removed: the claim that tag retention interacts with GC (not on the page). The "estimate is in the run logs" wording matches the History Logs column.

Method: documentation only; no commands were run.
