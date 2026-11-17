---
id: computing-software.cybersecurity-defensive.wazuh.centralized-configuration-agent-conf
name: centralized-configuration-agent-conf
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [centralized-configuration, agent-conf, agent-config, verify-agent-conf, remote-conf]
level: practitioner
status: docs-checked
description: "Centralized Wazuh configuration with agent.conf: agent_config filters by name, os and profile, safe edit workflow with validation, push timing, and precedence over ossec.conf."
sources:
  - https://documentation.wazuh.com/current/user-manual/reference/centralized-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap settings in `<agent_config>`; the file is valid only on server installations. Put it in the group folder, for example `/var/ossec/etc/shared/group1/agent.conf`, readable by the `wazuh` user.

Filters: `name`, `os` and `profile` each take a regex, matching the agent name, OS info and the `config-profile` from client configuration. Run `agent_control -i <AGENT_ID>` to see an agent's name and OS.

Safe workflow:
1. Edit a temporary file such as `agent.conf.tmp` so an incomplete file is never distributed.
2. Validate: `/var/ossec/bin/verify-agent-conf -f <file>`.
3. Rename to `agent.conf`. The manager distributes it automatically; restarting the manager speeds this up.

Agents check the `merged.mg` checksum with each keepalive (10 seconds by default) and reload without a restart.

Verify rollout with `GET /agents` using `select=group_config_status`, or `agent_groups -S -i <ID>`.

Precedence: `ossec.conf` is read first and `agent.conf` values override it; file paths from both are kept.

Gotchas:
- Disable shared config on an agent with `agent.remote_conf=0` in `local_internal_options.conf`.
- Remote commands need `wazuh_command.remote_commands=1` in the agent's `local_internal_options.conf`.
- `files.yml` in `/var/ossec/etc/shared/` can download files from URLs on a poll interval.

## Checked

2026-11-03. Confirmed against the Wazuh page "Centralized configuration (agent.conf)": agent_config name/os/profile regex filters, server-only validity, group folder path and wazuh-readable requirement, agent_control -i, the agent.conf.tmp then verify-agent-conf then rename workflow, manager restart speeding distribution, 10-second keepalive and merged.mg checksum, group_config_status and `agent_groups -S -i`, precedence (ossec.conf first, file paths merged), `agent.remote_conf=0`, `wazuh_command.remote_commands=1`, and files.yml with poll. Nothing removed.

Method: documentation only; no commands were run.
