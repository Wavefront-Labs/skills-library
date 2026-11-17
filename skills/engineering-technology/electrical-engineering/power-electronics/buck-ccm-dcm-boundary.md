---
id: engineering-technology.electrical-engineering.power-electronics.buck-ccm-dcm-boundary
name: buck-ccm-dcm-boundary
category: engineering-technology
field: electrical-engineering
product: power-electronics
tags: [buck-ccm-dcm-boundary, buck-converter, ccm, critical-inductance, dcm, discontinuous-conduction, electrical-engineering, power-electronics]
level: practitioner
status: draft
description: "Find the CCM/DCM boundary of a buck converter, the critical inductance and load, and what changes in gain and control in DCM."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ti.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Buck converter CCM/DCM boundary

- **Ripple:** `dI = (Vin - Vo) D / (L f_sw)` with `D = Vo/Vin` in CCM.
- **Boundary:** the inductor current just reaches zero when average inductor current equals half the ripple: `Io,crit = dI/2 = Vo (1 - D) / (2 L f_sw)`.
- **Critical inductance for a minimum load:** `L_crit = Vo (1 - D) / (2 Io,min f_sw)`. Example: 12 V to 5 V (D = 0.417), 500 kHz, Io,min = 0.5 A: `L_crit = 5 x 0.583 / (2 x 0.5 x 500e3) = 5.8 uH`. Use L above `L_crit` to stay in CCM down to Io,min.
- **In DCM** the gain depends on load: `Vo/Vin = 2 / (1 + sqrt(1 + 4 K/D^2))` with `K = 2L/(R T_sw)` (ideal). Duty must shrink at light load; loop gain and compensation change (the LC double pole becomes a single pole), so a compensator tuned for CCM may be unstable or sluggish.
- **Design choice:** forced-CCM synchronous operation avoids mode changes at the cost of light-load efficiency; pulse-skipping/PFM modes accept DCM for efficiency.
- **Watch:** synchronous buck in DCM needs zero-current detection to prevent reverse inductor current.

**Verify:** observe the inductor current at minimum load; it should touch zero only when intended.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
