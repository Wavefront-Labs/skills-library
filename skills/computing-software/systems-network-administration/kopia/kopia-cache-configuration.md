---
id: computing-software.systems-network-administration.kopia.kopia-cache-configuration
name: kopia-cache-configuration
category: computing-software
field: systems-network-administration
product: kopia
tags: [cache, cache-directory, content-cache, metadata-cache, blob-list, cache-set]
level: advanced
status: docs-checked
description: "Locate and size Kopia's local caches and know what each cache type holds."
sources: ["https://kopia.io/docs/advanced/caching/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default cache directory: `~/.cache/kopia/{unique-id}` on Linux, `~/Library/Caches/kopia/{unique-id}` on macOS, and under the local app data folder in a `kopia` directory on Windows. The unique ID is derived from the config file and repository. Override with `--cache-directory` at connect time (stored in the config file) or `KOPIA_CACHE_DIRECTORY`, which takes precedence over the stored value.

## Cache types

- `metadata` (encrypted): directory listings, manifests and other data from `q` blobs; each entry is a whole q blob, usually about 20 MB.
- `contents` (encrypted): sections of `p` blobs.
- `indexes` (unencrypted): content-to-blob mapping in a memory-mappable format.
- `own-writes` (unencrypted): names and timestamps of index blobs this client wrote, so it sees its own writes even when listing is eventually consistent.
- `blob-list` (unencrypted): short-lived listing cache, 30 seconds by default.
- `server-contents` (encrypted locally): contents downloaded from a repository server.

## Setting parameters

```console
kopia cache set --content-cache-size-mb=20000 --cache-directory=/var/my-cache
kopia cache set --max-list-cache-duration=300s
```

Cache sizes are soft limits: the cache is swept every few minutes to bring it back under the configured size, so it can briefly exceed it. When troubleshooting corruption, do not clear the cache on the machine where the problem appeared, because it may contain data that helps recovery.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Caching (default directories, KOPIA_CACHE_DIRECTORY precedence, cache types, 30 second blob-list default, cache set examples, soft limits swept every few minutes) and Consistency (do not clear the cache on the affected machine).
Method: documentation only; no commands were run.
