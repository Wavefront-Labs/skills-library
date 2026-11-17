---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-continuous-data-protection
name: veeam-continuous-data-protection
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam-cdp, continuous-data-protection, vaio, io-filter, rpo-seconds, cdp-proxy, veeam]
level: advanced
status: docs-checked
description: "Veeam CDP for VMware vSphere: snapshot-free VAIO replication, short and long-term restore points, failover and failback, and the documented requirements and limits."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/cdp_replication.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/cdp_requirements.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam continuous data protection (CDP)

**Goal:** protect mission-critical VMware VMs when losing seconds or minutes of data is unacceptable, with replicas ready to start.

## How it works
- CDP constantly replicates VM I/O using vSphere APIs for I/O filtering (VAIO), which avoids creating snapshots. Because it is always on and snapshot-free, it reaches a lower RPO than snapshot-based replication (near-zero RPO).
- I/O data stored on the target datastore forms short-term restore points, tracked in a journal that keeps records for a maximum of 168 hours (7 days). You can recover to seconds or minutes back, depending on the RPO you set.
- For older states, create long-term restore points (VM state hours or days back).
- Traffic is optimized: duplicate and zero blocks are filtered out and replica traffic is compressed.
- To replicate a VM you configure the required infrastructure components and create a CDP policy.

## Recovery
Recover to a short-term or long-term point by failing over to the replica. After the source is repaired, fail back to transfer changes; if it cannot be repaired, use permanent failover.

## Documented requirements and limits
- Licensing: availability depends on the license.
- Backup server: at least 16 GB RAM. Network: at least 100 Mbps recommended; better performance on 10 Gbps or faster with MTU 9000.
- Configure CDP for one cluster on one backup server only; adding the cluster (with the I/O filter) to another backup server makes CDP policies on the first fail.
- Maximum 400 CDP policies per backup server; one VM can be in only one CDP policy.
- Maximum 50 disks per VM; maximum 95 long-term restore points per disk.
- Not supported: 4K native disks, shared disks, physical RDM, SCSI bus sharing (vRDM is supported), VM storage policies with multiple datastore-specific rule sets, encryption of the transaction log files.
- VMs must have no snapshots when the policy first starts; CDP works only for powered-on VMs (VMs with IDE disks must be powered off for initial sync).
- Thick-provisioned disks need double space on the target during initial synchronization; half is freed afterwards. Changing a VM disk size restarts replication from scratch and removes earlier restore points.
- A cluster with the I/O filter installed cannot mix ESXi 7 and 8 hosts. When adding a cluster or host after the filter is installed, run the I/O Filter Management wizard.
- Replicas can be powered on only through the failover operation; Storage vMotion of replicas on the target is not allowed (host vMotion is, but not during failover).
- Re-IP works only for Windows VMs and only when failing over through Veeam; `*` in an IP matches a whole octet, and `10.0.0.*` does not match `10.0.1.1`.

## Checked
2026-11-07. Read in full: Veeam Help Center "Continuous Data Protection (CDP) for VMware vSphere" (updated 2025-10-22) and "Considerations and Limitations" (updated 2026-06-24), build 13.1.2.57. Linked pages on proxies, policy creation and How CDP Works were not read. Removed because the pages do not state them: the console menu path for installing the filter, "rolling install", CDP proxy placement and Windows/Linux types, the sample RPO/retention values (15 seconds, 4 hours, every 8 hours), the peak-write bandwidth sizing advice, the RPO-alarm gotcha and the invented Verify step.
Method: documentation only; no commands were run.
