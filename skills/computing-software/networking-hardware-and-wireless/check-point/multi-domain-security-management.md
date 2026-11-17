---
id: computing-software.networking-hardware-and-wireless.check-point.multi-domain-security-management
name: multi-domain-security-management
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, mds, multi-domain, domain-management-server]
level: practitioner
status: draft
description: "Understand Check Point Multi-Domain Security Management: MDS, Domain Management Servers, mdsstat and mdsenv."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_MultiDomainSecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-Domain Security Management (MDS) basics

```
mdsstat                              # status of MDS and each Domain Management Server (DMS)
mdsenv <domain-name>                 # switch CLI context to a domain
mdsenv                               # back to the MDS
mdsstop ; mdsstart                   # restart all domains
mdsstop_customer <domain>
```
- Multi-Domain Server (MDS) hosts several virtual management domains (Domain Management Servers, DMS), each with its own policy, objects, administrators and logs; the **Global Domain** holds shared rules/objects assigned to domains.
- Create domains in the **Multi Domain SmartConsole** (Multi Domain > Domains > New), choosing the IP address for each DMS (an IP per domain or the same with different ports, per version).
- From the CLI, each domain has its environment: after `mdsenv Domain1` you can use `fw`, `cpca_client`, and `mgmt_cli` commands inside that domain. Remember the prompt shows `[Domain1]`.
- Administrators can be global (Super User) or domain-specific; the API login selects the domain (`domain "Domain1"`).
- Logs: a **Multi-Domain Log Server** (MDLS) or per-domain logging; check disk, as logs are the main space consumer.
- Gotcha: forgetting `mdsenv` leads to editing the wrong environment; and `cpstop` on an MDS affects all domains. Use `mdsstop_customer` for single domains.
- Backup: `migrate_server` or `mds_backup` (confirm per version).

Verify: `mdsstat` shows `up` for MDS and each DMS (`FWM`, `CPM`); the domain appears in the Multi Domain SmartConsole as `Active`.
