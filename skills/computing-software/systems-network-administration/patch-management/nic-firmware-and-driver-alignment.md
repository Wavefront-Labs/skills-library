---
id: computing-software.systems-network-administration.patch-management.nic-firmware-and-driver-alignment
name: nic-firmware-and-driver-alignment
category: computing-software
field: systems-network-administration
product: patch-management
tags: [nic-firmware, nic-driver, firmware-driver-compatibility, vmware-hcl, firmware-patching, patch-management]
level: practitioner
status: draft
description: "Keep NIC firmware and drivers aligned: check vendor and HCL support matrices, read versions on Linux/Windows/ESXi, update both in one window and avoid mismatches."
sources:
  - https://compatibilityguide.broadcom.com/
  - https://www.kernel.org/doc/html/latest/networking/ethtool-netlink.html
  - https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapter
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NIC firmware and driver alignment

Mismatched NIC firmware and driver versions cause the classic post-patch failures: link flaps, dropped offloads, PSODs/BSODs, RDMA breakage. Treat firmware + driver as one unit.

## Find the supported pair
- **VMware**: Broadcom Compatibility Guide lists, per NIC and ESXi release, the certified driver + firmware combinations.
- **Server vendor**: Dell/HPE/Lenovo release bundles (SPP, UXSP, Dell catalog) pair NIC firmware with tested drivers.
- **NIC vendor** release notes (Intel, Broadcom, NVIDIA/Mellanox) state minimum driver per firmware.

## Read versions
```sh
ethtool -i ens1f0        # driver, version, firmware-version, bus-info
devlink dev info pci/0000:3b:00.0
```
```powershell
Get-NetAdapter | Select-Object Name, InterfaceDescription, DriverVersion, DriverDate
Get-NetAdapterAdvancedProperty -Name 'Ethernet 1'   # firmware sometimes here; vendor tools otherwise
```
```sh
# ESXi
esxcli network nic get -n vmnic0       # Driver Info + Firmware Version
```

## Update together
1. Stage both: driver package (OS) and firmware (via BMC/vendor tool).
2. Typical order: driver that supports both old and new firmware first, then firmware, then reboot. Follow vendor notes when they say otherwise.
3. Do one host per cluster/team at a time; check teaming/bond failover with `cat /proc/net/bonding/bond0` or `Get-NetLbfoTeam`/SET status.

## Gotchas
- OS cumulative updates and Linux kernel updates can swap inbox drivers silently (e.g. Windows Update offering a newer/older NIC driver; kernel in-tree driver replacing out-of-tree). Control driver updates explicitly (WUfB driver exclusion policy, `dkms` packages).
- Firmware upgrades can reset NIC settings (SR-IOV, NPAR, boot options).
- Mixed firmware within a bond/team can cause asymmetric behaviour.

## Verify
All hosts in a cluster report the same driver/firmware pair listed in the HCL/bundle; no link-down or driver errors in logs after 24 hours.
