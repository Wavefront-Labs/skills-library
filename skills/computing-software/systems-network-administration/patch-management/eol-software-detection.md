---
id: computing-software.systems-network-administration.patch-management.eol-software-detection
name: eol-software-detection
category: computing-software
field: systems-network-administration
product: patch-management
tags: [eol-detection, end-of-life, endoflife-date, support-lifecycle, software-inventory, eol-software, runtime-eol]
level: practitioner
status: docs-checked
description: "Detect end-of-life OS, runtimes and applications in the inventory automatically: endoflife.date API, mapping versions to cycles, upcoming-EOL reports and owner notification."
sources:
  - https://endoflife.date/docs/api
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/news-events/directives
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Detecting end-of-life software

EOL software gets no security fixes: every new CVE is permanent. NIST SP 800-40r4 treats
EOL as a distinct risk needing its own plan (upgrade, isolate, or accept with controls).

## Data source: endoflife.date
Community-maintained dates for hundreds of products (486 listed by the v1 API on 2026-10-27) with a JSON API (`/api/<product>.json`, and a newer `/api/v1/products`):
```sh
curl -s https://endoflife.date/api/rhel.json | jq '.[] | {cycle, eol, extendedSupport}'
curl -s https://endoflife.date/api/windows-server.json | jq '.[] | select(.cycle=="2016")'
curl -s https://endoflife.date/api/python.json | jq '.[0:5]'
```
Fields in the responses read on 2026-10-27: `cycle`, `releaseDate`, `eol`, `lts`, `latest`, `latestReleaseDate`, `support` (end of active support) and `extendedSupport`; `eol` and `extendedSupport` can be a date or a boolean. Vendor pages remain authoritative for contracts; use the
API for automation and verify edge cases.

## Mapping inventory to cycles
| Inventory field | Cycle |
|---|---|
| `/etc/os-release` VERSION_ID 8.9 | rhel `8` |
| Windows build 14393 | windows-server `2016` |
| `java -version` 1.8.0_402 | Temurin/Oracle Java `8` |
| `postgres --version` 13.14 | postgresql `13` |
| `node -v` v18.19 | nodejs `18` |
Write a mapping table per product (regex → cycle) and join with the API data daily.

## Report
- **EOL now**: assets running a cycle with `eol` < today (and no `extendedSupport` contract).
- **EOL within 6/12 months**: planning list, sent to owners with the date.
- Group by owner/business unit and by product for migration projects.

## Actions
EOL now → exception with compensating controls + migration date, or ESU/third-party
support purchase; upcoming → migration project kicked off ≥ 12 months ahead for OS/DB.

## Gotchas
- Distros with long lifecycles have phases (RHEL Full/Maintenance/ELS, Ubuntu standard vs
  ESM): define which phase counts as "supported" for your policy.
- Embedded/vendor-bundled runtimes follow the vendor's support, not upstream EOL.
- Appliances (firewalls, storage OS) have vendor EoSW dates not in public APIs: track
  manually.

## Verify
Dashboard shows EOL count trending down; every EOL asset has an owner, plan and exception.

## Checked
Date: 2026-10-27. Documentation: live endoflife.date API responses for rhel, windows-server (cycle 2016, eol 2027-01-12), nodejs and postgresql, and the v1 products listing (486 products). Corrected the product count and listed the actual field names. NIST SP 800-40 Rev. 4 page read. See also CISA BOD 26-02 "Mitigating Risk From End-of-Support Edge Devices" on the CISA directives page for edge devices.
Method: documentation only; no commands were run.
