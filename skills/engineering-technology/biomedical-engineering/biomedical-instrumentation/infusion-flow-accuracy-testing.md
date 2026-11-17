---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.infusion-flow-accuracy-testing
name: infusion-flow-accuracy-testing
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [flow-accuracy, infusion-pump, iec-60601-2-24, gravimetric-method, trumpet-curve, start-up-curve, back-pressure, balance]
level: advanced
status: gated
description: "Test infusion pump flow accuracy per IEC 60601-2-24: gravimetric setup, test rates, start-up and trumpet curves, back-pressure, evaporation control and uncertainty."
sources: ["IEC 60601-2-24 Particular requirements for the basic safety and essential performance of infusion pumps and controllers (confirm edition)", "FDA infusion pump guidance (current text at https://www.fda.gov)", "Balance and metrology guidance from the manufacturer (for example evaporation traps)"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Infusion pump flow accuracy testing

**Goal:** measure delivered flow versus set rate over time and show the pump meets its declared accuracy, including start-up behaviour.

Every figure below (back pressure, trumpet windows, rates, tolerance) is (gated: unconfirmed, source is paywalled or blocked); 100 mmHg = 13.33 kPa was computed. Values below summarise common practice from IEC 60601-2-24; confirm the test rates, windows and limits in the current edition and in your declared specification.

## Setup
- **Gravimetric method:** pump delivers into a container on a precision balance; the mass increase (corrected for density) gives volume. Use a balance with resolution well below the smallest volume of interest (for example 0.1 mg for low rates), calibrated.
- **Evaporation control:** cover the water surface with a layer of oil and use a covered container to prevent evaporation errors; keep temperature stable.
- **Fluid and temperature:** use degassed water or the specified test fluid at a stated temperature; fluid density matches temperature.
- **Back pressure:** the standard defines a nominal back pressure (about 100 mmHg or 13.3 kPa) (gated: unconfirmed, source is paywalled or blocked) with variations, applied by height or a pressure controller.
- **Administration set:** use the specified set type (and new sets per test); prime per instructions.
- **Data logging:** record mass at short intervals (for example every few seconds to a minute), with synchronised timestamps.

## Tests
1. **Start-up curve:** at a low rate (for example 1 mL/h) record from pump start for 2 hours (gated: unconfirmed, source is paywalled or blocked): shows delay before the delivered volume follows the set rate.
2. **Trumpet curves:** for a long run (for example the second hour after start-up), compute the maximum and minimum percentage error for observation windows of several durations (commonly 2, 5, 11, 19 and 31 minutes) (gated: unconfirmed, source is paywalled or blocked), plotted against window duration; shows short-term flow variation.
3. **Rates:** a low rate (for example 1 mL/h), mid (for example 25 mL/h) and maximum rate, and other rates per the standard and device claims.
4. **Mean flow accuracy** over the test period compared with the declared tolerance (for example plus or minus 5%).
5. **Variation tests:** with different back pressures, orientations, temperatures, syringe sizes (for syringe pumps) and in different power modes.

## Analysis
- Compute flow in each interval, apply the oil-layer evaporation correction, and compute percentage errors with a stated uncertainty (balance resolution, drift, temperature).
- Present the start-up and trumpet curves, and the mean flow and maximum deviation.

## Verify
- [ ] Balance calibration and an evaporation control test run in the same environment.
- [ ] Results at each required rate and condition meet the declared specification.
- [ ] Data and analysis scripts archived for audit.
