---
id: computing-software.systems-network-administration.keepalived.build-prefix-versioning
name: build-prefix-versioning
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, building, prefix, symlink, multiple-versions, uninstall]
level: practitioner
status: docs-checked
description: "Use ./configure --prefix with a per-version directory so several Keepalived builds coexist, uninstall is a directory delete, and a symlink picks the active one."
sources:
  - https://keepalived.readthedocs.io/en/latest/installing_keepalived.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-version install prefix

The install page recommends setting a prefix so each version lives in its own directory:
```
./configure --prefix=/usr/local/keepalived-1.2.15
```
Benefits it lists:
- Uninstalling is deleting that directory.
- Several versions coexist without overwriting each other.
- A symlink in /usr/local (for example `keepalived` pointing to `keepalived-1.2.15`) selects the active version; switch versions by repointing it.

Then run make and make install as usual.

Verify: the binary under the prefix runs, and the symlink target matches the version you intend to be active.

## Checked

2026-11-04. Confirmed the prefix recommendation, its three benefits and the symlink layout example on the Installing Keepalived page. Nothing removed.

Method: documentation only; no commands were run.
