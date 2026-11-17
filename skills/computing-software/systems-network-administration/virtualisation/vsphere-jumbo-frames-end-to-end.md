---
id: computing-software.systems-network-administration.virtualisation.vsphere-jumbo-frames-end-to-end
name: vsphere-jumbo-frames-end-to-end
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [jumbo-frames, vmkernel-mtu, vsphere-networking, mtu-9000, vmkping, vmotion, vsan, iscsi, vmware, vsphere]
level: practitioner
status: draft
description: "Enable MTU 9000 end to end for vMotion, vSAN, iSCSI and NFS: vSwitch or vDS MTU, VMkernel MTU, physical switch, and proving it with vmkping -d -s 8972."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0.html
  - https://developer.broadcom.com/xapis/esxcli-command-reference/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jumbo frames end to end

A mismatched MTU is worse than none: small packets (pings, control traffic) work while
large ones silently drop, giving vMotion timeouts, vSAN "network configuration" health
failures, or iSCSI sessions that log in then stall.

## Order of change (largest to smallest)
1. **Physical switches**: every port and inter-switch link in the path at 9000+ (many
   vendors need 9216 to carry 9000 payload plus headers). Include LAG/vPC peer links.
2. **Virtual switch**: vDS → Settings → Advanced → MTU 9000 (switch-wide), or
   `esxcli network vswitch standard set -v vSwitch1 -m 9000`.
3. **VMkernel adapters** that should use jumbo:
   `esxcli network ip interface set -i vmk2 -m 9000`
4. **Storage targets/array ports** (iSCSI/NFS) and guests if they need it.

Management vmk0 usually stays 1500. The vSwitch MTU must be ≥ every vmk MTU on it.

## Prove it (the only valid test)
```sh
vmkping -I vmk2 -d -s 8972 10.10.20.12      # -d = don't fragment; 9000 - 20 IP - 8 ICMP
vmkping -I vmk2 -S vmotion -d -s 8972 10.10.30.12   # vMotion TCP/IP stack
esxcli network ip interface list | grep -i mtu
```
Success at 8972 and failure at 8973 means the path is exactly 9000. If 1472 works but
8972 fails, some hop is at 1500.

## vDS health check
Enable VLAN and MTU health check (vDS → Configure → Health Check) to catch physical-port
mismatches; it uses broadcast probes, so disable after validation on very large fabrics.

## Gotchas
- NSX overlay needs MTU ≥ 1600 (1700 recommended) on the TEP path even without jumbo.
- Changing vDS MTU briefly resets uplinks; do it in a window.
- Mixed MTU in a vSAN cluster gives intermittent "vSAN: MTU check (ping with large packet
  size)" failures in Skyline Health.
- Don't enable on vmk used for replication over a WAN/VPN unless the WAN supports it.

## Verify
All hosts pass `vmkping -d -s 8972` to every peer on each jumbo VMkernel network
(script the mesh), vSAN health MTU check green, vMotion of a large VM completes.
