---
id: engineering-technology.biomedical-engineering.medical-device-design.wireless-coexistence-medical
name: wireless-coexistence-medical
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [wireless-coexistence, rf-wireless, ansi-c63-27, wireless-medical-device, essential-performance]
level: advanced
status: gated
description: "Plan and test wireless coexistence for medical devices: spectrum choice, risk analysis, ANSI C63.27 test approach, graceful degradation and essential performance."
sources: ["IEEE/ANSI/USEMCSC C63.27-2021 American National Standard for Evaluation of Wireless Coexistence (active; published 17 May 2022; corrigendum 2026 listed), https://standards.ieee.org/ieee/C63.27/10662/", "FDA guidance Radio Frequency Wireless Technology in Medical Devices (final, 14 Aug 2013; has a Wireless Coexistence section), https://www.fda.gov/media/71975/download", "AAMI TIR69 Risk management of radio-frequency wireless coexistence of medical devices and systems (title and edition unconfirmed)", "https://www.fda.gov"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Wireless coexistence in medical devices

**Goal:** the device keeps its essential performance when other wireless devices share the spectrum, and fails safely when it cannot.

## Method
1. Define the wireless function, its role in safety (monitoring alarm transmission versus convenience), and the expected radio environment (hospital, home, mobile).
2. Select spectrum and technology: licensed or shared bands (2.4 GHz is crowded); consider channel agility and retransmission.
3. Risk analysis: lost, delayed, corrupted and duplicated data; interference causing a missed alarm or wrong therapy.
4. Design controls: error detection, acknowledgements, timeouts, local alarm when link is lost, safe state on link loss.
5. Test coexistence per the ANSI C63.27 approach (the standard gives methods and key performance indicators for coexistence in the intended environment; clause detail (gated: unconfirmed, source is paywalled or blocked)): define a pass criterion tied to essential performance, test with realistic interferers across channel and power conditions, and document.
6. Include radio emissions and immunity from IEC 60601-1-2 and radio regulations separately.
7. Labelling: state wireless technology, range, and degraded-mode behaviour.

## Verify
- [ ] Wireless-related hazards traced into the risk file.
- [ ] Coexistence test report against stated pass criteria.
- [ ] Link-loss behaviour verified.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
