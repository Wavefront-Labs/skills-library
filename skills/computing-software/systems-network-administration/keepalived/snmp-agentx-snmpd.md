---
id: computing-software.systems-network-administration.keepalived.snmp-agentx-snmpd
name: snmp-agentx-snmpd
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, snmp, agentx, snmpd, snmpd-conf]
level: practitioner
status: docs-checked
description: "Enable AgentX in snmpd so Keepalived can register: add master agentx to snmpd.conf, restart snmpd, and start keepalived with the snmp option."
sources:
  - https://keepalived.readthedocs.io/en/latest/snmp_support.html
  - https://keepalived.readthedocs.io/en/latest/programs_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# snmpd AgentX configuration

Keepalived's SNMP support needs AgentX enabled in the SNMP daemon.

1. Add this line to the snmpd configuration (typically /etc/snmp/snmpd.conf on CentOS RPM installs):
```
master agentx
```
2. Reload or restart snmpd so the change takes effect.
3. Start keepalived with `-x` (long form `--snmp`), which enables the SNMP subsystem. The build must have been configured with `--enable-snmp`.

Verify: an snmpwalk of the Keepalived base OID returns data (see the MIB and OID skill).

## Checked

2026-11-04. Confirmed the master agentx line, the typical snmpd.conf location, the reload note and --enable-snmp on the Configuring SNMP Support page, and -x and --snmp on the programs synopsis page. Removed the subagent description, which the pages do not state.

Method: documentation only; no commands were run.
