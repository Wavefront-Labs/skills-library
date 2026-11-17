---
id: computing-software.networking-hardware-and-wireless.juniper-junos.commit-confirmed
name: commit-confirmed
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, commit-confirmed, auto-rollback, safe-change]
level: practitioner
status: draft
description: "Use commit confirmed so a remote change automatically rolls back if you lose access, then confirm with a plain commit."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# commit confirmed for safe remote changes
Goal: make risky changes (interfaces, routing, firewall filters) over SSH without locking yourself out.

```
user@host# commit confirmed 5
commit confirmed will be automatically rolled back in 5 minutes unless confirmed
commit complete
# verify you can still reach the box, then:
user@host# commit
commit complete
```

- The argument is minutes (1-65535, default 10).
- If no confirming `commit` arrives, Junos rolls back to the previous configuration and logs it.
- `commit confirmed 5` can be extended by issuing another `commit confirmed` before the timer expires.
- `commit check` first; `commit confirmed` is not a substitute for validation.

Gotcha: the rollback restores configuration, not state you changed operationally (cleared sessions, software upgrades, `request` actions). If your SSH session dies, wait for the timer; do not start a second configure session and commit, which would confirm the change.

## Verify
- `show system commit` shows a `commit confirmed` entry, then a rollback entry if it timed out.
- `show system rollback compare 0 1` is empty after you confirm.
