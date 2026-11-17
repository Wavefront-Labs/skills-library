---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.battery-equivalent-circuit-in-simulink
name: battery-equivalent-circuit-in-simulink
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [battery-ecm-simulink, equivalent-circuit-model, battery-model, ocv-soc, rc-pair, simulink]
level: practitioner
status: gated
description: "Implement a first- or second-order RC equivalent-circuit battery model in Simulink with OCV-SOC, temperature-dependent R, and cell-to-pack scaling."
sources:
  - "Plett, Battery Management Systems Vol. 1"
  - "Simscape Battery: Battery block (https://www.mathworks.com/help/simscape-battery/ref/battery.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Battery equivalent-circuit model

1. Terminal voltage: `V = OCV(SOC,T) - I*R0 - V1 - V2`; each RC: `dV1/dt = -V1/(R1*C1) + I/C1` (I positive on discharge).
2. SOC: `dSOC/dt = -eta*I/(3600*Q)` (Q in Ah, eta ~ 1 on discharge, slightly < 1 on charge; textbook value (gated: unconfirmed, source is paywalled or blocked)).
3. Parameters from pulse tests (HPPC-style): R0 from the instantaneous voltage step, RC pairs from the relaxation. Tabulate vs SOC and T. The HPPC procedure itself is defined in the INL/USABC test manuals; confirm there (gated: unconfirmed, source is paywalled or blocked).
4. Scale to pack: Ns cells in series, Np in parallel: `Vpack = Ns*V`, `Ipack = Np*Icell`.
5. Add current, voltage and power limits as outputs for the supervisory controller.
6. Use the Simscape Battery `Battery` block if licensed (its Charge dynamics parameter offers one to five parallel RC sections, each with a polarization resistance and a time constant); custom is fine for BMS algorithm work.

**Gotchas:** sign convention; hysteresis in OCV (LFP) breaks pure OCV-SOC lookups.

## Verify
- [ ] Constant-current discharge tracks the test curve in voltage within tens of mV mid-SOC.
- [ ] Rest after a pulse relaxes with the fitted time constants.
