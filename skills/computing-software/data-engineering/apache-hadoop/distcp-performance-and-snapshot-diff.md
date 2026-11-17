---
id: computing-software.data-engineering.apache-hadoop.distcp-performance-and-snapshot-diff
name: distcp-performance-and-snapshot-diff
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, distcp, snapshots, performance, bandwidth, incremental]
level: advanced
status: docs-checked
description: "Tuning and incremental DistCp: -m, -strategy dynamic, -bandwidth, listing threads, -blocksperchunk, plus -diff and -rdiff snapshot-based synchronisation and -filters."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-distcp/DistCp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DistCp performance and snapshot diffs

Parallelism and tuning:
- `-m <num_maps>`: maximum simultaneous copies; more maps do not necessarily improve throughput because files are the finest granularity. The page recommends tuning the map count to cluster sizes, copy size and bandwidth for long-running or regular jobs.
- `-strategy {dynamic|uniformsize}`: uniformsize (default) balances bytes per map; dynamic (DynamicInputFormat) splits files into sets, usually 2-3 times the number of maps, so faster maps take more chunks. The page says dynamic gives superior performance under most conditions.
- `-bandwidth`: MB/second per map; not exact, the map throttles so net bandwidth tends towards the value.
- `-numListstatusThreads`: threads for building the listing, at most 40. `-useiterator` uses a single-threaded listStatusIterator (saves client memory) and ignores `-numListstatusThreads`. For object stores the page suggests raising listing threads with `-update`, and `-direct` writes straight to the destination to avoid expensive rename of temporary files.
- `-blocksperchunk <n>`: files with more blocks are split into chunks of n blocks, copied in parallel and reassembled; default 0 (off); needs `getBlockLocations` on the source file system and `concat` on the target.
- `-copybuffersize`: default 8192 bytes.

Incremental sync with snapshots (both require `-update` and DistributedFileSystem at both ends):
- `hadoop distcp -update -diff <oldSnapshot> <newSnapshot> <src> <dst>`: both snapshots must exist on the source, the target must have a snapshot named `<oldSnapshot>` and must have no changes (create, rename, delete) since it. It copies, renames and deletes per the diff list. It does not create `<newSnapshot>` on the target. Re-running after success fails with a "DistCp sync failed" exception if the target changed. Deletes follow the diff without checking file contents, and a missing file to delete does not raise an error.
- `-rdiff <newSnapshot> <oldSnapshot>`: finds what changed on the target since `<oldSnapshot>`, reverses it and copies modified files from the source's `<oldSnapshot>`, making the target match `<oldSnapshot>`; both snapshots must be on the target, with no change since `<newSnapshot>`, and the source must have the same `<oldSnapshot>` content. Source and target may be the same path.
- Most cloud providers do not work well with sync; `-diff` and `-rdiff` are not supported on object stores.

Filtering: `-filters <file>` holds one java.util.regex pattern per line; matching paths are excluded.

`-xtrack <path>` saves information about missing source files (experimental, needs `-update`, incompatible with `-atomic`). `-filelimit` and `-sizelimit` are deprecated and ignored.

## Checked

Method: 2026-11-08 compared against the DistCp guide (apache/hadoop trunk markdown source, options table, sync section and map-sizing appendix). Option semantics match; the draft's unsupported "FAQ default 20" maps and "Verify" step were removed and sync preconditions, listing and object-store notes added.
