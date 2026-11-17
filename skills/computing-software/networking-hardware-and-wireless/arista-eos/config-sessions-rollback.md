---
id: computing-software.networking-hardware-and-wireless.arista-eos.config-sessions-rollback
name: config-sessions-rollback
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, config-session, configure-session, commit-timer, rollback]
level: practitioner
status: draft
description: "Use EOS configure session with commit timer, abort and show session-config diffs for safe, atomic changes."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuration sessions and commit timers
Goal: make a staged, reversible config change.

```
switch# configure session CHG1234
switch(config-s-CHG1234)# interface ethernet 3
switch(config-s-CHG1234-if-Et3)# description to-core
switch(config-s-CHG1234)# end
switch# show session-config named CHG1234 diffs
switch# configure session CHG1234 commit timer 00:05:00
switch# configure session CHG1234 commit
```

```
switch# configure session CHG1234 abort
switch# show configuration sessions
```

- Changes in a session are pending until commit; nothing touches the live config.
- `commit timer hh:mm:ss` auto-reverts unless a later `commit` confirms (like Junos commit confirmed).
- `rollback clean-config` and `configure replace` exist for whole-config replacement: confirm exact syntax on your release.

Gotcha: a session is validated at commit; if the running config changed meanwhile you may see `configuration changed` conflicts. Keep sessions short and do not leave stale sessions around.

Operational tip: name sessions after the change ticket, review `show session-config diffs` with a peer, and keep the commit timer short for remote changes. A timer expiring is the safe outcome, not a failure.

## Verify
- `show configuration sessions` shows the session as committed or completed; `show running-config` has the new line.
