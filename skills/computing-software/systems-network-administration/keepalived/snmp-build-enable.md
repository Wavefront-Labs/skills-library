---
id: computing-software.systems-network-administration.keepalived.snmp-build-enable
name: snmp-build-enable
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, snmp, building, enable-snmp, net-snmp, configure]
level: practitioner
status: docs-checked
description: "Build Keepalived with SNMP support: install the Net-SNMP packages, pass --enable-snmp to configure, and confirm the configuration summary."
sources:
  - https://keepalived.readthedocs.io/en/latest/snmp_support.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building with SNMP support

1. Install the Net-SNMP packages first: `net-snmp`, `net-snmp-utils` and `net-snmp-libs`.
2. Run configure with the SNMP flag:
```
./configure --enable-snmp
```
3. Check the configuration summary: it should report "SNMP support : Yes" and list Net-SNMP libraries such as `-lnetsnmpagent` under Extra Lib.

At run time the daemon needs the `-x` / `--snmp` option to enable the SNMP subsystem, and snmpd must have AgentX enabled (see the AgentX skill).

Verify: the configure summary shows SNMP support Yes.

## Checked

2026-11-04. Confirmed the package names, --enable-snmp, the configuration summary lines and the AgentX requirement on the Configuring SNMP Support page, and the -x option on the programs synopsis page. Nothing removed.

Method: documentation only; no commands were run.
