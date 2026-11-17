---
id: computing-software.firmware-embedded-development.iot-protocols.matter-ecosystems
name: matter-ecosystems
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-ecosystems, matter-development, matter, ecosystem, apple-home, google-home, alexa, iot-protocols]
level: practitioner
status: draft
description: "Matter ecosystems and controllers: Test with the major controllers."
sources:
  - https://csa-iot.org/all-solutions/matter/
  - https://github.com/project-chip/connectedhomeip
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter ecosystems and controllers

**Goal:** Test with the major controllers.

## Steps
1. Apple Home needs a home hub (HomePod or Apple TV) as a controller and Thread Border Router
2. Google Home uses Nest hubs or Android devices as hubs
3. Amazon Alexa Echo devices; Samsung SmartThings hub; Home Assistant has a Matter Server add-on
4. Each adds a fabric; use multi-admin
5. Test commissioning by QR from each
6. Check which clusters each ecosystem exposes in UI (confirm support lists)
7. Thread devices need a Border Router in the home

## Gotcha
A cluster working in chip-tool may not show in a given ecosystem app; verify per ecosystem, not only via chip-tool.

## Verify
- [ ] Commissioned to two ecosystems
- [ ] State syncs in both
- [ ] Offline behavior verified
