---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.weed-backup-volume-mirror
name: weed-backup-volume-mirror
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [weed-backup, fs-meta-save, cluster-mirror, mirror, incremental]
level: advanced
status: docs-checked
description: "Back up volumes incrementally with weed backup -volumeId and build a cluster mirror by restoring volumes plus fs.meta.save metadata."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# weed backup volume mirror

Incremental volume backup from any machine with enough disk space:
```bash
weed backup -server=master:port -dir=. -volumeId=5
```
If the local volume does not exist it is created. Remote needle entries are compared with local ones and only the missing delta is fetched from the volume server. A non-existent `-volumeId` creates nothing locally, so a script can loop over a range of ids. It is a one-shot command, not a continuously running service.

Mirror a whole cluster:
1. Pause operations on the source (volumes and filer metadata are copied separately and must match).
2. Install SeaweedFS on the new cluster, ideally the same version; do not start its volume servers yet, so it does not create its own volumes.
3. Create the data directory on each backup volume server, mimicking the source layout (volume 1 from source volume server 1 goes to backup volume server 1), and run `weed backup` there with `-dir` pointing at it.
4. Save metadata on the source filer: `fs.meta.save -o=<dir>/<name>.meta` in `weed shell`, then copy the file to the backup filer machine (for example with scp).
5. Run `fs.meta.load <file>.meta` on the backup cluster's filer.
6. Start the backup volume servers with `-dir` set to the directory holding the backed-up volumes.

The page warns that this is not bullet-proof (tested on a few gigabytes), that transfer time depends on disk and network speed, and that the whole cluster must stop receiving writes during the copy.

Verify: run `volume.fsck` in `weed shell` and check that files load and are not corrupted.

## Checked
Checked 2026-11-09 against the SeaweedFS wiki page Data-Backup (read in full). Removed the unsupported pointer to `weed filer.backup` and `filer.sync` and the `fs.ls`/`fs.verify` verify step (the page uses `volume.fsck`).
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Data-Backup, read in full from a local clone of the wiki.
