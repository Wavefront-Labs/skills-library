---
id: computing-software.cybersecurity-defensive.wazuh.auditd-log-monitoring
name: auditd-log-monitoring
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [auditd, audit-keys, cdb-list, audit-log, system-calls, auditctl]
level: practitioner
status: docs-checked
description: "Monitor Linux system calls with Wazuh: auditd logs, audit-keys CDB list values, auditctl rules and the audit localfile."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/system-calls-monitoring/audit-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server side: the audit CDB list is `/var/ossec/etc/lists/audit-keys`. Each entry is `<KEY_NAME>:<VALUE>`. Valid values are `write` (`-p w`), `read` (`-p r`), `execute` (`-p x`), `attribute` (`-p a`) and `command` (system call rules). Defaults run from `audit-wazuh-w:write` through `audit-wazuh-c:command`.

Add a custom key:

```
echo "<YOUR_KEY>:<VALUE>" >> /var/ossec/etc/lists/audit-keys
```

Restart the manager after any CDB change with `systemctl restart wazuh-manager`. Out-of-the-box audit rules are in `/var/ossec/ruleset/rules/0365-auditd_rules.xml`.

Monitored endpoint:
1. Install `auditd` with `apt`, `yum` or `dnf`.
2. Add a `<localfile>` to `/var/ossec/etc/ossec.conf` with `<log_format>audit</log_format>` and `<location>/var/log/audit/audit.log</location>`.
3. Restart with `systemctl restart wazuh-agent`.
4. Create audit rules with `auditctl` or a rules file, using the same keys as the CDB list.

Gotcha: if `auditd` was installed before the Wazuh agent, skip the manual localfile step because the configuration is added by default. Linux audit alerts appear in the Threat Hunting module of the dashboard.

## Checked

2026-11-08: confirmed against the Wazuh docs page Monitoring system calls: Configuration (read in full): the audit-keys CDB list syntax, the five values and their -p flags, default keys, the echo append command, restart, the rules file 0365-auditd_rules.xml, auditd install, the localfile block, agent restart, and the note that auditd installed before the agent needs no manual step. Nothing removed.
Method: documentation only; no commands were run.
