---
id: engineering-technology.biomedical-engineering.medical-device-design.ethylene-oxide-design
name: ethylene-oxide-design
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [ethylene-oxide, sterilization-design, sterilisation-compatibility, eto, ethylene-oxide-sterilization, iso-11135, eo-residuals]
level: advanced
status: gated
description: "Design a device and its packaging to be sterilised by ethylene oxide: gas access to lumens and interfaces, material EO uptake, residuals and cycle-time effects."
sources: ["https://www.iso.org/standard/56137.html","https://www.iso.org/standard/84824.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Designing for ethylene oxide (EO) sterilisation

**Goal:** a device whose every surface can be reached by EO and humidity during the cycle, and from which EO and by-products can be removed to acceptable levels.

Engineering guidance. Cycle development and validation follow ISO 11135:2014 (reviewed and confirmed 2024; a new edition is at FDIS stage per iso.org, so confirm the current edition) with a qualified sterilisation provider.

## Design rules
- **Gas access:** EO is a gas, so it diffuses slowly into long narrow lumens, blind holes and tight mated interfaces. Avoid closed-end lumens; keep length-to-diameter of through-lumens modest; add vent paths or sterilisation ports; avoid zero-clearance joints that trap air.
- **Moisture and temperature:** typical cycles precondition for humidity and run at roughly 30-60 C with defined humidity and EO concentration (gated: unconfirmed, source is paywalled or blocked); electronics, adhesives and some plastics must tolerate heat and humidity swings and deep vacuum.
- **Material uptake:** materials such as PVC and polyurethane can absorb EO; thick sections need longer aeration. Choose materials with known EO behaviour and note that residuals limits (ISO 10993-7: the 2008 edition and its 2019 amendment are withdrawn and ISO 10993-7:2026 is current per iso.org) depend on contact duration and patient exposure.
- **Packaging:** the sterile barrier must pass EO and moisture but block microbes (for example medical-grade paper or Tyvek-type breathable films) and survive vacuum pressure changes without bursting; see sterile-barrier-design.
- **Load pattern:** the worst-case location in the product, such as the innermost lumen or most packed unit, is where the biological indicator or process challenge device is placed.

## Process choices that interact with design
- Preconditioning and aeration times drive lead time; a product that needs a week to degas may change your launch plan.
- Residual ethylene chlorohydrin and ethylene glycol also need to be assessed where relevant.

## Verify
- [ ] Hardest-to-reach location identified and challenged in the validation.
- [ ] Material list checked for EO, humidity and vacuum compatibility.
- [ ] Residuals within the limits your risk assessment sets, measured by an accredited lab.
- [ ] Package integrity after cycle confirmed.
