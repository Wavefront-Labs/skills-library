---
id: computing-software.systems-network-administration.cisco-networking.err-disabled-recovery
name: err-disabled-recovery
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, catalyst, err-disabled, errdisable-recovery, errdisable-detect, bpduguard, psecure-violation, link-flap, udld, channel-misconfig, arp-inspection, dhcp-rate-limit, show-interfaces-status-err-disabled, interface-errors]
level: practitioner
status: draft
description: "Handle err-disabled Catalyst ports: find the cause, fix it before re-enabling, configure errdisable recovery per cause and avoid auto-recovery masking real loops."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/69980-errdisable-recovery.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# err-disabled ports and errdisable recovery

A switch puts a port in `err-disabled` (LED amber/off, `show int status` says `err-disabled`)
when a protection feature trips. The port stays down until you bounce it or recovery fires.

## Find the cause
```
show interfaces status err-disabled         ! port + reason column
show errdisable recovery                     ! which causes auto-recover, timer, time left
show logging | i ERR_DISABLE|PSECURE|BPDUGUARD|LINK_FLAP|UDLD
show errdisable detect
```
Common reasons and what to fix:
| Reason | Trigger | Fix before re-enabling |
|---|---|---|
| bpduguard | BPDU received on PortFast edge port | a switch/bridge was plugged into an access port; remove it |
| psecure-violation | too many / wrong MACs (port security) | dock/phone/hub behind the port; adjust maximum or `clear port-security sticky` |
| link-flap | > 5 flaps in 10 s | bad cable/optic, NIC power-saving |
| udld | unidirectional fibre link | one strand broken or swapped TX/RX |
| channel-misconfig | EtherChannel guard: peer not bundled | match LACP/channel config both ends |
| arp-inspection | DAI rate limit exceeded (15 pps default) | raise `ip arp inspection limit rate` on trunks/servers |
| dhcp-rate-limit | DHCP snooping rate limit exceeded | raise `ip dhcp snooping limit rate` on uplinks |
| gbic-invalid | unsupported SFP | use a supported optic (or `service unsupported-transceiver`, unsupported by TAC) |

## Re-enable manually
```
interface Gi1/0/12
 shutdown
 no shutdown
```
For port security also `clear port-security sticky interface Gi1/0/12` if the old MAC is stuck.

## Automatic recovery
```
errdisable recovery cause bpduguard
errdisable recovery cause psecure-violation
errdisable recovery cause link-flap
errdisable recovery interval 300        ! seconds, default 300, minimum 30
```
Enable it for causes where a human cannot respond quickly (user-facing ports) but keep the
interval long. Auto-recovery on bpduguard means a looping device re-triggers every 5 minutes:
alert on the syslog message so someone actually removes it.

## Gotchas
- Some causes can be turned off: `no errdisable detect cause link-flap`. Prefer fixing the
  cause; disabling detection on loop-related causes invites outages.
- On IOS XE, `shutdown/no shutdown` on a Port-channel does not recover err-disabled members;
  bounce the members.
- psecure `violation restrict` or `protect` modes do not err-disable; they drop silently
  (restrict logs and counts).

## Verify
- [ ] `show interfaces status err-disabled` is empty.
- [ ] `show errdisable recovery` lists only the causes you intended, with your interval.
- [ ] Syslog alert exists for `%PM-4-ERR_DISABLE`.
