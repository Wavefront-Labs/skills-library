---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.temperature-setpoints-and-integration
name: temperature-setpoints-and-integration
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, temperature-integration, climate-setpoints, dif, heating-setpoint, cooling-setpoint, deadband, climate-computer, climate-control]
level: practitioner
status: draft
description: "Set greenhouse temperature setpoints and use temperature integration: day and night values, deadband, DIF, ramping, energy savings and crop response limits."
sources:
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Temperature setpoints and integration

**Goal:** a temperature strategy that grows the crop on time at the lowest energy and without disease.

## Setpoints
- Heating setpoint: the temperature below which the heating starts. Cooling (vent) setpoint is a few degrees above, giving a deadband in which neither heating nor ventilation runs; a narrow deadband wastes energy by heating and venting in quick succession.
- Day and night values differ by crop and by light level; raise the setpoint when sunny (more photosynthesis) and lower when dull.
- Crop recommendations come from the crop growth guide or the variety breeder; they are the base values.

## Temperature integration
Plant development depends largely on the average temperature over a period (24 hours or several days), not on the instantaneous value. Temperature integration lets the temperature float (lower in cold periods, higher in sunny periods using free solar heat) so long as the average over the integration window is on target, saving heating energy. Limits: minimum and maximum temperatures set by the crop and disease risk, and not letting the average slip when the crop is in a sensitive stage. The control computer will ramp the setpoint to catch up.

## DIF
DIF is the day minus night temperature difference; a negative DIF shortens stems in many ornamentals, a positive DIF lengthens them. Use for height control as a supplement to or in place of chemical growth regulators; effect varies with the species.

## Practice
- Avoid sudden drops of temperature around dawn that cause condensation on the crop and disease risk (use a short morning heating pulse or ventilation); coordinate with humidity (`humidity-control-and-vapour-pressure-deficit`).
- Ramp setpoints gradually; sensors must be representative (`aspirated-sensor-placement-and-calibration`).

## Verify
- [ ] Logged 24 h average temperature versus the target.
- [ ] Heating energy use before and after introducing integration.
- Unconfirmed: crop-specific limits.
