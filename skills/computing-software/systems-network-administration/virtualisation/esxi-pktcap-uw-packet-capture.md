---
id: computing-software.systems-network-administration.virtualisation.esxi-pktcap-uw-packet-capture
name: esxi-pktcap-uw-packet-capture
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pktcap-uw, net-dvs, vsphere-troubleshooting, packet-capture, vsphere-networking, wireshark, vmware, vsphere]
level: advanced
status: docs-checked
description: "Capture packets inside ESXi with pktcap-uw at uplink, vmk or VM switchport, read vDS state with net-dvs, and open captures in Wireshark."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/monitoring-network-packets/using-the-pktcap-uw-tool/pktcap-uw-command-syntax.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/monitoring-network-packets/using-the-pktcap-uw-tool/filter-options-for-capturing-and-tracing-packets.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packet capture on ESXi: pktcap-uw and net-dvs

`pktcap-uw` captures at any point in the virtual switch path, which lets you locate
where a frame disappears.

## Find the capture points
```sh
esxcli network vm list                         # VM world IDs
esxcli network vm port list -w <worldID>       # Port ID, vSwitch, uplink in use
net-stats -l                                   # all PortNum with clients
```

## Capture
```sh
# VM's switchport, both directions (--dir 2)
pktcap-uw --switchport 67108879 --dir 2 -o /tmp/vm.pcap
# physical uplink, received from wire / sent to wire
pktcap-uw --uplink vmnic2 --dir 0 -o /tmp/in.pcap
pktcap-uw --uplink vmnic2 --dir 1 -o /tmp/out.pcap
# VMkernel adapter
pktcap-uw --vmk vmk1 -o /tmp/vmk1.pcap
# filters
pktcap-uw --uplink vmnic2 --ip 10.1.1.20 --tcpport 443 -c 500 -o /tmp/f.pcap
# where are drops happening
pktcap-uw --capture Drop -o /tmp/drops.pcap
```
Stop with Ctrl+C (or `-c` count). Write to a datastore for big captures, not `/tmp`
(ramdisk). Copy off with scp/datastore browser and open in Wireshark.

## Reading the path
Capture at VM port and at uplink simultaneously (two sessions in background with `&`,
stop with `kill $(lsof | grep pktcap-uw | awk '{print $1}' | sort -u)`). If the frame
is on the VM port but not on the uplink: vSwitch policy (VLAN, security policy, teaming
picks another uplink). On the uplink but no reply: physical network.

## net-dvs (vDS host-side state)
```sh
net-dvs -l | less        # per port: VLAN, teaming, security policy, stats, uplink
```
Use to confirm the host actually applied what vCenter shows (out-of-sync hosts).

## Gotchas
- `--dir` defaults to input only on older builds; always set it.
- Captures with VLAN tags appear only at uplink points (tags stripped toward VMs in VST).
- Capturing at high rates costs CPU on the host; filter and count.

## Verify
You can state the hop where the packet is last seen; the fix (VLAN, MTU, teaming, ACL)
makes it appear at the next hop in a repeat capture.

## Checked
2026-10-31: Confirmed the pktcap-uw capture points (--switchport, --uplink, --vmk),
directions (--dir 0/1/2), count and output options, --capture Drop and the --ip/--tcpport
filters against the vSphere 8.0 "pktcap-uw Command Syntax" and "Filter Options for
Capturing and Tracing Packets" pages. Removed the tcpdump-uw comparison and the 7.0+
version note.
Method: documentation only; no commands were run.
