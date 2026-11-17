---
id: computing-software.cybersecurity-defensive.wazuh.agent-enrollment-password
name: agent-enrollment-password
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [use-password, authd-pass, enrollment, agent-auth, authorization-pass-path]
level: practitioner
status: docs-checked
description: "Require a password for Wazuh agent enrollment: auth use_password on the manager, authd.pass file permissions, random password lookup, and per-OS agent paths."
sources:
  - https://documentation.wazuh.com/current/user-manual/agent/agent-enrollment/security-options/using-password-authentication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Manager (`/var/ossec/etc/ossec.conf`): add `<auth><use_password>yes</use_password></auth>`. Recommended: create `/var/ossec/etc/authd.pass` containing the password, `chmod 640` and `chown root:wazuh`, then `systemctl restart wazuh-manager`.

If you omit the file, the enrollment service generates a random password at each manager restart. Find it with `grep "Random password" /var/ossec/logs/ossec.log`. In a multi-node cluster, enable it on every manager node, ideally with the same password.

Agents:
- Linux/Unix: create `/var/ossec/etc/authd.pass`, mode 640, owner root:wazuh. Optionally set `<enrollment><authorization_pass_path>` if the file is elsewhere. Set the manager in `<client><server><address>`. Restart with `systemctl restart wazuh-agent`.
- Windows (elevated PowerShell): `%ProgramFiles(x86)%\ossec-agent\authd.pass` (64-bit systems) or `%ProgramFiles%\ossec-agent\authd.pass` (32-bit systems). Restart with `Restart-Service -Name wazuh` or `net stop wazuh` then `net start wazuh`.
- macOS: `/Library/Ossec/etc/authd.pass`, mode 640, owner root:wazuh; config `/Library/Ossec/etc/ossec.conf`; restart with `/Library/Ossec/bin/wazuh-control restart`.

Verify in the dashboard under Agents management, Summary.

Failure mode: a random per-restart password means agents enrolling after a manager restart need the new value, so a fixed `authd.pass` is more predictable.

## Checked

2026-11-03. Confirmed against the Wazuh page "Using password authentication": the `<auth><use_password>` setting, authd.pass creation with chmod 640 and chown root:wazuh, the random password logged to ossec.log and the grep, the multi-node note, `authorization_pass_path`, the `<client><server><address>` setting, per-OS restart commands and the dashboard check. Removed: the `<WAZUH_AGENT_DIR>` placeholders (the page gives the real 64-bit and 32-bit directories).

Method: documentation only; no commands were run.
