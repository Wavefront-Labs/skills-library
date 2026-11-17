---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-key-accept-reject-delete
name: salt-key-accept-reject-delete
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-key, keys, accept, reject, delete, aes, minion-keys]
level: intro
status: docs-checked
description: "Manage minion keys with salt-key: list by state, accept, reject and delete with globs, --include-all, and the AES key regeneration side effect."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/cli/salt-key.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt-key: list, accept, reject, delete

List: `-l`/`--list ARG` where ARG is `pre`/`un`/`unaccepted`, `acc`/`accepted`, `rej`/`rejected`, or `all`. (`-L` is deprecated for `--list all`.) Print keys with `-p` (one) and `-P` (all).

Accept:
- `-a <key>` (globs allowed); add `--include-all` to also match rejected keys.
- `-A` accepts all pending keys.

Reject:
- `-r <key>`; `--include-all` also matches accepted keys. `-R` rejects all pending.

Delete: `-d <key>` (globs), `-D` all.

Notes:
- To change a key's state, delete it first, then accept or reject.
- Reject and delete make the master generate a new AES key so connected minions re-authenticate; mass operations can hurt master performance.
- `--rotate-aes-key False` skips that refresh, but lowers security (default True).
- `-y` answers yes to prompts.

## Checked

2026-11-04: read the salt-key CLI reference page in full. Confirmed the list arguments, -L deprecation, accept, reject, delete and print options, --include-all, the delete-then-change-state rule, the AES key regeneration warnings and --rotate-aes-key. Nothing removed.

Method: documentation only; no commands were run.

