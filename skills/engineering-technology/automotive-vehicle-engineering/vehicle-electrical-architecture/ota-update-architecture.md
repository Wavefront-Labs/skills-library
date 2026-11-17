---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.ota-update-architecture
name: ota-update-architecture
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [ota-update, over-the-air, uptane, unece-r156, sums, rollback, delta-update, software-update-management]
level: practitioner
status: verified
description: "Design an OTA update system: backend, vehicle update manager, signing (Uptane-style), A/B partitions, delta updates, safety conditions and UN R156 expectations."
sources:
  - "UN Regulation No 156 (software update and software update management system) as published in the EU Official Journal (https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:42021X0388)"
  - "UN Regulation No 155 (cyber security management system) as published in the EU Official Journal (https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:42021X0387)"
  - "Uptane Standard (https://uptane.org/docs/2.0.0/standard/uptane-standard)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# OTA update architecture

Professional practice guidance; UN R156 and R155 compliance is established with your approval authority.

1. **Backend:** campaign management (which vehicles, which versions, staged rollout), software repository with signed metadata, secure transport (TLS), vehicle identity.
2. **Vehicle side:** telematics unit as OTA master, update manager coordinating ECU updates, and per-ECU flashing via UDS or an internal bus; gateway enforces access.
3. **Security:** signed images and metadata; Uptane adds separation of roles and per-ECU verification to survive compromise of one key or server; verify before install, not just at download.
4. **Robust install:** A/B partitions (install to the inactive partition, switch on success) or recovery partition; rollback on failed self-test; watchdog on first boot.
5. **Delta updates** reduce download size; verify the base version first.
6. **Safety and conditions:** install only when the vehicle is stationary, ignition/charging state is safe, battery level sufficient; consider functional safety of the update process; user consent and information (R156 expects the driver to be informed of updates and safe states during update).
7. **UN R156 (software update management system):** requires documented processes for updates, tracking software versions (RXSWIN), ensuring updates do not endanger safety, and compatibility with the type approval; confirm the current text and national implementation.
8. Records: configuration tracking per VIN, update history, and ability to prove the exact software on any vehicle.
9. Test: power-loss during update, bad image, network loss, mixed fleets.

**Gotchas:** interdependent ECU versions causing incompatible combinations; unmanaged variants.

## Verify
- [ ] Power-loss and corrupted-image tests lead to a working vehicle (rollback or retry).
- [ ] Software version inventory for a vehicle matches the update records.
