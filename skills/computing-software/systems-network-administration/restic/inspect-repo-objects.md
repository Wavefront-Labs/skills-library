---
id: computing-software.systems-network-administration.restic.inspect-repo-objects
name: inspect-repo-objects
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, cat, list, repository-objects, masterkey, snapshots, debugging]
level: advanced
status: draft
description: "Inspect restic internals with restic list and restic cat: object types, IDs, snapshot JSON, trees, blobs, indexes, keys, locks and packs."
sources:
  - https://restic.readthedocs.io/en/stable/
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inspecting repository objects

## list (plural types)

```
restic -r /srv/restic-repo list snapshots
restic list blobs
restic list packs latest
```

Types: `blobs`, `index`, `keys`, `locks`, `packs`, `packs [snapshot ID]`, `snapshots`. `list blobs` prints `blob-type blob-ID`, where type is `data` or `tree`. Use `-q` to suppress extra messages.

## cat (singular types)

```
restic cat config
restic cat snapshot <ID>
restic cat tree latest:/path/in/snapshot
restic cat blob <ID>
restic cat index <ID>
restic cat key <ID>
restic cat lock <ID>
restic cat pack <ID>
restic cat masterkey
```

- `config` prints the version and chunker polynomial; `masterkey` prints the Base64 master keys (treat as secret).
- `snapshot` prints JSON metadata; an ID prefix is enough.
- `tree snapshot[:subfolder]` prints JSON for the root or subfolder.
- `blob` prints raw decrypted content, `pack` the raw pack and warns if its hash mismatches.
- `key` shows created time, user, host and KDF data; `lock` shows time, exclusive flag, host and PID.

JSON-printing types pair well with `jq`; check blob hashes with `sha256sum`. Errors still go to stderr.
