---
id: computing-software.systems-network-administration.kopia.kopia-sharding-and-storage-layout
name: kopia-sharding-and-storage-layout
category: computing-software
field: systems-network-administration
product: kopia
tags: [sharding, blob-types, repository-layout, filesystem-repository]
level: advanced
status: docs-checked
description: "Kopia repository blob prefixes and the sharding feature that customizes the on-disk directory structure."
sources: ["https://kopia.io/docs/advanced/sharding/", "https://kopia.io/docs/advanced/storage-tiers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Repository storage is a set of blobs named by prefix. The prefixes documented with storage classes are:

- `p`: the bulk of snapshot data, mostly written once and read only during compaction in full maintenance or when you test snapshots.
- `q`: snapshot metadata (directory listings, manifests), frequently read and written.
- `n`, `m`, `l`, `x`: indexes, frequently read, written and deleted.
- `s`: sessions, frequently read, written and deleted.

Sharding, introduced in v0.9.0, lets you customize the filesystem layout of a repository. A sharded filesystem repository holds a `.shards` file and `kopia.maintenance.f`, and blobs are placed into nested directories such as `p00/003/` or `n4e/ad3/` so that no single directory holds too many files; the page cites hundreds of thousands of data files in repositories over 1 TB. Small repositories may not need sharding. Blob files carry the `.f` extension in this layout.

The layout is controlled by a `.shards` JSON file in the repository: `default` is an array of directory-name lengths (`[2, 3]` splits the first 5 characters of the blob hash into two directory levels), `maxNonShardedLength` leaves shorter hashes unsharded, and `overrides` set `shards` per blob `prefix`. Change it with `kopia blob shards modify --default-shards=0 --i-am-sure-kopia-is-not-running --path=<repo_root>` (`0` turns sharding off). Some `repository sync-to` subcommands accept `--flat` to make the destination unsharded, which suits cloud storage.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Sharding page (v0.9.0, on-disk layout, .shards fields, blob shards modify, --flat) and Storage Tiers page (blob prefix descriptions). Removed or corrected: the closing paragraph about small writes to q and index blobs, which no page states.
Method: documentation only; no commands were run.
