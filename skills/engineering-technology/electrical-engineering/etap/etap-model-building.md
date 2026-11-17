---
id: engineering-technology.electrical-engineering.etap.etap-model-building
name: etap-model-building
category: engineering-technology
field: electrical-engineering
product: etap
tags: [electrical-engineering, etap, etap-library-data, etap-model, etap-model-building, etap-model-validation, one-line-diagram]
level: practitioner
status: draft
description: "Build an ETAP one-line diagram model: elements, library data, connectivity and validation before running studies."
sources:
  - "https://etap.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# ETAP one-line model building

1. **Data first:** collect utility short-circuit MVA with X/R (maximum and minimum), transformer nameplates (kVA, kV, %Z, X/R, tap range, vector group), cable type, size, length and installation, motor nameplates, breaker/fuse ratings, protective device model numbers and CT/relay data.
2. **Build the one-line:** place elements on the one-line diagram (utility, buses, transformers, cables, loads, motors, protective devices) and connect them; ETAP elements carry editor tabs (rating, impedance, loading, protection). Keep consistent naming (ID scheme) so reports map to drawings.
3. **Use the library** for cable and device data where possible instead of typing values; add custom entries to the project library for non-standard devices.
4. **Configurations and scenarios:** use study cases and configuration status (open/closed) to represent normal, emergency, generator-only and maximum/minimum utility cases rather than separate files.
5. **Validate:** run the model checks provided by the software (connectivity, missing data, isolated sections, duplicate IDs), compare transformer %Z and loading to nameplates, and review bus nominal voltages.
6. Save a baseline revision before modifying so changes can be compared.

**Tool-detail caveat:** menu names and report fields below are described from general ETAP practice and the ETAP documentation structure; confirm exact labels and options in the installed ETAP version's help (status draft, tool behaviour not re-run for this entry).

**Verify:** a first load-flow run converges and bus voltages are near nominal; sum of connected load matches the load schedule.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
