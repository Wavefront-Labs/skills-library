---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.amperometric-glucose-sensor
name: amperometric-glucose-sensor
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [amperometric-sensor, biosensor, electrochemical-biosensor, glucose-oxidase, glucose-dehydrogenase, mediator, test-strip, iso-15197]
level: advanced
status: draft
description: "Understand the electrochemistry of amperometric glucose sensors: enzyme and mediator, electrode layout, applied potential, interferents, hematocrit and accuracy standards."
sources: ["Wang, Electrochemical glucose biosensors (Chem Rev 2008)", "ISO 15197 In vitro diagnostic test systems - Requirements for blood-glucose monitoring systems for self-testing (2013 edition; confirm current)", "Bard and Faulkner, Electrochemical Methods"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Amperometric glucose sensor

**Goal:** convert glucose concentration into a measurable current, reproducibly, with limited interference.

## Chemistry
- Enzyme (glucose oxidase, GOx, or glucose dehydrogenase, GDH) oxidises glucose; the reduced enzyme is re-oxidised by a mediator (for example a ferricyanide or osmium complex) that is then oxidised at the electrode at a modest potential. The current is proportional to glucose over the working range.
- First-generation sensors measure oxygen consumption or hydrogen peroxide at a high potential (about +0.6 V vs Ag/AgCl), which also oxidises interferents; second-generation mediators lower the potential (around 0.2 V or below); third-generation direct electron transfer is mostly research.

## Strip design
- A working electrode with enzyme and mediator, a counter or reference electrode (Ag/AgCl or carbon), a capillary channel that draws a few tenths of a microlitre to a microlitre of blood, and a fill-detect electrode.
- The meter applies a potential step, waits the incubation period and records the current (Cottrell-type decay); the endpoint current relates to glucose via a calibration code or lot-specific curve.

## Interferents and errors
- Electroactive species (acetaminophen, ascorbic acid, uric acid) at high potentials; sugars like maltose or xylose for some enzymes (GDH-PQQ); oxygen for GOx strips; haematocrit (the sample viscosity changes diffusion); temperature; humidity damage to strips.
- Mitigation: lower potentials, dual-electrode compensation, haematocrit correction by impedance, temperature sensor, rejection algorithms.

## Accuracy
ISO 15197:2013 requires a high share of results to be within a limit of the reference method (for example 95% within plus or minus 15 mg/dL below 100 mg/dL and plus or minus 15% above) and also consensus error grid criteria; confirm the current edition and local regulatory expectation.

## Verify
- [ ] Interference panel tested at specified concentrations.
- [ ] Haematocrit range tested (for example 20-60%).
- [ ] Lot-to-lot calibration validated; strip stability confirmed.
