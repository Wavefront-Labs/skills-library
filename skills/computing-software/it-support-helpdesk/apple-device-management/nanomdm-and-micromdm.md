---
id: computing-software.it-support-helpdesk.apple-device-management.nanomdm-and-micromdm
name: nanomdm-and-micromdm
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, mdm-alternatives, nanomdm-and-micromdm, nanomdm, micromdm, open-source-mdm]
level: practitioner
status: draft
description: "Understand open-source MDM servers NanoMDM and MicroMDM, their storage backends and where they fit for labs, commands and custom workflows."
sources:
  - "https://docs.kandji.io/"
  - "https://learn.microsoft.com/en-us/mem/intune/"
  - "https://github.com/micromdm/nanomdm"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# nanomdm-and-micromdm

Goal: know what the open-source MDM servers provide.
- MicroMDM: single binary with API and command queue, DEP sync and APNs, no UI beyond community front-ends.
- NanoMDM: minimal MDM core with pluggable storage (file, MySQL, PostgreSQL), push, and webhooks; pair with NanoDEP for ADE.
- Generate APNs via `mdmctl mdmcert` or a vendor signed CSR flow (confirm current steps).
- Commands are sent as plists to `/v1/enqueue/<id>` or `/v1/commands/<id>`.
- Use for lab protocol learning, custom flows, and testing declaration endpoints.
Gotcha: no built-in inventory, scope or UI; production use means building or adopting these layers yourself and securing the API key.
Verify:
- Test device enrols and an enqueued DeviceInformation returns a response.
- API key is not exposed publicly.
