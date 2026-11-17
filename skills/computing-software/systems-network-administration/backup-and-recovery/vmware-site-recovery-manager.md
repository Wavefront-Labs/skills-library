---
id: computing-software.systems-network-administration.backup-and-recovery.vmware-site-recovery-manager
name: vmware-site-recovery-manager
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [srm, site-recovery-manager, live-site-recovery, recovery-plan, protection-group, vsphere-replication, dr-orchestration]
level: advanced
status: draft
description: "Orchestrate vSphere DR with Site Recovery Manager: site pairing, replication, protection groups, recovery plans, test recovery, planned migration and reprotect."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/live-recovery/live-site-recovery/9-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=2102453
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VMware Site Recovery Manager

**Goal:** fail vSphere workloads over to a recovery site with a tested, ordered, one-click recovery plan. (Broadcom renamed SRM to VMware Live Site Recovery; concepts are unchanged.)

## Components
- SRM appliance at each site, registered with its vCenter; sites **paired**.
- Replication: **vSphere Replication** (per-VM, host-based, RPO 5 min to 24 h) or **array-based replication** via the storage vendor's Storage Replication Adapter (SRA).
- **Inventory mappings**: networks, folders, resource pools, storage policies between sites. Separate test network mappings.
- **Placeholder datastore** for placeholder VMs at the recovery site.

## Protection groups
Sets of VMs failed over together: vSphere Replication groups (chosen VMs), array-based groups (all VMs on replicated datastores/consistency groups), or storage policy based groups.

## Recovery plans
- Contain one or more protection groups.
- **Priority groups 1-5** and VM dependencies define boot order (identity first, then databases, then apps).
- IP customisation (per VM or by subnet rules), pre/post power-on steps (scripts, prompts), shutdown actions for the protected site.

## Operations
- **Test recovery**: runs the plan into isolated test networks using snapshots of replicated data; production replication continues. **Cleanup** removes test VMs.
- **Planned migration**: sync, shut down protected VMs cleanly, recover with no data loss; fails if errors occur.
- **Disaster recovery**: recover from last replicated data even if the protected site is unreachable; continues past errors.
- **Reprotect**: reverse replication direction after a recovery; then run the plan back for **failback**.

## Gotchas
- Inventory mapping gaps make VMs fail to recover; run test recovery after every infrastructure change.
- Array-based plans depend on SRA and array versions matching the compatibility matrix.

## Verify
Quarterly test recovery completes without errors, with recorded duration per priority group compared to RTO.
