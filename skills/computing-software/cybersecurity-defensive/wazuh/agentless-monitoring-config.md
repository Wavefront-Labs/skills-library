---
id: computing-software.cybersecurity-defensive.wazuh.agentless-monitoring-config
name: agentless-monitoring-config
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [agentless, ssh-integrity-check, periodic-diff, expect, use-su]
level: practitioner
status: docs-checked
description: "Configure Wazuh agentless monitoring over SSH: agentless blocks, type values, periodic vs periodic_diff, use_su and the expect prerequisite."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/agentless-monitoring/agentless-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Agentless checks run from the Wazuh server, so devices need no agent. Install `expect` as root first: `yum install -y expect` (RHEL-based) or `apt install -y expect` (Debian-based).

Add `<agentless>` blocks to `/var/ossec/etc/ossec.conf` on the server with these tags:
- `type`: `ssh_integrity_check_bsd`, `ssh_integrity_check_linux`, `ssh_pixconfig_diff` or `ssh_generic_diff`.
- `frequency`: integer seconds.
- `host`: `username@hostname`.
- `state`: `periodic` (output analysed with the ruleset as a log) or `periodic_diff` (output compared to the previous run, alerting on changes).
- `arguments`: space-delimited files or directories for integrity checks, or a command for generic diff.

Page examples: BSD with `frequency` 20000 and `arguments` `/bin /var/`; Linux with `frequency` 36000 and `/bin /etc /sbin`; PIX with host `pix@pix.fw.local` and `periodic_diff`; generic diff with `ls -la /etc` and `periodic_diff`.

Using `su`: place `use_su` before the host, for example `<host>use_su user@test.com</host>`.

Apply with `systemctl restart wazuh-manager`. A successful check logs a line like `Test passed for 'ssh_integrity_check_linux'` in `/var/ossec/logs/ossec.log`.

The page gives no default values for `frequency` or `state`, so always set them.

## Checked

2026-11-08: confirmed against the Wazuh docs page Agentless monitoring: Configuration (read in full): expect install commands, the attribute table (type values, frequency, host, state, arguments), the four example configurations and values, the use_su note, the restart command and the ossec.log success message. Nothing removed.
Method: documentation only; no commands were run.
