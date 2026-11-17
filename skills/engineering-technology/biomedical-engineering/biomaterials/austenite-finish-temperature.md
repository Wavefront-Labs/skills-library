---
id: engineering-technology.biomedical-engineering.biomaterials.austenite-finish-temperature
name: austenite-finish-temperature
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [austenite-finish, nitinol, shape-memory-alloy, af-temperature, dsc, bend-and-free-recovery, astm-f2004, astm-f2082, astm-f2063]
level: advanced
status: draft
description: "Control and measure nitinol transformation temperatures: Ms Mf As Af, DSC and bend-and-free-recovery methods, Ni content sensitivity and how Af sets superelastic behaviour."
sources: ["ASTM F2063 Standard specification for wrought nickel-titanium shape memory alloys for medical devices and surgical implants (confirm edition)", "ASTM F2004 Test method for transformation temperature of nickel-titanium alloys by thermal analysis", "ASTM F2082 Test method for determination of transformation temperature by bend and free recovery"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Austenite finish temperature (Af) of nitinol

**Goal:** set and verify the transformation temperature that gives the intended superelastic or shape-memory behaviour at body temperature.

## Transformations
NiTi has a high-temperature austenite phase and a low-temperature martensite phase. On cooling, martensite starts at Ms and finishes at Mf; on heating, austenite starts at As and finishes at **Af**. An intermediate **R-phase** can appear in some conditions.
- **Superelastic devices** (stents, guidewires, filters) need Af below body temperature (commonly Af around 0 to 20 C, so the alloy is fully austenitic at 37 C and at room temperature during handling) so that loading induces martensite and unloading reverses it.
- **Shape-memory devices** (actuators, some staples) use Af above body temperature (or a controlled activation temperature) so that shape recovery occurs on heating.

## Sensitivity
- Af is highly sensitive to composition: roughly 10 C change per 0.1 atomic percent nickel; nitinol for medical use (ASTM F2063) is about 54.5-57 wt% nickel, and suppliers supply tubing or wire with a guaranteed Af range.
- Cold work and heat treatment shift transformation temperatures; thermal history after laser cutting or shape setting resets them (see nitinol-heat-treatment).
- Af also influences the plateau stress: stress rises with temperature above Af by several MPa per degree (Clausius-Clapeyron behaviour, about 6-7 MPa/K).

## Measurement
1. **DSC (ASTM F2004):** heat and cool a small specimen, record peaks; Af from the intersection of baseline and tangent of the transformation peak. Condition (anneal) consistent with finished device, after final processing.
2. **Bend and free recovery (ASTM F2082):** cool to martensite, bend, heat while measuring recovery, find temperatures at which recovery begins and ends; sensitive for finished device wire.
3. **Mechanical testing** (tensile at 37 C) confirms superelastic plateau and residual strain.
4. Test on final-geometry, final-processed devices, not just raw material.

## Verify
- [ ] Af measured on finished device and inside the specification (for example Af 15 +/- 5 C).
- [ ] Mechanical tensile plateau at 37 C and recovery strain verified.
- [ ] Incoming material certificate checked against measured transformation temperatures.
