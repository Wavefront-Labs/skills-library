---
id: computing-software.systems-network-administration.wireshark.stp-cdp-lldp-frame-analysis
name: stp-cdp-lldp-frame-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, stp-analysis, cdp, lldp, bpdu, layer2-analysis]
level: practitioner
status: verified
description: "Analyse STP/RSTP BPDUs and CDP/LLDP frames in Wireshark to find the root bridge, topology changes, native VLAN mismatches and switch port identity."
sources:
  - https://www.wireshark.org/docs/dfref/s/stp.html
  - https://www.wireshark.org/docs/dfref/l/lldp.html
  - https://www.wireshark.org/docs/dfref/c/cdp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STP/CDP/LLDP frame analysis

## Capture filters
```
stp                                 # BPF: 802.3 frames with LLC DSAP 0x42 (compiles to a length check and byte 14 == 0x42, not a MAC match)
ether dst 01:00:0c:cc:cc:cd         # Cisco PVST+
ether host 01:00:0c:cc:cc:cc        # CDP/VTP/DTP
ether proto 0x88cc                  # LLDP
```

## STP display filters
```
stp.root.hw                         # root bridge MAC
stp.root.prio
stp.flags.tc == 1                   # topology change flag
stp.type == 0x02                    # RSTP/MSTP BPDU
```
- The root bridge ID should be the intended core switch. An access switch or a hypervisor bridge
  claiming root (priority 32768 with lowest MAC) is a misconfiguration.
- Many TC flags: a port flapping without portfast/edge, flushing MAC tables and causing flooding.
  The bridge ID in the BPDU points to the switch that originated the TC.
- PVST+ BPDUs carry the VLAN in a TLV (`stp.pvst.origvlan`); a mismatch with the native VLAN is reported by the switch
  (look for a PVID inconsistency message in its log).

## CDP/LLDP: what port am I on?
```
cdp.deviceid
cdp.portid
cdp.native_vlan
lldp.port.id
lldp.tlv.system.name
lldp.ieee.802_1.port_vlan.id
lldp.ieee.802_3.mdi_power_support
```
Capture for at least one advertisement interval (check the switch's CDP/LLDP timers; both are commonly tens of seconds)
to learn switch name, port, native VLAN, voice VLAN (LLDP-MED network policy) and PoE allocation. A native VLAN
difference between the two ends is logged by the switch.

## Gotchas
- Some NICs and drivers drop these frames before capture; if none arrive, try another NIC/driver setting or capture
  on the switch.
- BPDUs from a user port with BPDU guard should not exist; seeing them proves bpduguard is off.

## Verify
- [ ] Root bridge ID equals the core switch and TC counts stop increasing after enabling edge ports.

## Checked (2026-10-22)
- Built STP (config and topology-change BPDUs), CDP (device ID, port ID, native VLAN) and LLDP frames with scapy and ran on Wireshark 4.4.1: `stp.flags.tc == 1` matched 1, `stp.root.hw`/`stp.root.prio` returned 00:aa:00:00:00:01 / 32768, `stp.type == 0x02` matched 0 (the test BPDUs are type 0x00), `cdp.deviceid`/`cdp.portid`/`cdp.native_vlan` returned sw1.lab / GigabitEthernet0/1 / 10, `lldp.port.id` and `lldp.tlv.system.name` returned Gi0/1 / sw1.lab; all fields in the skill (including `stp.pvst.origvlan`, `lldp.ieee.802_1.port_vlan.id`, `lldp.ieee.802_3.mdi_power_support`) exist in `tshark -G fields`.
- Capture filters compiled with `dumpcap -i <Ethernet> -f "<filter>" -d` (they are invalid on the Npcap loopback adapter, which is not Ethernet): `stp` (bytecode: length-type <= 0x5dc and byte 14 == 0x42), `ether dst 01:00:0c:cc:cc:cd`, `ether host 01:00:0c:cc:cc:cc`, `ether proto 0x88cc`. The skill's old comment claiming `stp` is `ether dst 01:80:c2:00:00:00` was wrong. The Wireshark CDP wiki uses `ether host 01:00:0c:cc:cc:cc` (https://gitlab.com/wireshark/wireshark/-/wikis/CDP).
- Removed unverifiable Cisco syslog names and the fixed 60 s/30 s timers; the root-bridge and TC advice is interpretation, not tested on real switches.
