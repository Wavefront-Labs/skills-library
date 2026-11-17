---
id: computing-software.systems-network-administration.zabbix.snmp-trap-receiving
name: snmp-trap-receiving
category: computing-software
field: systems-network-administration
product: zabbix
tags: [snmptrap, snmptrapd, snmptrapperfile, startsnmptrapper, snmp-fallback, trapper]
level: advanced
status: docs-checked
description: "Receive SNMP traps through snmptrapd and a receiver script into trap file items on a server or proxy."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/snmptrap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zabbix collects traps from a file rather than listening for them itself. The flow is: the device sends a trap to snmptrapd; snmptrapd passes it to a receiver (a Bash script, a Perl script, or SNMPTT); the receiver appends it to a trap file; the Zabbix SNMP trapper process reads that file and matches each trap to items on the host interface.

Server or proxy configuration:
StartSNMPTrapper=1
SNMPTrapperFile=<path to the trap file>

The trap file must be the one the receiver writes.

Items use the SNMP trap item type with these keys:
- snmptrap[regexp]: catches traps matching the regular expression; with no regexp it catches any trap.
- snmptrap.fallback: catches traps for that interface not caught by any snmptrap[] item.

For each trap, Zabbix finds items on the host whose interface matches the sender address and compares the trap text to each snmptrap[regexp]; unmatched traps go to the fallback item if present.

Receiver choice: the Bash script solution is the simplest to set up, but for better performance on production systems the docs recommend the embedded Perl solution (a script with the do perl option, or SNMPTT).

Because traps depend on the interface address, make sure the trap source IP matches the host interface in Zabbix. Multiline regular expression matching is not supported, and if no item matches a trap, Zabbix logs the unmatched trap by default.

## Checked

2026-11-09. Confirmed against the Zabbix manual page SNMP trap (current): the trap workflow, receiver options, StartSNMPTrapper and SNMPTrapperFile settings, snmptrap[regexp] and snmptrap.fallback behaviour, interface address matching, the unmatched-trap logging default and the multiline limitation.

Method: documentation only; no commands were run.
