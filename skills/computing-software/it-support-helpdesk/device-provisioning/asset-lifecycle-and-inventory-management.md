---
id: computing-software.it-support-helpdesk.device-provisioning.asset-lifecycle-and-inventory-management
name: asset-lifecycle-and-inventory-management
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, asset-management, cmdb, inventory, warranty, spares-pool, loaner-devices, asset-tag, barcode, depreciation, hardware-refresh, lost-or-stolen, chain-of-custody, audit, serial-number, inventory-audit, asset-assignment]
level: practitioner
status: draft
description: "Track hardware through its full lifecycle: CMDB accuracy, warranty tracking, spares/loaner pools, periodic audits, hardware refresh cycles, lost/stolen device process."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# asset-lifecycle-and-inventory-management

Goal: know where every device is, who has it, and what state it's in,
end to end — this is what the day-one provisioning checklist in
`onboarding-and-offboarding-devices` depends on being accurate, and it's a
distinct, ongoing discipline from the one-time enrollment event.

## The CMDB/asset record is the source of truth, not the MDM console
- MDM consoles (Intune, Jamf) show *management* state; a separate CMDB
  (ServiceNow Hardware Asset Management, Snipe-IT, even a well-kept
  spreadsheet at small scale) should hold *ownership* state: who has it,
  cost center, purchase date, warranty expiry, location. These drift apart
  constantly — a device reassigned informally ("just hand your old laptop
  to the new hire") without an asset record update is the single most
  common cause of a CMDB being untrustworthy within a year.
- Minimum fields to track per asset: serial number, asset tag, model,
  purchase date, warranty expiry, assigned user, cost center/department,
  location/site, status (in-use, in-stock, in-repair, retired, lost).
  Serial number is the only field guaranteed unique and vendor-verifiable
  — asset tags get swapped, lost, or mis-stuck; always cross-check serial
  when the two disagree.

## Warranty and vendor support entitlement
- Pull warranty status by serial directly from the vendor (Dell
  TechDirect/Warranty API, Lenovo Warranty Lookup, HP Support) rather than
  trusting the purchase date in the CMDB — extended warranties, accidental
  damage protection (Dell ProSupport Plus, Lenovo ADP) are often bought
  separately and not reflected unless someone recorded it.
- Flag devices nearing warranty expiry (60–90 days) for the refresh queue
  or an extension decision before they go out of support — an
  out-of-warranty failure becomes a capital purchase decision mid-incident
  instead of a planned swap.

## Spares and loaner pools
- Keep loaners in a visibly separate CMDB status ("loaner-available" /
  "loaner-issued") so they don't get mistaken for abandoned stock during
  an audit, and set a return SLA (e.g. 5 business days after the user's
  own device is fixed/replaced) — loaners with no return date tend to
  become permanent, invisible shadow inventory.
- Wipe and re-provision loaners between users the same way as a full
  offboarding wipe (see `onboarding-and-offboarding-devices`) — a loaner
  is a higher re-exposure risk than a primary device precisely because it
  cycles through many users.
- Keep spares pre-imaged/pre-enrolled where provisioning time matters
  (executive laptop dies the morning of a trip) — but re-check compliance
  policies and app assignments are current before handing one out; a
  spare that's been sitting six months may be missing a year of patches.

## Periodic physical audits
- Reconcile MDM "last check-in" against CMDB "assigned" status at least
  quarterly — a device that hasn't checked in for 90+ days while marked
  active is either lost, stolen, retired without proper offboarding, or
  sitting powered off in a drawer; each needs a different action.
- Barcode/asset-tag scanning sweeps (even a phone camera + a simple app)
  for a physical office audit catch devices present but never logged
  (shadow IT purchases) and logged-but-absent devices faster than a
  manual spreadsheet check.

## Lost and stolen devices
1. Immediately mark the device lost/stolen in the MDM (triggers remote
   lock, and for encrypted drives confirms BitLocker/FileVault state) —
   before data classification matters, assume the worst and lock first.
2. Revoke the user's active sessions and rotate any credentials cached on
   the device (see the credential-rotation step in the related desktop
   and remote-support skills) — a lost laptop with a cached session token
   is a live access risk until revoked, not just a hardware loss.
3. File the incident per company policy — a lost device holding regulated
   data (PII, PHI, PCI) may trigger breach-notification obligations
   regardless of whether it's recovered; this decision isn't the
   helpdesk's to make alone, escalate to security/compliance immediately
   rather than waiting to see if it turns up.
4. Update CMDB status and, once past the recovery window, trigger
   insurance/write-off and chain-of-custody documentation (date reported,
   who reported, last known location, serial, remote-wipe confirmation).

## Depreciation and refresh cycles
- Standard refresh is typically 3–4 years for laptops, driven by OS
  support lifecycle (e.g. Windows feature-update support windows) and
  battery/performance degradation, not just accounting depreciation
  schedules — the two numbers often don't match and a device can be fully
  depreciated on the books while still under active OS support, or vice
  versa.

## Gotchas
- A device "returned" verbally at offboarding but never logged as
  received in the CMDB will look lost in the next audit — confirm
  physical receipt updates the record, not just the offboarding ticket
  closure.
- Don't let "in repair" become a permanent status — set a follow-up
  reminder; devices sent to vendor repair are a common place inventory
  silently vanishes.

## Verify
- CMDB record for a given serial matches MDM last-check-in, warranty
  status pulled from the vendor matches the recorded purchase/extension
  date, and a sample physical audit (10–20 devices) finds zero
  unexplained discrepancies between tag, serial, and assigned user.
