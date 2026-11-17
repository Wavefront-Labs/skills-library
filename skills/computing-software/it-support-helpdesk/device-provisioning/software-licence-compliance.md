---
id: computing-software.it-support-helpdesk.device-provisioning.software-licence-compliance
name: software-licence-compliance
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, software-license-compliance, software-asset-management, effective-licence-position, licence-audit, sam]
level: practitioner
status: draft
description: "Keep software licence compliance: build an effective licence position from entitlements and installs, understand licence metrics, reclaim unused licences, survive vendor audits"
sources:
  - "https://www.iso.org/standard/68531.html"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps"
  - "https://learn.microsoft.com/en-us/mem/configmgr/apps/deploy-use/monitor-app-usage-with-software-metering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# software-licence-compliance

## Effective licence position (ELP)
For each product: entitlements owned versus what is deployed or assigned, using the
vendor's licence metric.

| Product | Metric | Entitled | Used | Position |
|---|---|---|---|---|
| Visio Plan 2 | Per user (subscription) | 50 | 46 assigned | +4 |
| Adobe Acrobat Pro | Named user | 120 | 131 active | -11 |
| CAD tool | Concurrent | 20 | 26 peak | -6 |

## Data sources
- Entitlements: contracts, reseller portals, Microsoft 365 admin center licence pages,
  invoices. Keep proof of purchase.
- Usage: Intune Discovered apps, ConfigMgr software inventory and metering, SaaS admin
  consoles (last activity), licence servers for concurrent licences.

## Licence metrics to understand
Per user, per device, concurrent, per core (servers, often with minimums), and virtual
environment rules. A desktop app installed on a VDI image counts per device that can
access it for some vendors.

## Reclaim and control
- Monthly: remove licences from leavers and users inactive 60-90 days (after asking).
- Request workflow with approval and cost centre; approved catalogue in Company Portal/
  Self Service.
- No local admin rights so users cannot install unlicensed software.

## Audits
- Vendor audit letters: acknowledge, involve procurement/legal, agree scope and dates;
  never send raw data without reviewing it first.
- Run your own ELP twice a year so findings are not a surprise.

## Gotchas
- Free for personal use is not free for business (common with utilities and trial
  software).
- Shared accounts on per-user SaaS breach terms.
- OEM licences are tied to the device and do not move with the user.

## Verify
ELP up to date for top-spend vendors, negative positions have an approved purchase or
removal plan, and reclaimed licences are reported each month.
