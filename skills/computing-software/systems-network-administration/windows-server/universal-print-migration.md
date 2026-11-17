---
id: computing-software.systems-network-administration.windows-server.universal-print-migration
name: universal-print-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, print-server, print-services, universal-print, cloud-printing, universal-print-connector, entra-id, print-server-retirement]
level: practitioner
status: docs-checked
description: "Replace Windows print servers with Universal Print: licensing, native printers vs the connector, registering and sharing printers, Intune deployment and migration tool."
sources:
  - https://learn.microsoft.com/en-us/universal-print/fundamentals/universal-print-whatis
  - https://learn.microsoft.com/en-us/universal-print/fundamentals/universal-print-connector-installation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Universal Print as a print server replacement

Universal Print is Microsoft's cloud print service. It is built on IPP and Mopria standards, so no client printer drivers are needed, and it works with Windows and macOS.

## Licensing
A Universal Print license must be assigned to each user; see the Universal Print documentation for which Microsoft 365 plans include it.

## Printers
Printers that cannot talk to Universal Print directly use the **Universal Print connector** installed on a Windows machine (installer from the link in the documentation).

## Migration from print servers
Run the cloud service and the print server in parallel, move groups of users, then retire GPO-deployed printer connections and the print server.

## Verify
- [ ] Test user prints from an Entra-joined device; job appears in the printer's job
  history in the portal.

## Checked
2026-10-28: Confirmed on Learn pages universal-print-whatis and universal-print-connector-installation: IPP and Mopria with no drivers, Windows and macOS integration, license assigned to the user, connector installer. Removed: Entra join requirements, specific Microsoft 365 plans, Universal Print-ready printer claim, outbound-HTTPS detail, share/Intune provisioning steps, migration tool claim, limits (vendor features, connector single point of failure, server OS clients).
Method: documentation only; no commands were run.
