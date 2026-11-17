---
id: computing-software.it-support-helpdesk.device-provisioning.loaner-pool-procurement-and-asset-costs
name: loaner-pool-procurement-and-asset-costs
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, loaner-pool, hardware-procurement, asset-depreciation, saas-license-management, spare-stock, tco]
level: practitioner
status: draft
description: "Run a loaner and spare-stock pool, buy hardware against standard models, track TCO and depreciation for refresh decisions, and keep SaaS licence usage in check."
sources:
  - "https://www.iso.org/standard/68531.html"
  - "https://www.gartner.com/en/information-technology/glossary/total-cost-of-ownership-tco"
  - "https://learn.microsoft.com/en-us/microsoft-365/admin/activity-reports/activity-reports"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# loaner-pool-procurement-and-asset-costs

## Loaner pool and spare stock
- Size: typically 2-5% of the fleet per model class, more where repair turnaround is
  slow or there are many travellers. Track usage to tune.
- Loaners are fully managed devices (Autopilot/Intune), wiped between users with
  Autopilot Reset or a full reset, data never stored locally (OneDrive).
- Check-out records: user, date, expected return, condition; a loan becomes permanent
  only through the asset process.
- Spares: keep a stock of high-failure parts (docks, chargers, keyboards, mice, headsets,
  screens for common models). Reorder points per item.

## Procurement against standard models
- Catalogue of 3-5 standard models (standard laptop, power user, lightweight, desktop,
  ruggedised), reviewed yearly with vendors. Fewer models = fewer drivers, images,
  spares.
- Buy with: warranty (3-4 years next-business-day onsite), Autopilot registration by
  the reseller, asset tags/serials delivered electronically for import, firmware/BIOS
  settings preset where offered.
- Exceptions go through approval with a business case.

## TCO and depreciation
- TCO = purchase + deployment labour + support (tickets x cost) + licences + downtime +
  disposal minus residual value.
- Depreciation: typically straight-line over 3-4 years for laptops (purchase price /
  useful life per year); finance decides the policy. Refresh when support costs and
  failure rate climb past the value of keeping the device, often around year 4.
- Track per model: failure rate, ticket count, repair cost; this justifies refresh
  timing and model choice.

## SaaS licence usage
- Pull usage regularly: Microsoft 365 admin center usage reports (active users per
  product), app vendor admin consoles, SSO sign-in logs (last sign-in per app).
- Reclaim from inactive users (no sign-in 60-90 days) after confirming with the manager;
  downgrade over-licensed users (E5 used like E3).
- Watch shadow SaaS from expense reports and SSO discovery (Defender for Cloud Apps).
- True-up dates and renewal notice periods in a calendar with owners.

## Verify
Loaners are all accounted for with check-out records, purchases match standard models,
refresh decisions cite TCO data, and inactive SaaS licences are reclaimed monthly.
