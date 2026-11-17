---
id: computing-software.systems-network-administration.cisco-networking.safe-remote-change-reload-in
name: safe-remote-change-reload-in
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, reload-in, reload-cancel, safe-remote-change, revert-timer, configure-confirm, lockout-prevention, change-window, ios-cli]
level: practitioner
status: draft
description: "Make risky remote changes on Cisco gear without driving to site: reload in / reload cancel, configure revert timers, ordering ACL and routing edits, and what each net cannot save."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/command/fundamentals-cr-book/fundamentals-r1.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/config-mgmt/configuration/xe-16/config-mgmt-xe-16-book/cm-config-rollback-confirmed-change.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe remote changes: reload in and revert timers

Any change that can cut your own SSH session (ACLs on the management path, routing, VLAN or
trunk edits on the uplink, AAA) gets a dead-man switch first.

## Option A: reload in (works everywhere)
```
write memory                 ! startup-config = known good
reload in 10                 ! schedule; answer 'no' if asked to save
configure terminal
 ... risky change ...
end
! still connected and verified?
reload cancel
write memory
```
- `show reload` shows the pending reload.
- If you lose access, the device reloads into the saved (old) config in 10 minutes.
- Do **not** `write memory` before you verify: that saves the breaking change and the reload
  brings it back.

## Option B: configure revert (no reload, faster)
Needs `archive` with a `path` (see config-archive-and-configure-replace).
```
configure terminal revert timer 5
 ... change ...
end
configure confirm            ! keep it
```
If you do not confirm, IOS rolls back with configure replace after 5 minutes. No outage
from a reload, but it cannot undo things outside the config (crypto keys, VLAN database on
older switches, files).

## Order changes so you never cut yourself off
- ACL on VTY or management interface: add the new permit lines **before** binding, use
  sequence numbers (`ip access-list extended MGMT` then `5 permit tcp host <JUMP> any eq 22`).
- Replacing an interface ACL: build ACL v2, then swap in one line (`ip access-group MGMT-V2 in`).
- Changing the management IP: add the new address as secondary or on a second SVI first.
- Trunk allowed list: always `switchport trunk allowed vlan add|remove`, never the bare form
  that replaces the whole list.

## Gotchas
- `reload in` on a stack reloads every member; on a core switch that is a full outage, so
  prefer revert timers there.
- Some platforms ask "System configuration has been modified. Save?" when scheduling; answering
  yes defeats the purpose.
- Commands pasted in one block execute line by line; the line that cuts you off stops the
  rest of the paste, leaving a half-applied change for the timer to undo.

## Verify
- [ ] `show reload` shows nothing scheduled after the change.
- [ ] `show archive` shows the confirmed config; no pending revert (`show archive config rollback timer`).
- [ ] A fresh SSH session from the jump host works before you close the old one.
