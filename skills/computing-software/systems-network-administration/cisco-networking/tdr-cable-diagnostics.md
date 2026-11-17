---
id: computing-software.systems-network-administration.cisco-networking.tdr-cable-diagnostics
name: tdr-cable-diagnostics
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, tdr, cable-diagnostics, test-cable-diagnostics, time-domain-reflectometer, open-pair, short-pair, cable-length, physical-layer-troubleshooting, interface-errors]
level: practitioner
status: draft
description: "Run the Catalyst built-in TDR on copper ports to find open, shorted or mis-wired pairs and their distance, read results correctly and know its accuracy limits."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-4500-series-switches/116158-trouble-tdr-00.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TDR cable diagnostics on Catalyst copper ports

Time Domain Reflectometry sends a pulse down each pair and times reflections. It finds the
type and rough distance of a fault without a handheld tester.

## Run it
```
test cable-diagnostics tdr interface Gi1/0/14
! wait 5-10 s
show cable-diagnostics tdr interface Gi1/0/14
```
Sample output:
```
Interface Speed Local pair Pair length        Remote pair Pair status
Gi1/0/14  auto  Pair A     41   +/- 5 meters  N/A         Open
                Pair B     42   +/- 5 meters  N/A         Open
                Pair C     0    +/- 5 meters  N/A         Short
                Pair D     42   +/- 5 meters  N/A         Open
```

## Read the status
| Status | Meaning |
|---|---|
| Normal | pair terminated correctly (link usually up) |
| Open | no termination at that distance: unplugged far end, cut cable, or the far device is off |
| Short | conductors touching at that distance (crushed cable, bad punch-down) |
| Impedance mismatch | bad joint, wrong cable type, kinks |
| Not completed / N/A | test failed or unsupported on this port/speed |

- With nothing plugged in at the far end, every pair shows **Open** at the full length: a
  handy way to measure a run.
- One pair Open at a shorter distance than the others = a break or bad termination at that point.
- 100 Mb links use only pairs A and B; a damaged C/D pair passes traffic at 100 Mb but stops
  gigabit (link negotiates down to 100 or flaps).

## Gotchas
- The test is **disruptive**: the link drops for a few seconds. Do it in a window or on a
  dead port.
- Accuracy is about +/- 5 m (some platforms +/- 2 m); not useful under ~5 m.
- Not supported on all ports (e.g. some mGig or PoE configurations, uplink SFPs); fibre needs
  DOM/OTDR instead.
- On PoE ports the powered device reboots during the test.

## Verify
- [ ] After re-termination, all four pairs show Normal (or Open at equal full lengths with the
  far end unplugged).
- [ ] Link comes up at the expected speed (`show interfaces status`).
