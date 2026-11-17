---
id: computing-software.cybersecurity-defensive.wazuh.active-response-default-scripts
name: active-response-default-scripts
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [firewall-drop, host-deny, disable-account, route-null, netsh, default-scripts]
level: intro
status: docs-checked
description: "List the active response scripts shipped with Wazuh agents on Linux, macOS, Unix and Windows, what each does, and the dependencies each one requires."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/active-response/default-active-response-scripts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default scripts live in `/var/ossec/active-response/bin` (Linux/Unix), `/Library/Ossec/active-response/bin` (macOS) and `%ProgramFiles(x86)%\ossec-agent\active-response\bin` (Windows).

Linux, macOS and Unix:
- `disable-account`: disables a user account.
- `firewall-drop`: adds an IP to the iptables deny list.
- `firewalld-drop`: adds an IP to the firewalld drop list; needs firewalld.
- `host-deny`: adds an IP to `/etc/hosts.deny`.
- `ip-customblock`: a custom block meant to be modified.
- `ipfw`, `npf`, `pf`: firewall-drop variants, each needing its firewall installed.
- `wazuh-slack`: posts Slack notifications; needs a Slack hook URL in `extra_args`.
- `restart.sh`, `restart-wazuh`: restart the agent or manager.
- `route-null`: adds an IP to a null route.
- `kaspersky`: integrates with Kaspersky Endpoint Security for Linux CLI.

Windows:
- `netsh.exe`: blocks an IP with `netsh`.
- `restart-wazuh.exe`: restarts the agent.
- `route-null.exe`: adds an IP to a null route.

Failure modes:
- Firewall-specific scripts (`firewalld-drop`, `ipfw`, `npf`, `pf`) require the matching firewall installed on the endpoint.
- `wazuh-slack` requires a Slack hook URL passed as `extra_args`.
- A script is only used once a `<command>` and `<active-response>` pair on the server references it.

## Checked

2026-11-03. Confirmed against the Wazuh page "Default active response scripts": every script name and description above, the Linux/Unix, macOS and Windows directories, and the stated requirements (firewalld, IPFW, NPF, PF, Slack hook URL in extra_args, Kaspersky Endpoint Security for Linux CLI). Removed: the `<WAZUH_AGENT_DIR>` placeholder (the page gives the concrete Windows path) and the unsupported "fail silently" wording. The last bullet follows the "How to configure Active Response" page (command and active-response blocks).

Method: documentation only; no commands were run.
