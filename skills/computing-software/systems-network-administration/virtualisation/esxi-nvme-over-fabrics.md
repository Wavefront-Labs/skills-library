---
id: computing-software.systems-network-administration.virtualisation.esxi-nvme-over-fabrics
name: esxi-nvme-over-fabrics
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [nvme-of, nvme-tcp, nvme-rdma, nvme-fc, hpp, vmware, esxi, vsphere]
level: advanced
status: docs-checked
description: "Connect ESXi to NVMe-oF storage over TCP, RDMA (RoCE v2) or FC: requirements, software adapters, VMkernel binding, controller discovery, HPP pathing and unsupported features."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0/about-vmware-nvme-storage.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/about-vmware-nvme-storage/requirements-for-vmware-nvme-storage.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/about-vmware-nvme-storage/configuring-nvme-over-tcp-on-esxi.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/about-vmware-nvme-storage/configuring-nvme-over-rdma-roce-v2-on-esxi.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/about-vmware-nvme-storage/configuring-nvme-over-rdma-roce-v2-on-esxi/add-controller-for-nvme-over-fabrics.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/understanding-multipathing-and-failover-in-the-esxi-environment/vmware-hpp.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# NVMe over Fabrics on ESXi

**Goal:** present NVMe namespaces from an array to ESXi hosts with multipathing and lower latency than SCSI. ESXi supports NVMe end to end, without NVMe-to-SCSI emulation.

## Transports and requirements
| Transport | Needs |
|---|---|
| NVMe/FC | Array with FC NVMe support and an FC HBA that supports NVMe; it shows as a vmhba with protocol NVMe and needs no adapter or controller configuration. It auto-connects to reachable targets. |
| NVMe/TCP | Array with NVMe/TCP, an Ethernet adapter, a software NVMe over TCP adapter, and a controller you add |
| NVMe/RDMA | Array with RoCE v2, switches supporting lossless Ethernet, a RoCE v2 NIC, a software NVMe over RDMA adapter, and a controller you add |

Local NVMe over PCIe needs only a compatible host and adapter (shown as a vmhba with protocol PCIe).

## TCP and RDMA setup (vSphere Client)
1. Install the NIC (RDMA: review it under the host's RDMA adapters).
2. Configure VMkernel binding: create a vSphere standard or distributed switch with the physical NIC and a VMkernel adapter, which binds the adapter to the VMkernel adapter.
3. Add the software NVMe over TCP or NVMe over RDMA adapter in the vSphere Client.
4. Add a controller: select the vmhba, Controllers tab -> Add Controller, then choose a discovery method:
   - Automatically: give the IP address and port (TCP also takes the digest parameter), click Discover Controllers and select one.
   - Manually: give the subsystem NQN and target port details (FC takes the WWNN and WWPN). Optional admin queue size (default 16) and keepalive timeout (default 60 seconds). IO queue size and IO queue number can only be set with esxcli.
5. The namespaces then appear as storage devices; a namespace is analogous to a LUN.

Arrays present namespaces to the host by subsystem NQN. Lossless Ethernet is a requirement for RoCE v2.

## Pathing
The High-Performance Plug-in (HPP) claims NVMe-oF targets by default; NMP cannot claim them. HPP supports only active/active and implicit ALUA targets, has no second-level plug-ins and does not support SCSI-3 persistent reservations. Path selection schemes: FIXED, LB-RR (the default for HPP-claimed devices), LB-IOPS (default switch after 1000 I/Os), LB-BYTES (default 10 MB) and LB-Latency (evaluates latency over a configurable interval and sample count). Change the scheme in the vSphere Client (Change the Path Selection Policy) or with the esxcli HPP commands; check the ESXi esxcli reference for exact syntax.

## Gotchas
- Do not mix transport types to access the same namespace, and make sure active paths are presented: namespaces cannot be registered until an active path is discovered.
- NVMe-oF does not support RDMs, core dump, SCSI-2 reservations or VAAI hardware acceleration plug-ins. Clustered VMDK is supported; shared VMDK with the multi-writer flag needs vSphere 7.0 Update 1 or later; Virtual Volumes need vSphere 8.0 or later.
- For NVMe/FC follow the general Fibre Channel storage recommendations.

## Verify
The namespaces appear under Storage Devices on the host, every path to each is listed, and the device is claimed by HPP.

## Checked
Date: 2026-11-08. Confirmed against the vSphere 8.0 Storage pages: About VMware NVMe Storage, Requirements for VMware NVMe Storage, Configuring NVMe over TCP and over RDMA (RoCE v2), Add Controllers for NVMe over Fabrics, and VMware High Performance Plug-In and Path Selection Schemes. Corrected: RDMs are unsupported on NVMe-oF (the draft said limited). Removed because the cited pages do not confirm them: all esxcli command lines (the esxcli reference page cannot be read as plain text), 32G FC and 7.0U3 TCP minimums, jumbo frame advice, vmk tag names, the ANA/ALUA equivalence, WSFC version claims, the persistent-discovery note and the VMFS6 requirement.
Method: documentation only; no commands were run.
