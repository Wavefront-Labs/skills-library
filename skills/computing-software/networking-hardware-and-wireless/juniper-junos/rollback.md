---
id: computing-software.networking-hardware-and-wireless.juniper-junos.rollback
name: rollback
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, rollback, rollback-compare, load-override, saved-configs]
level: practitioner
status: draft
description: "Roll back to previous Junos commits, compare versions, and save or load full configuration files."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rolling back and saving configurations
Goal: revert a bad change fast and keep known-good copies.

```
user@host# rollback ?
user@host# show | compare rollback 3
user@host# rollback 1
user@host# commit
user@host# save /var/tmp/known-good.conf
user@host# load override /var/tmp/known-good.conf
user@host# commit check
```

- `rollback 0` discards uncommitted candidate changes; `rollback N` loads the Nth previous commit into the candidate (you must still commit).
- `rollback rescue` after `request system configuration rescue save` loads the rescue config, a last-resort known-good.
- `load override` replaces the whole candidate; `load merge` merges; `load replace` uses `replace:` tags.

Gotcha: rollback only loads the candidate; the box is unchanged until `commit`. Also, `load override` of a file made on another device brings its hostname, addresses and keys, so review `show | compare` before committing.

Operational tip: `show system commit` lists the index numbers, and `show system rollback compare 0 3` previews a rollback without touching the candidate. Keep a copy of the known-good file off-box before major work.

## Verify
- `show | compare` is empty after `rollback 0`.
- `file list /config/ detail` shows the rescue and juniper.conf.N.gz files.
