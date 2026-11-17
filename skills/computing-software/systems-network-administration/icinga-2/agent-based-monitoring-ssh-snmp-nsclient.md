---
id: computing-software.systems-network-administration.icinga-2.agent-based-monitoring-ssh-snmp-nsclient
name: agent-based-monitoring-ssh-snmp-nsclient
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, agent-based, check-by-ssh, by-ssh, snmp, snmptt, nsclient]
level: practitioner
status: docs-checked
description: Monitor hosts without the Icinga agent using check_by_ssh with the by_ssh CheckCommand, SNMP checks with snmp_oid and snmp_miblist, SNMPTT trap passive results, and NSClient++.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/07-agent-based-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent-based monitoring: SSH, SNMP, NSClient++
The Icinga agent is the recommended choice on Linux/Unix and Windows. Alternatives exist when it is unavailable.

**SSH** (recommended where the Icinga agent is not available): the `check_by_ssh` plugin, wrapped by the ITL `by_ssh` CheckCommand, runs a plugin on the remote host.
- Create a key pair for the Icinga daemon user without a passphrase, create an `icinga` user on the remote host, copy the public key (for example `ssh-copy-id`).
- Connect once and accept the host key, otherwise checks go UNKNOWN.
- Permissions: `.ssh` 700, `id_rsa.pub` 644, `id_rsa` 600.
- Mark hosts with a custom variable such as `vars.agent_type = "ssh"` and use `by_ssh_command` plus `by_ssh_arguments` in an apply rule.

**SNMP**: use the `snmp` CheckCommand with `snmp_oid`, and a service assigned where `host.vars.snmp_community != ""`. Always set `snmp_miblist`; without it the plugin defaults to `ALL`, and load grows with the number of MIB files.

**SNMP traps**: receive and filter with SNMPTT; its `EXEC` line writes a `PROCESS_SERVICE_CHECK_RESULT` external command into the command pipe, giving passive results.

**Windows**: NSClient++ or WMI; the Icinga agent can query a local NSClient++ when no plugin exists.

## Checked

2026-11-04. Confirmed against the Icinga 2 agent-based monitoring chapter: SSH by_ssh setup, SNMP snmp_miblist advice, SNMPTT passive results, NSClient++.

Method: documentation only; no commands were run.
