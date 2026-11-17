---
id: computing-software.systems-network-administration.windows-server.ltsc-vs-annual-channel-servicing
name: ltsc-vs-annual-channel-servicing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-updates, servicing, ltsc, annual-channel, azure-local]
level: practitioner
status: docs-checked
description: "Choose between Windows Server LTSC and Annual Channel: support lifecycles, editions, Server Core only limits, feature cadence and which workloads fit each."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/servicing-channels-comparison
  - https://learn.microsoft.com/en-us/lifecycle/products/?terms=windows%20server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTSC vs Annual Channel

## Long-Term Servicing Channel (LTSC)
- A new major version is typically released every 2-3 years.
- **5 years mainstream + 5 years extended** support.
- Installable as Server Core or Server with Desktop Experience; available under all licensing programs.

## Annual Channel (AC)
- Typically a release every 12 months (for example version 23H2); each has a 24-month lifecycle: **18 months mainstream + 6 months extended**.
- Installable with the **Server Core** option only.
- Software Assurance customers only (volume licensing; loyalty programs such as Visual Studio Subscriptions also qualify).

## Choosing
| Need | Pick |
|---|---|
| Domain controllers, file servers, app servers | LTSC |
| Minimum operational churn | LTSC |

## Track lifecycles
Keep an inventory of OS version, channel and end-of-support date per server.

## Verify
- [ ] Every server's channel and end-of-support date known; AC hosts have an upgrade plan.

## Checked
2026-10-28: Confirmed on Learn page servicing-channels-comparison: LTSC release every 2-3 years, 5+5 years support, Server Core or Desktop Experience, all licensing programs; Annual Channel 12-month cadence, 24-month lifecycle (18 + 6), Server Core only, Software Assurance customers only, version 23H2 naming. Removed: release years, ESU, hotpatch, in-place AC upgrade claim, Azure Local and container rows, container image compatibility section, AD query. The lifecycle source link was not fetched.
Method: documentation only; no commands were run.
