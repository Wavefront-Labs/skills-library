---
id: computing-software.cybersecurity-defensive.wazuh.agent-groups-and-shared-files
name: agent-groups-and-shared-files
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [agent-groups, shared-files, merged-mg, default-group, guess-agent-group]
level: practitioner
status: docs-checked
description: "Group Wazuh agents and distribute shared config: default group, per-group agent.conf, multi-group precedence, merged.mg locations, and re-enrollment group loss."
sources:
  - https://documentation.wazuh.com/current/user-manual/agent/agent-management/grouping-agents.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Unassigned agents join the `default` group, whose files live in `/var/ossec/etc/shared/default/`. Each group's config is `/var/ossec/etc/shared/<GROUP_NAME>/agent.conf`, empty by default.

Commands (root, on the server):
- Create: `/var/ossec/bin/agent_groups -a -g <GROUP> -q`
- List groups: `/var/ossec/bin/agent_groups -l`
- Assign: `/var/ossec/bin/agent_groups -a -i 002 -g dbms`
- Members: `/var/ossec/bin/agent_groups -l -g dbms`
- An agent's groups: `/var/ossec/bin/agent_groups -s -i 001`
- Remove: `/var/ossec/bin/agent_groups -r -i 001 -g apache -q`
- Replace all groups: `/var/ossec/bin/agent_groups -a -f -i 001 -g apache`
- Enroll into groups: `agent-auth -m <MANAGER_IP> -G webserver,apache`

Multiple groups: agents receive files from every group. For same-named shared files the last one added overwrites earlier ones; `agent.conf` files are appended, and on conflicts the most recently assigned group wins.

`merged.mg` is at `/var/ossec/etc/shared/merged.mg` on server and Linux agent, and `%ProgramFiles(x86)%\ossec-agent\shared\merged.mg` on Windows.

Gotchas:
- The group must exist before you assign agents.
- Group names allow only letters, numbers, dots, underscores and hyphens.
- Re-enrolled agents return to `default` unless `remoted.guess_agent_group=1` is set in `/var/ossec/etc/local_internal_options.conf`.
- Push time depends on file size, number of agents and protocol. The page's example: it may take 8 minutes to receive a 10 MB folder (excluding merged.mg) on 100 agents using UDP, and less with TCP.

## Checked

2026-11-03. Confirmed against the Wazuh page "Grouping agents": default group and shared folders, agent_groups commands (-a -g -q, -l, -a -i -g, -l -g, -s -i, -r -i -g -q, -a -f), `agent-auth -G`, multi-group precedence and shared-file merging, group name rules, remoted.guess_agent_group=1, and the merged.mg locations. Removed: the `<WAZUH_AGENT_DIR>` placeholder and the "pushing is slow" paraphrase of the timing example.

Method: documentation only; no commands were run.
