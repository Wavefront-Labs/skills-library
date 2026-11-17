---
id: computing-software.systems-network-administration.patch-management.tracking-vendor-support-lifecycles
name: tracking-vendor-support-lifecycles
category: computing-software
field: systems-network-administration
product: patch-management
tags: [end-of-life, eol-software, support-lifecycle, endoflife-date, extended-support, lifecycle-calendar, risk-register, patch-management]
level: practitioner
status: docs-checked
description: "Track end-of-support dates for every OS, database, runtime and appliance in inventory: lifecycle sources, the endoflife.date API, 12/6/3-month warnings and risk register entries."
sources:
  - https://endoflife.date/api/v1/products/rhel/
  - https://endoflife.date/api/v1/products/windows-server/
  - https://learn.microsoft.com/en-us/lifecycle/
  - https://access.redhat.com/support/policy/updates/errata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracking vendor support lifecycles

**Goal:** no product silently stops receiving security fixes; every end-of-life date is
known a year ahead and has a plan.

## Sources
| Vendor | Where |
|---|---|
| Microsoft | Lifecycle pages (Fixed and Modern policy), Windows release health |
| Red Hat / SUSE / Canonical | Product lifecycle pages (full support, maintenance, ELS/ESM) |
| Oracle, VMware/Broadcom, Cisco, Fortinet, Palo Alto | EoL/EoS notices per product and version |
| Languages and runtimes (Python, Node.js, Java, PHP) | Project release schedules |
| Aggregator | **endoflife.date** (JSON API; each product record links its vendor release-policy page) |

## Automate with endoflife.date
```sh
curl -s https://endoflife.date/api/v1/products/windows-server/ | jq '.result.releases[] | {name, eolFrom, isEol}'
curl -s https://endoflife.date/api/v1/products/rhel/ | jq '.result.releases[] | {name, eolFrom, isEol}'
```
Each release record also carries `isMaintained`, `eoasFrom` and `eoesFrom`; the product record's `labels` say what the dates mean for that vendor (for RHEL `eol` is "Maintenance Support"; for Windows Server `eol` is "Security Support" and `eoes` is "Extended Security Updates"), and `links.releasePolicy` points to the vendor page. Read the labels before treating `eolFrom` as the last security fix. Join the result
with your software inventory (product + major version) to produce a report of assets by
months-to-EOL.

## Warnings and actions
| Time to EOL | Action |
|---|---|
| 12 months | Owner notified; migration plan and budget |
| 6 months | Migration in progress; decide on extended support |
| 3 months | Escalate; risk register entry if not finishing |
| Past EOL | Risk accepted formally with compensating controls (isolation), or ESU purchased |

## Know the support phases
The date that matters is the end of security fixes, and vendors define the phases differently. Microsoft publishes Fixed Policy (defined end-of-support dates at release) and Modern Policy (continuous servicing) products on its lifecycle site, with an Extended Security Updates FAQ. Red Hat describes Full Support, Maintenance Support and Extended Life Phases; errata are released in the first two, while the Extended Life Phase provides no bug fixes or security fixes, so continued fixes need a paid extended offering (Extended Life Cycle Premium and Long-Life add-ons for RHEL 8, 9 and 10, per the Red Hat policy page). Appliances often have "end of sale" years before "end of security fixes". Track the
**last security fix** date.

## Gotchas
- Components inside products (bundled Java, OpenSSL) have their own lifecycles.
- Cloud managed services force upgrades on their schedule (e.g. managed DB major versions).

## Verify
Report lists every inventory product with an EOL date or "unknown" (to research);
nothing reaches EOL without a plan, ESU or signed acceptance.

## Checked
Date: 2026-11-08. Documentation: endoflife.date v1 API responses for rhel and windows-server (fields name, eolFrom, isEol, isMaintained, eoasFrom, eoesFrom, labels, links.releasePolicy), Microsoft Lifecycle Policy landing page (Fixed and Modern policies, ESU FAQ), Red Hat Enterprise Linux life cycle page (Full Support, Maintenance Support, Extended Life Phase, ELCP and Long-Life add-ons, no security fixes in Extended Life Phase). Removed: the claim that v0 `<product>.json` paths still work, the "community" description, the Microsoft-extended-support and Linux ESM/ELS-fee statements as written (replaced with page-stated facts), and the unreadable endoflife.date docs page from sources. The 12/6/3-month schedule is advice, not a vendor fact.
Method: documentation only; no commands were run.
