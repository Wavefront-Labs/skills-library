---
id: computing-software.systems-network-administration.network-design.loopback-plugs-and-loopback-tests
name: loopback-plugs-and-loopback-tests
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-physical, loopback-plug, loopback-test, serial-loopback, fiber-loopback]
level: practitioner
status: draft
description: "Isolate physical faults with loopback plugs and tests: RJ45 and fibre loopbacks on ports, carrier loopback requests on circuits, and reading the results."
sources:
  - https://www.cisco.com/c/en/us/support/docs/wan/t1-e1-t3-e3/10215-ext-loopback.html
  - https://www.fluke.com/en-us/learn/blog/fiber-optics/fiber-loopback-testing
  - https://www.comptia.org/certifications/network
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loopback plugs and loopback tests

## What a loopback proves
Transmit is wired back to receive. If a port comes up/passes traffic with a loopback plug, the port,
optic and its transmit/receive path are good; the fault lies beyond (cable, far end, provider).

## Types
| Type | How |
|---|---|
| RJ45 Ethernet loopback | pins 1-3 and 2-6 bridged; tests NIC/switch port (link LED); some switches err-disable on loop detection (keepalive), which itself proves loop |
| Fibre loopback | short patch connecting Tx to Rx on the same optic/panel port (with attenuator for long-reach optics to avoid saturating Rx) |
| Serial / T1/E1 loopback | hardware plug or provider-initiated line/payload loopback on the CSU/DSU or NTU |
| Software loopback | IOS `loopback` interface (logical, not a test); `loopback line`/`loopback local` on serial/controller interfaces |

## Circuit testing
Ask the carrier to loop the NTU/smartjack toward you: if your router sees its own packets/keepalives
(serial shows "looped"), your side to the demarc is good. Progressive loops (local, demarc, far end)
isolate the segment. Ethernet services: Y.1731/802.1ag loopback (LBM/LBR) or RFC 2544/Y.1564 tests
via provider NIDs.

## Procedure
1. Loop the device port directly: port good?
2. Loop at the patch panel or far end of the cable: cable good?
3. Ask for a carrier loop at the demarc and progressively farther.

Remove loops afterwards; leaving a loop in a production switch can cause a broadcast storm if loop
protection is off.

## Verify
- [ ] Test record lists each loop point and result, identifying the segment at fault.
