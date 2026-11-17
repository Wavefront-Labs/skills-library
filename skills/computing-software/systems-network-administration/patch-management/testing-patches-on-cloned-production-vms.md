---
id: computing-software.systems-network-administration.patch-management.testing-patches-on-cloned-production-vms
name: testing-patches-on-cloned-production-vms
category: computing-software
field: systems-network-administration
product: patch-management
tags: [production-clone-test, vm-clone, isolated-network, patch-testing, patch-management]
level: practitioner
status: docs-checked
description: "Test patches on clones of production VMs: isolated network bubble, avoiding duplicate SID/IP/AD conflicts, data masking, running the patch and tearing down."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controller-architecture
  - https://learn.microsoft.com/en-us/azure/virtual-machines/snapshot-copy-managed-disk
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Testing on cloned production VMs

The closest test you can get: same OS build, same apps, same data, same cruft. The risk is the clone talking to production.

## Isolate first
- Create a port group / vNet with **no route** to production (no gateway, or a dedicated firewall that drops everything except your jump host).
- Clone dependencies together into the bubble if the app needs them (DB, AD DC, file server); otherwise the app breaks for reasons unrelated to the patch.
- Disconnect the NIC at clone time, change network, then connect.

## Clone
- On a hypervisor, use its clone feature with the NIC disconnected, then attach the clone to the bubble network before connecting it.
- In Azure, an Azure managed disk snapshot is a full, read-only copy of a managed disk (OS or data disk) that exists independently of the source disk and can be used to create new managed disks. To build a new VM from a snapshot, first shut the source VM down cleanly. Create the new disks and VM in a separate, isolated virtual network.

## Avoid conflicts
- Keep the same hostname/IP only inside the bubble; never bridge it.
- Domain controllers: Microsoft's virtualised DC cloning relies on the hypervisor supplying a VM-Generation ID. When the IDs differ the DC treats itself as a clone (or restored snapshot) and applies safeguards such as invalidating the local RID pool and setting a new invocation ID. If the hypervisor does not provide a VM-Generation ID, a DC with a DCCloneConfig.xml boots into DSRM, and one without it boots normally, with the potential for a duplicate domain controller on the network. Either way, keep cloned DCs inside the isolated bubble.
- Disable outbound integrations: SMTP relays, scheduled jobs that post to partners, backup agents, licensing servers, monitoring agents (they will alert as the real host).
- Mask or minimise sensitive data if the test team should not see it.

## Test
Apply the patch exactly as production will (same tool/script), reboot, run app checks, time the install for window planning.

## Tear down
Delete clones and snapshots after sign-off; record deletion in the change.

## Gotchas
- Check vendor licence terms for clones.
- Time sources: give the bubble its own time source so authentication keeps working.
- Linked clones depend on a parent snapshot where the hypervisor uses them; do not leave them around.

## Verify
Bubble isolation test (route and port check to production fails) before power-on of the app; test results and install duration recorded in the change.

## Checked
Date: 2026-11-09. Confirmed against the Microsoft Learn virtualised domain controller architecture page (VM-Generation ID comparison, DCCloneConfig.xml behaviour, DSRM, duplicate DC risk, RID pool and invocation ID safeguards; read by keyword search, partial) and the Azure managed disk snapshot page (snapshot is a full read-only copy, independent of source, clean shutdown before creating a VM). Removed: the VMware PowerCLI and az commands, the claim that domain-joined clones reset the machine password, the Kerberos clock-drift claim and the licence-counting claim (stated as advice to check terms instead).
Method: documentation only; no commands were run.
