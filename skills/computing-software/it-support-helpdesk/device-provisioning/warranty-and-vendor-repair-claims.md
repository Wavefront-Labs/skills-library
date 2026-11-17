---
id: computing-software.it-support-helpdesk.device-provisioning.warranty-and-vendor-repair-claims
name: warranty-and-vendor-repair-claims
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, warranty-claim, vendor-repair, rma, self-dispatch, keep-your-hard-drive, diagnostics]
level: practitioner
status: draft
description: "Run warranty claims that get parts fast: check entitlement, gather vendor diagnostic codes, self-dispatch vs onsite vs depot, data protection during repair, and tracking returns."
sources:
  - "https://support.hp.com/us-en/checkwarranty"
  - "https://pcsupport.lenovo.com/us/en/warrantylookup"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# warranty-and-vendor-repair-claims

## Before you call
- Look up entitlement by serial: coverage type (onsite next business day, depot,
  accidental damage, keep-your-drive) and end date.
- Run the vendor's own pre-boot diagnostics (Dell ePSA/SupportAssist, HP PC Hardware
  Diagnostics UEFI, Lenovo Diagnostics). Vendors ask for the failure/validation code; with it
  you skip most of the phone script.
- Collect: serial, symptoms, steps tried, photos of physical damage, the user's location and
  availability.

## Choosing the route
| Route | Use when |
|---|---|
| Self-dispatch (Dell TechDirect, HP and Lenovo partner programs) | Certified techs on staff; parts ship to you, you fit them |
| Onsite engineer | Board swaps, sealed devices, no certified staff |
| Depot / mail-in | Low urgency, spare device available for the user |

## Data during repair
- Storage replacement: keep the failed drive if the contract has keep-your-hard-drive;
  otherwise wipe or remove before shipping where possible.
- Board replacement on Windows: BitLocker recovery key needed after; Autopilot hash changes
  (re-register). On Macs, the device may need re-activation.
- Never send a device with an unknown admin password or activation lock unless asked.

## Track
- Record the case/RMA number, parts ordered, and engineer visit date in the ticket.
- Return defective parts within the vendor's window (often 10-15 days) or you are billed.
- Log repeat failures by model; three similar faults is a pattern worth raising with the
  account manager.

## Gotchas
- Accidental damage claims need honest descriptions; "it stopped working" on a cracked
  screen gets rejected.
- Out-of-warranty repairs above about half the device's value: replace instead.

## Verify
The device passes vendor diagnostics after repair, the user confirms it works, the
defective part is returned, and the asset record notes the repair.
