---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-templates-zero-touch-provisioning
name: sdwan-templates-zero-touch-provisioning
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-templates, zero-touch-provisioning, sdwan-onboarding]
level: practitioner
status: draft
description: "Use device/feature templates, variables and ZTP/claim workflows to onboard branch edges consistently."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Templates and onboarding

- Build templates per role (small branch, large branch, hub) with variables for site-specific data (IP, VLAN, site ID). Avoid per-device CLI.
- ZTP: a factory-default edge contacts a cloud redirect service, receives its orchestrator address, authenticates by certificate or serial/token, and pulls its config.
- Pre-stage serials and device-to-site mapping in the portal before shipping.
- Lab the template, pilot at one site, then roll out in waves; keep a rollback template.
- Keep an out-of-band console path for failed onboarding.

## Verify
- [ ] A new edge shipped to a branch comes up, authenticates and shows the expected configuration with no console work.
