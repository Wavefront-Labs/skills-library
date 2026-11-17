---
id: computing-software.networking-hardware-and-wireless.strongswan.child-sa-start-close-and-dpd-actions
name: child-sa-start-close-and-dpd-actions
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, start-action, dpd, trap, close-action]
level: practitioner
status: docs-checked
description: "Control how strongSwan CHILD_SAs start, restart and recover: start_action none, trap or start, close_action, dpd_action, dpd_delay and dpd_timeout."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# child sa start close and dpd actions
`start_action` (per child, default `none`): 
- `none` only loads the connection, to be initiated manually or used as responder.
- `trap` installs a trap policy that triggers the tunnel when matching traffic appears.
- `start` initiates the connection actively.
- `trap|start` combines both (the page says since 5.9.6).

Unloading or replacing a child with a non-`none` start action performs the inverse: `start` connections are closed, `trap` policies uninstalled.

`close_action` (default `none`) acts after the peer closes the CHILD_SA: `trap` installs a trap policy, `start` re-creates it at once. It acts on explicit close messages only, not on negotiation failures; use trap policies to reliably re-create failed CHILD_SAs.

`dpd_action` (default `clear`) on DPD timeout: `clear` closes the CHILD_SA, `trap` installs a trap policy, `restart` renegotiates under a fresh IKE_SA.

Connection-level liveness: `dpd_delay` (default `0s`) is the interval for active checks via IKEv2 INFORMATIONAL or IKEv1 R_U_THERE, enforced only if no IKE or ESP/AH packet arrived in that time. `dpd_timeout` applies to IKEv1 only; IKEv2 uses normal retransmission timeouts.

## Checked
2026-11-04. Confirmed against the swanctl.conf page: start_action, close_action and dpd_action values and defaults, and the dpd_delay and dpd_timeout descriptions.

Method: documentation only; no commands were run.
