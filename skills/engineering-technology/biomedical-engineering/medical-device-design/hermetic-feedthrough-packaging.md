---
id: engineering-technology.biomedical-engineering.medical-device-design.hermetic-feedthrough-packaging
name: hermetic-feedthrough-packaging
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [hermetic-packaging, active-implants, active-implantable, feedthrough, helium-leak-test, iso-14708, titanium-case, ceramic-brazing]
level: advanced
status: gated
description: "Design an implant housing and feedthrough: titanium or ceramic cases, brazed and glass seals, helium leak testing, and why hermeticity protects electronics and tissue."
sources: ["https://www.iso.org/standard/52804.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hermetic packaging and feedthroughs for active implants

**Goal:** keep body fluids out of electronics and keep device materials out of tissue for the implant life, while passing wires through a metal or ceramic wall.

Safety-critical, regulated work. Requirements come from ISO 14708-1:2014 (a draft third edition is in enquiry per iso.org) and the particular standard for your device type (confirm editions) and from the notified body or FDA; this is background, not a design basis.

## Elements
- **Case:** laser-welded titanium (Grade 1 or 2 commonly) halves; ceramic or glass for RF-transparent designs. Weld quality, wall thickness and pressure cycling are specified.
- **Feedthroughs:** pins (platinum or platinum-iridium, niobium) through an insulator (alumina ceramic or glass) brazed (gold braze is common) to a titanium ferrule that is then welded to the case. Filtered feedthroughs add capacitors for EMI protection.
- **Hermeticity:** helium fine leak testing with the case sealed in or pressurised with helium and read by mass spectrometer. Fine-leak rates are in the order of 1e-9 to 1e-12 atm cc/s helium depending on volume and life target (gated: unconfirmed, source is paywalled or blocked); the allowable rate is derived from the internal volume, moisture limit and lifetime, not copied from a table.
- **Moisture getters** and internal humidity monitoring (residual gas analysis on samples) support the argument.
- **Header:** polymer (epoxy, polyurethane, silicone) cast over the connector block; polymer headers are not hermetic and must be addressed separately through material choice and design.

## Failure modes
- Braze voids, crack at ceramic during welding heat, dendrite growth between pins in moisture, corrosion of weld seams.

## Verify
- [ ] Gross and fine leak tests plus residual gas analysis on sample.
- [ ] Thermal cycling and pressure tests before and after leak testing.
- [ ] Documented lifetime moisture budget linked to the risk file.
