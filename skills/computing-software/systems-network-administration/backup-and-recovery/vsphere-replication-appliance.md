---
id: computing-software.systems-network-administration.backup-and-recovery.vsphere-replication-appliance
name: vsphere-replication-appliance
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [vsphere-replication-appliance, vsphere-replication, hypervisor-replication, rpo, site-recovery-manager, mpit]
level: advanced
status: gated
description: "Deploy and run vSphere Replication: appliance pairing, per-VM RPO, multiple point-in-time instances, seeds, recovery, and use as SRM's replication engine."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/live-recovery/vsphere-replication/9-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=2102453
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere Replication

Hypervisor-based asynchronous replication of individual VMs, licensing and edition entitlements change: confirm in Broadcom documentation (gated: unconfirmed, source is paywalled or blocked). Storage-agnostic (any datastore to any datastore).

## Deploy
1. Deploy the **vSphere Replication appliance** OVF at each site (one per vCenter); optional extra replication servers for scale.
2. Register it with vCenter via the VAMI (port 5480 (gated: unconfirmed, source is paywalled or blocked)) and accept the SSO certificate.
3. **Pair sites** in the Site Recovery UI (source vCenter -> target vCenter); configure network mappings for replication traffic (a dedicated vmkernel with vSphere Replication tags is best).

## Configure a VM
Right-click VM > Configure Replication:
- Target site, datastore, storage policy, disk format.
- **RPO** from 5 minutes to 24 hours, with a lower minimum for enhanced replication (gated: unconfirmed, source is paywalled or blocked). Confirm the exact range for your version in the vSphere Replication Administration guide.
- Quiescing (VSS for Windows) if application consistency needed; increases impact.
- **Multiple point-in-time (MPIT) instances**: keep several recovery points (a maximum of 24 was reported in the admin guide, (gated: unconfirmed, source is paywalled or blocked)), which appear as snapshots after recovery; useful against corruption. Retention depends on the RPO: confirm the instance-count rules in the admin guide.
- **Seeds**: pre-copy the VMDK to the target (e.g. from a restore) and point to it to avoid initial full sync.
- Network compression and encryption options.

## Recover
Site Recovery > Replications > Recover: synchronise latest changes (if source is up) or use latest available data; choose folder and resource; power on. Then reverse replication when the original site returns.

## With SRM / Live Site Recovery
vSphere Replication is the replication engine for SRM protection groups when array replication is not used; SRM adds recovery plans and testing.

## Gotchas
- RPO violations from bandwidth: check the per-VM "RPO violation" status and link capacity.
- Replicated VMs' snapshots at source are not replicated as snapshots.
- Cannot replicate VMs with physical RDMs (gated: unconfirmed, source is paywalled or blocked).

## Verify
Replication status OK with last sync within RPO; a test recovery into an isolated network boots the VM.

## Checked
Date: 2026-11-02. The Broadcom techdocs vSphere Replication 9.0 landing page and the Broadcom knowledge-base article were fetched; the landing page only lists guide titles and the KB article gives scale maximums (one appliance per vCenter; up to 9 additional replication servers per appliance; for 8.6 and newer, 4000 VMs managed and 400 protected per server), none of which this skill relies on. The administration-guide pages that hold RPO, MPIT, quiescing and recovery details could not be fetched as readable text, so those figures are marked gated. Marked gated: RPO range, MPIT count, port 5480, RDM restriction, edition entitlement. Nothing else was confirmed.
Method: documentation only; no commands were run.
