---
id: computing-software.systems-network-administration.kopia.kopia-consistency-verify-and-repair
name: kopia-consistency-verify-and-repair
category: computing-software
field: systems-network-administration
product: kopia
tags: [verify, snapshot-verify, corruption, repair, bit-rot, clock-skew]
level: advanced
status: docs-checked
description: "Verify Kopia snapshots with snapshot verify and file percent checks, and recover from repository corruption."
sources: ["https://kopia.io/docs/advanced/consistency/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A real restore is the gold standard. When that is impractical use `kopia snapshot verify`, which walks snapshots from their roots to confirm the directory structure is consistent and all required blobs exist. It runs automatically during every daily full maintenance, but it does not download, decrypt or decompress blobs, so it will not detect bit rot.

To test the data itself add `--verify-files-percent`:

```console
kopia snapshot verify --verify-files-percent=100 --file-parallelism=10
kopia snapshot verify --verify-files-percent=1
```

A percent value downloads a random sample, which is a cheaper compromise when egress is expensive. This option is CLI only; KopiaUI cannot run it.

## Why corruption happens

- Unsupported or misconfigured filesystems. Kopia needs POSIX semantics, atomic writes, strong read-after-write and eventual list-after-write consistency. Prefer a mature local filesystem or a supported cloud repository over emulated, layered or networked ones.
- Silent corruption after write (bit rot). ZFS or Btrfs detect and recover from it, and RAID alone does not protect against it. Kopia can do little about detected filesystem corruption, so use the most reliable filesystem or cloud storage.
- Large clock skew. A few minutes is tolerated, more can lead Kopia to delete its own data. Keep clients and storage time synchronized.

## Repair tips

1. Remove zero-size repository files; Kopia never writes them.
2. Try opening the repository from another computer; if that works, the local cache may be corrupted and clearing it may fix the issue. Do not clear the cache on the main computer where the corruption appeared, because the cache may help recovery.
3. Remove files with odd timestamps such as 1970 or 2038.
4. If maintenance has not run yet, stash the most recently written `x` index files one by one in reverse timestamp order to roll the repository back to an earlier state.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Consistency page (snapshot verify behaviour, daily full maintenance, --verify-files-percent, CLI-only, three corruption causes, repair tips). Removed or corrected: the Reed-Solomon / v0.12.0 sentence (not on the page) and the invented 'copy the cache first' advice, replaced with the page's wording.
Method: documentation only; no commands were run.
