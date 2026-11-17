---
id: computing-software.cybersecurity-defensive.wazuh.sca-policy-management
name: sca-policy-management
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [sca, security-configuration-assessment, policies, remote-commands, agent-conf]
level: practitioner
status: docs-checked
description: "Control which Wazuh SCA policies run: ruleset folders, disabling a policy, and pushing policies from the server with sca.remote_commands."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/how-to-configure.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default each agent scans every `.yaml` or `.yml` file in its SCA ruleset folder: `/var/ossec/ruleset/sca` (Linux/Unix), `ruleset\sca` in the agent install directory (`ossec-agent` under Program Files (x86) by default, Windows), `/Library/Ossec/ruleset/sca` (macOS). Installs and updates do not preserve those folders, so keep custom policies elsewhere.

Disable a policy by renaming the file to an extension other than `.yaml`/`.yml`, or set `enabled="no"` on a `<policy>` element inside `<sca><policies>` in `ossec.conf`. Paths are relative to the install directory (for example `ruleset/sca/FILE`); centralized policies use `etc/shared/FILE` (`shared\FILE` on Windows), and an absolute path also works. Restart with `systemctl restart wazuh-agent`.

Push a policy from the server:
1. Agent: add `sca.remote_commands=1` to `local_internal_options.conf` (remote commands are disabled by default as a security measure; on Linux the file is `/var/ossec/etc/local_internal_options.conf`).
2. Server: place the file in `/var/ossec/etc/shared/default/` and run `chown wazuh:wazuh` on it.
3. Server: in `/var/ossec/etc/shared/default/agent.conf` add an `<agent_config><sca><policies><policy>` entry pointing at `etc/shared/<NEW_POLICY_FILE>`.

The agent saves pushed files in `etc/shared/` (Linux, macOS) or `shared\` (Windows) regardless of group, which is why a relative path is used. The pushed `<sca>` block merges with the agent-side one.

Note: remote commands need not be enabled if you add the policy file to each agent yourself (for example with scp). Enabling them lets the server execute commands on the monitored endpoint.

## Checked

2026-11-08: confirmed against the Wazuh docs page How to configure SCA (read in full): default ruleset folders, non-preserved folders, the two ways to disable a policy, relative and shared paths, restart commands, sca.remote_commands, chown, the agent.conf block, the shared directory and merge behaviour. Removed the unsupported failure-mode claim that the agent will not run pushed policies, and replaced it with the documented note.
Method: documentation only; no commands were run.
