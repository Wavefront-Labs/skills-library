---
id: computing-software.systems-network-administration.syncthing.max-folder-concurrency
name: max-folder-concurrency
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, maxfolderconcurrency, scan-concurrency, waiting-to-scan]
level: advanced
status: docs-checked
description: "Limit how many Syncthing folders scan or sync at once with maxFolderConcurrency and read the waiting states."
sources: ["https://docs.syncthing.net/advanced/option-max-concurrency.html", "https://docs.syncthing.net/users/tuning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# maxFolderConcurrency

Controls how many folders may concurrently be in I/O-intensive operations such as syncing or scanning. Added in version 1.4.0.

## Values
- `0` (default): the number of logical CPUs in the system, autodetected.
- Negative: no limit on concurrent operations; this was the default before 1.4.0.
- A positive integer: that specific limit.

Folders waiting for their turn show as "Waiting to Scan" or "Waiting to Sync" until the number of ongoing operations is low enough to let them proceed.

## Choosing a value
The tuning guide says to take into account the inherent concurrency of the underlying storage:
- Two folders on the same spinning disk: syncing them concurrently is a strict loss of performance.
- Folders on a large array of disks: syncing many folders concurrently may be beneficial.
- Set to `1` to sync folders sequentially, reducing peak memory usage.

```xml
<options>
  <maxFolderConcurrency>2</maxFolderConcurrency>
</options>
```

## Related knobs
The folder settings `copiers`, `hashers` and `pullerMaxPendingKiB` tune work inside a folder. `maxConcurrentIncomingRequestKiB` is a global limiter (not per folder) on data being processed for incoming requests.

## Checked
2026-11-04. Read the maxFolderConcurrency page, Configuration Tuning and the config page element names: version, value meanings, waiting states, the spinning-disk, disk-array and set-to-1 advice, and the related settings. Removed the SSD and small-device advice and the "Observation" paragraph, which the pages do not state.
Method: documentation only; no commands were run.
