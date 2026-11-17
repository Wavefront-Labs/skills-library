---
id: computing-software.networking-hardware-and-wireless.check-point.management-high-availability
name: management-high-availability
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, management-ha, standby-smart-center, mgmt-sync]
level: practitioner
status: draft
description: "Set up an active and standby Check Point management server pair, sync status and promote the standby."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Installation_and_Upgrade_Guide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Management High Availability and synchronization

- A secondary Security Management Server (installed with the same version, a standalone **Secondary** role selected in the First Time Wizard) is added in SmartConsole: Manage & Settings > Permissions & Administrators > or **Gateways & Servers** > New > Check Point Host > select **Secondary Server**, then SIC.
```
cpstat mg                           # management status, role (active/standby)
mgmt_cli -r true show-api-versions
cpprod_util FwIsActiveManagement      # returns 1 on active (confirm)
```
- The first management is **Primary and Active**; sync is automatic every few minutes or at publish; status in the bottom bar "Synchronization". Manual sync is under Gateways & Servers > Sync.
- To fail over: connect SmartConsole to the standby and click **Actions > Set Active**; or on the CLI, `cpstat mg` to confirm; follow the documented procedure in the Management guide (confirm).
- Do not change both servers at the same time; the second one is read-only for policy until promoted. The previous active becomes standby after you resynchronize (full sync).
- Gateways connect to the active server for logs; add the secondary as a log server.
- Gotcha: the standby must be able to resolve and reach the active (TCP 18190, 18191, 18192, 19009 for CPM sync; confirm ports in sk), and must be the same Jumbo take.

Verify: SmartConsole shows both servers with `Synchronized`; `cpstat mg` shows `Active/Standby`.
