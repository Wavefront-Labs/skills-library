---
id: engineering-technology.electrical-engineering.power-electronics.gate-drive-design
name: gate-drive-design
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [bootstrap-supply, dead-time, desaturation-protection, electrical-engineering, gate-charge, gate-drive-design, gate-driver, gate-resistor-selection, miller-clamp-and-desaturation, power-electronics]
level: advanced
status: draft
description: "Design MOSFET, IGBT and SiC gate drives: gate resistor, bootstrap supply, dead time, Miller clamp and desaturation protection."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ti.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Gate drive design

1. **Gate charge:** drive power `P = Qg Vgs f_sw`, average current `Iavg = Qg f_sw`; the driver peak current `Ipk = Vdrive/(Rg + Rdriver)`.
2. **Gate resistors:** separate turn-on and turn-off resistors (diode steering); larger turn-on Rg slows `di/dt` to limit overshoot and EMI, a smaller turn-off Rg speeds turn-off while the Miller clamp holds the gate.
3. **Bootstrap supply for high-side:** `Cboot >= Qg_total / dV_allowed` (about 10 to 20 times the gate charge); fast diode with rating above the bus; very low duty cycles or 100 percent on require an isolated supply.
4. **Negative gate drive:** needed for IGBTs and SiC (for example -4 to -5 V or per datasheet) to prevent parasitic turn-on from `dv/dt` through the Miller capacitance; or use an active Miller clamp.
5. **Desaturation protection (IGBT/SiC):** monitor Vce(sat) after blanking time; soft turn-off to avoid overshoot; fault output to the controller.
6. **Isolation:** reinforced isolation rating for line-connected sides; common-mode transient immunity (CMTI) above 100 V/ns for SiC.
7. **Layout:** gate loop as small as possible; Kelvin source connection.

**Verify:** capture Vgs and Vds with isolated probes at the worst corner; look for ringing and false turn-on.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
