---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.occlusion-detection
name: occlusion-detection
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [occlusion-detection, infusion-pump, iec-60601-2-24, pressure-sensing, bolus-on-release, time-to-alarm, downstream-occlusion]
level: advanced
status: draft
description: "Design infusion pump occlusion detection: pressure and force sensing, thresholds, time-to-alarm at low rates, bolus on release and IEC 60601-2-24 tests."
sources: ["IEC 60601-2-24 Particular requirements for the basic safety and essential performance of infusion pumps and controllers (confirm edition)", "FDA infusion pump guidance (current text on fda.gov)", "Infusion pump engineering literature and manufacturer technical papers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Occlusion detection in infusion pumps

**Goal:** detect a blocked line quickly enough to limit under-delivery and avoid a harmful bolus when the block is cleared.

Safety-critical; limits and test methods come from IEC 60601-2-24 and the regulator (confirm editions and local guidance).

## Sensing approaches
- **Downstream pressure** via a force or pressure sensor against the tubing or a diaphragm in the cassette.
- **Motor current or torque** as an indirect proxy in syringe and peristaltic drives.
- **Upstream occlusion** (empty container, closed clamp) detected by a sensor on the inlet side or pressure drop.

## Design parameters
1. **Alarm threshold:** user-selectable or fixed pressure; a low threshold alarms early and may nuisance-alarm with normal viscous or small-bore lines, a high threshold delays alarms and stores more pressure (and so more bolus).
2. **Time to alarm:** at a low flow rate (for example 1 mL/h), the time to build pressure to threshold may be long, so the standard requires reporting the time to alarm at specified rates and thresholds.
3. **Bolus on release:** the elastic volume stored in tubing and syringe at alarm pressure is released when the blockage clears. The design limits it by a retraction step (backing off the plunger), by lower thresholds, by stiffer sets or by pressure-limited drive.
4. **Compliance** of the syringe, tubing and pump mechanism sets pressure-volume behaviour; characterise it.

## Test method
- Set rate and threshold, block the line, and record the time and pressure at alarm and the bolus on release; repeat at several rates, for several sets (and for syringe sizes in syringe pumps).
- Trumpet curves and start-up tests are used in the standard to show flow accuracy (see infusion-flow-accuracy-testing).

## Verify
- [ ] Time-to-alarm and bolus volume documented and within the risk file limits.
- [ ] Sensor failure and drift detected by diagnostics.
- [ ] Alarm priority and signals follow the alarm standard (see alarm-priority-and-signals).
