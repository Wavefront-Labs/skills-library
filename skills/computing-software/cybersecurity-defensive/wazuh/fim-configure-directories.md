---
id: computing-software.cybersecurity-defensive.wazuh.fim-configure-directories
name: fim-configure-directories
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [syscheck, directories, fim, file-integrity, wildcards, restart]
level: intro
status: docs-checked
description: "Add files and directories to Wazuh FIM with directories entries in the syscheck block, using the right agent config path, wildcards and restart command per OS."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/how-to-configure-fim.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
File integrity monitoring (FIM) is configured inside the `<syscheck>` block. Each monitored file or directory gets a `<directories>` entry, or several paths can be comma separated in one tag.

Where to configure: the agent `ossec.conf`, the server configuration, or centralized configuration (`agent.conf`).
- Linux agent: `/var/ossec/etc/ossec.conf`
- Windows agent: `%ProgramFiles(x86)%\ossec-agent\ossec.conf`
- macOS agent: `/Library/Ossec/etc/ossec.conf`

Wildcards `*` and `?` behave as in a shell or cmd terminal, for example a `\Users\*\Downloads` path on the system drive.

Apply the change by restarting the agent with administrator rights:
- Linux: `systemctl restart wazuh-agent`
- Windows: `Restart-Service -Name wazuh`
- macOS: `/Library/Ossec/bin/wazuh-control restart`

Failure modes:
- If the same directory is set in both centralized configuration and local `ossec.conf`, the centralized setting takes precedence, so a local edit can appear to do nothing.
- From Wazuh 4.13.0, Windows UNC network paths and mapped network drives are not supported. Only local paths are monitored.
- Edits do not take effect until the agent restarts.

## Checked

2026-11-03. Confirmed against the Wazuh pages "How to configure the FIM module" and "Basic settings": `<syscheck>`/`<directories>` usage, comma-separated or multi-line entries, `*` and `?` wildcards, config locations per OS, restart commands, centralized-over-local precedence, and the 4.13.0 UNC/mapped-drive restriction. Removed: the `<WAZUH_AGENT_DIR>` and `<USER_PROFILES>` placeholders (the page gives concrete paths).

Method: documentation only; no commands were run.
