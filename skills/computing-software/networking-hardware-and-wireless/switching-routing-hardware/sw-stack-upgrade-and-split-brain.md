---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-stack-upgrade-and-split-brain
name: sw-stack-upgrade-and-split-brain
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [switch-split-brain, stack-upgrade, dual-active-detection]
level: advanced
status: draft
description: "Plan stack/MLAG upgrades with rollback, and set dual-active detection so a peer link failure does not create duplicate gateways."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Upgrades and split-brain

- Split-brain/dual-active: both members think they are the active member after the link between them fails, producing duplicate IPs and L2 loops. Configure a secondary detection path (e.g. a keepalive over a separate link or fast hello) and a defined tie-breaker.
- Upgrade methods vary: full reload of the stack, rolling/ISSU on supported platforms, or staggered MLAG peer upgrade. Verify supported versions and the vendor's upgrade matrix before starting.
- Always stage the image, check flash space, back up config, and have console access to each member.
- Test the downgrade path.

## Verify
- [ ] After upgrade, all members run the same version and the stack/peer state shows ready with expected roles.
