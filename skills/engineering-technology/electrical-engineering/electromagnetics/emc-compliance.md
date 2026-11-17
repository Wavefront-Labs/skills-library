---
id: engineering-technology.electrical-engineering.electromagnetics.emc-compliance
name: emc-compliance
category: engineering-technology
field: electrical-engineering
product: electromagnetics
tags: [cable-and-enclosure-emc, ce-marking, cispr, electrical-engineering, electromagnetics, emc, emc-compliance, emc-pre-compliance-testing, emi, iec-61000]
level: practitioner
status: draft
description: "Plan EMC compliance: emission and immunity standards, pre-compliance scans, and cable and enclosure practice."
sources:
  - "https://www.iec.ch/"
  - "https://www.fcc.gov/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# EMC compliance

1. **Framework:** EU EMC Directive 2014/30/EU, FCC Part 15 (US), and national equivalents; select the product standard (for example CISPR 32/EN 55032 for multimedia, EN 61000-6-x generic, IEC 61800-3 for drives, CISPR 11 for industrial equipment).
2. **Immunity tests (IEC 61000-4-x):** ESD (-2), radiated RF (-3), EFT burst (-4), surge (-5), conducted RF (-6), power-frequency magnetic field (-8), voltage dips (-11); define performance criteria A, B, C.
3. **Pre-compliance:** near-field probes and a spectrum analyser to find radiators; LISN and spectrum analyser for conducted; compare to limit with margin (6 dB).
4. **Design measures:** continuous ground plane, stackup, filtering at every I/O, shield 360-degree termination, ferrites, spread-spectrum clocks, reduced edge rates.
5. **Cables and enclosures:** keep slots shorter than a tenth of a wavelength of the highest frequency; conductive gaskets; filtered connectors; separate clean and noisy cables.
6. **Documentation:** technical file, declaration of conformity, and test reports from an accredited lab.

**Verify:** accredited test report with measurement uncertainty; keep the design under configuration control since changes may invalidate it.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
