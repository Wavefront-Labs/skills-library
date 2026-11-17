---
id: computing-software.cybersecurity-defensive.wazuh.active-response-server-config
name: active-response-server-config
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [active-response, command, location, timeout-allowed, rules-id, active-responses-log]
level: practitioner
status: docs-checked
description: "Configure Wazuh active response on the server with command and active-response blocks, choose location values safely, and find the per-OS script folders and logs."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/active-response/how-to-configure.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server configuration lives in `/var/ossec/etc/ossec.conf` inside `<ossec_config>`.

`<command>` block: `<name>`, `<executable>` and `<timeout_allowed>` (`yes` lets the action be reverted after a period). Out-of-the-box scripts already have command blocks; custom scripts need one added. Omit the file extension in `<executable>` unless several scripts share a name.

`<active-response>` block: `<disabled>`, `<command>` (must equal a command `<name>`), `<location>`, `<level>`, `<timeout>` in seconds, and `<agent_id>` (used with `defined-agent`). Triggers can be a rule ID, alert level or rule group.

`<location>` values: `local`, `server`, `defined-agent`, `all`. The page warns to use `all` with caution.

Apply with `sudo systemctl restart wazuh-manager`.

Endpoint side, custom scripts only:
- Linux/Unix: `/var/ossec/active-response/bin`, with `chmod 750` and `chown root:wazuh`.
- macOS: `/Library/Ossec/active-response/bin`, same permissions.
- Windows: `%ProgramFiles(x86)%\ossec-agent\active-response\bin`.

Logs: `/var/ossec/logs/active-responses.log` (Linux), `/Library/Ossec/logs/active-responses.log` (macOS), `%ProgramFiles(x86)%\ossec-agent\active-response\active-responses.log` (Windows). The page says execution results are written there.

## Checked

2026-11-03. Confirmed against the Wazuh page "How to configure Active Response": command and active-response blocks and their tags, the four location values and the caution on `all`, `<timeout>` in seconds, the manager restart, per-OS script directories with chmod 750 and chown root:wazuh, and the three log paths. Removed: the `<WAZUH_AGENT_DIR>` placeholder, the unsupported "check these first" advice, and the narrower "rule level or rule IDs" trigger wording.

Method: documentation only; no commands were run.
