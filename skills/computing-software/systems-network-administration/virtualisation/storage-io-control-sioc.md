---
id: computing-software.systems-network-administration.virtualisation.storage-io-control-sioc
name: storage-io-control-sioc
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [sioc-congestion-threshold, storage-io-control, sioc, storage-performance, vmware, vsphere]
level: advanced
status: docs-checked
description: "Storage I/O Control: enable per datastore, disk shares and IOPS limits, the 30 ms default threshold, requirements, and Broadcom's SIOC troubleshooting steps and logging."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management-8-0/managing-storage-i-o-resources.html
  - https://knowledge.broadcom.com/external/article?legacyId=1022091
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage I/O Control (SIOC)

**Goal:** when a datastore is congested, VMs get I/O in proportion to their shares instead
of the noisiest VM winning.

## How it works
When you enable SIOC on a datastore, ESXi monitors the device latency hosts observe to it.
When latency exceeds a threshold the datastore is considered congested and each VM using it
is allocated I/O in proportion to its shares. Shares are set per VM. Configuring SIOC is
two steps: enable it on the datastore, then set shares and an upper IOPS limit per VM.

Defaults: all VM shares are Normal (1000) with unlimited IOPS, so if you leave the defaults
SIOC does not prioritise any VM. SIOC is enabled by default on Storage DRS-enabled datastore
clusters.

## Requirements
- Supported on Fibre Channel and iSCSI storage in ESX/ESXi 6.x, 7.x and 8.x; NFS support was
  added from ESXi 5.x.
- Datastores must be managed by a single vCenter Server.
- Datastores with multiple extents are not supported.
- Requires Enterprise Plus licensing; without it the enable option is greyed out.
- Arrays with automated storage tiering: check the VMware Storage/SAN Compatibility Guide
  for SIOC certification first.

## Enable
In the vSphere Client select the datastore, open Configuration > Properties, and under
Storage I/O Control choose Enabled. The setting is per datastore, not per host. If SIOC
misbehaves or the number of hosts on the datastore has changed since enabling it, disable
and save, then enable and save.

## Threshold
Under Storage I/O Control click Advanced. The KB gives 30 ms as the default congestion
threshold; if it was changed, reset it to 30.

## Shares and limits
Select the VM, Edit Settings, Resources tab, Disk. For a virtual disk pick the Share value
(Low, Normal, High or Custom with your own number) and enter an upper limit in the Limit -
IOPS column. These per-disk limits apply even when SIOC is not enabled. To see shares for
all VMs in a cluster, choose the cluster, Resource Allocation, Storage.

## SIOC logging
Set the host advanced setting `Misc.SIOControlLogLevel` (Host > Configuration > Software >
Advanced Settings > Misc): 0 is info logging only, 7 is complete logging. Enable it before
collecting support logs and set it back to 0 afterwards. On ESXi the log file is
`/var/log/storagerm.log`. The SIOC service on ESXi is controlled with
`/etc/init.d/storageRM {start|stop|status|restart}`.

## Checked
Date: 2026-11-07. Read in full the Broadcom vSphere 8.0 Resource Management page "Manage
Storage I/O Resources with vSphere" (the child pages listed in its navigation, such as
"Set Storage I/O Control Threshold Value", were not opened) and the KB "Troubleshooting
Storage I/O Control for vSphere" (article 311249). Corrected: the skill claimed a default
threshold of 90 percent of peak throughput; the KB gives 30 ms as the default. Removed as
not on the pages: the percentage-of-peak and typical-ms threshold advice, storage-policy
based SIOC with Low 500 and High 2000 share values, RDM and vSAN support statements, the
unmanaged-workload alarm, the performance chart names and the verify test. The menu paths
are the older Configuration > Properties paths the KB gives and may differ in current clients.
Method: documentation only; no commands were run.
