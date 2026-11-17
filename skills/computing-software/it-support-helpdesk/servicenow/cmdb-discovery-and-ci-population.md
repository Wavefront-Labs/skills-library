---
id: computing-software.it-support-helpdesk.servicenow.cmdb-discovery-and-ci-population
name: cmdb-discovery-and-ci-population
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, cmdb, configuration-item, cmdb-discovery, servicenow-discovery, mid-server, service-graph-connectors, itil-4]
level: practitioner
status: draft
description: "Populate the CMDB from discovery not typing: ServiceNow Discovery via MID Server, Service Graph Connectors for Intune/SCCM, credentials, schedules and checking what landed."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://learn.microsoft.com/en-us/mem/intune/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cmdb-discovery-and-ci-population
Goal: CIs that support relies on (laptops, servers, apps, network gear)
arrive and stay current automatically, so nobody hand-maintains rows.

## Sources, best first
- **Endpoint management tools** via Service Graph Connectors (SGC):
  Microsoft Intune, Microsoft SCCM, Jamf. Laptops and mobiles come from
  here; agentless network discovery is weak for roaming devices.
- **ServiceNow Discovery** (horizontal, via MID Server): servers,
  network devices, storage, load balancers in the data centre/cloud.
- **Cloud discovery**: AWS/Azure/GCP via service accounts.
- **Agent Client Collector** where agents are acceptable.
- Manual entry only for things nothing can see (a wall-mounted kiosk with
  no agent), and then with an owner.

## Setting up Discovery
1. Install a **MID Server** (Windows or Linux service) in each network
   zone; validate it in MID Server > Servers.
2. Add **credentials** (Windows domain account with WMI/WinRM rights; SSH
   key for Linux; SNMP v3 for network). Store in Credentials, never in
   scripts. Test with "Test credential".
3. Create a **Discovery schedule** with IP ranges; run off-hours, start
   with a small range.
4. Review **Discovery Status** and the **ECC queue** for errors:
   authentication failures, WMI blocked by firewall (TCP 135 + dynamic RPC),
   SSH timeouts.

## Service Graph Connector for Intune (typical)
Install from the Store, enter Entra app registration (client ID, secret or
certificate, tenant), run guided setup, schedule import. Imports go
through **IRE** (Identification and Reconciliation Engine), so serial
number + name rules decide matches (see ci-reconciliation skill).

## What to check after the first run
- Counts by class vs the source (Intune device count vs `cmdb_ci_computer`
  with discovery source Intune).
- Key fields filled: serial, assigned user, OS version, model, location.
- Relationships created (server runs app, app depends on database).

## Gotchas
- Discovery accounts with domain admin rights are a security finding; use
  least-privilege accounts and document them.
- Multiple sources writing the same field fight each other; set
  reconciliation rules for data source precedence.
- Ranges including printers and OT devices can upset fragile equipment;
  exclude them.

## Verify
New laptops enrolled in Intune appear in the CMDB within one import cycle
with serial and user filled, without anyone creating them by hand.
