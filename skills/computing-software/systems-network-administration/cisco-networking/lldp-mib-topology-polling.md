---
id: computing-software.systems-network-administration.cisco-networking.lldp-mib-topology-polling
name: lldp-mib-topology-polling
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, snmp, lldp, lldp-mib, lldp-rem-table, topology-discovery, network-mapping, snmpwalk, ieee8021-lldp]
level: practitioner
status: docs-checked
description: "Poll LLDP-MIB (lldpRemTable, lldpLocPortTable) over SNMP to build a topology map, decode the index structure and handle port ID subtypes."
sources:
  - https://www.ieee802.org/1/files/public/MIBs/LLDP-MIB-200505060000Z.txt
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg/configuring_lldp__lldp_med__and_wired_location_service.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polling LLDP-MIB for topology

## Key tables (LLDP-MIB, OID 1.0.8802.1.1.2)
Tree: lldpObjects is `.1`, lldpLocalSystemData `.1.3`, lldpRemoteSystemsData `.1.4`.

| Object | OID | Content |
|---|---|---|
| lldpLocChassisId | 1.0.8802.1.1.2.1.3.2 | this device's chassis ID |
| lldpLocPortTable | 1.0.8802.1.1.2.1.3.7 | local port number -> port ID subtype, ID, description |
| lldpRemTable | 1.0.8802.1.1.2.1.4.1 | neighbours |
| lldpRemChassisId | ...1.4.1.1.5 | neighbour chassis ID |
| lldpRemPortId | ...1.4.1.1.7 | neighbour port ID |
| lldpRemPortDesc | ...1.4.1.1.8 | neighbour port description |
| lldpRemSysName | ...1.4.1.1.9 | neighbour system name |
| lldpRemManAddrTable | ...1.4.2 | neighbour management addresses |

Columns of the local port entry: lldpLocPortIdSubtype `.2`, lldpLocPortId `.3`, lldpLocPortDesc `.4`
(so `1.0.8802.1.1.2.1.3.7.1.3` is lldpLocPortId).

lldpRemTable index = `lldpRemTimeMark.lldpRemLocalPortNum.lldpRemIndex`.
- lldpRemTimeMark is an RFC 2021 TimeFilter.
- lldpRemLocalPortNum is the **local** port component index, the same index as lldpLocPortTable
  (lldpLocPortNum). The MIB defines it as an index value, not as an ifIndex.
- lldpRemIndex is an arbitrary local integer identifying the connection instance.

## Walk it
Walk `1.0.8802.1.1.2.1.4.1.1.9` for neighbour system names and `1.0.8802.1.1.2.1.3.7.1.3` for the
local port IDs, with SNMPv3 authPriv credentials of a read-only user. Join on
lldpRemLocalPortNum -> lldpLocPortId/lldpLocPortDesc to get "local port X connects to
<SysName> port Y".

## Gotchas
- Port ID subtype (`lldpRemPortIdSubtype`) varies: macAddress(3), interfaceName(5), local(7).
  Normalise before matching both sides.
- Chassis ID subtypes include macAddress(4), interfaceName(6) and local(7), so do not assume the
  chassis ID is a MAC; check `lldpRemChassisIdSubtype`. A MAC arrives as an octet string.
- LLDP must be running on the switch (`lldp run`; disabled globally by default).

## Verify
- [ ] For a known link, both switches' lldpRemTable show each other with matching ports.
- [ ] Map edges are symmetric (A sees B and B sees A); investigate any asymmetric edge.

## Checked
2026-11-08. Confirmed against LLDP-MIB-200505060000Z from the IEEE 802.1 site: OID tree, every
object and column number in the table above, the lldpRemTable INDEX, lldpLocPortTable INDEX
(lldpLocPortNum), TimeFilter and subtype enumerations. Cisco Catalyst 9300 17.9 LLDP chapter for
"disabled globally by default" and `lldp run`. Removed unsupported claims: IEEE8021-LLDP-V2-MIB
OID, SNMP view requirement, do-not-cache advice, snmpwalk flag string, "newer devices"
statement. Cisco guide URL replaced (old one 404s).
Method: documentation only; no commands were run.
