---
id: computing-software.cybersecurity-defensive.wazuh.agent-groups-cli
name: agent-groups-cli
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [agent-groups-tool, agent-groups-flags, sync-status, group-removal]
level: intro
status: docs-checked
description: "Reference for the Wazuh agent_groups command: flags to list, create, remove, assign and replace groups, show an agent's groups, and check shared-file sync status."
sources:
  - https://documentation.wazuh.com/current/user-manual/reference/tools/agent-groups.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`/var/ossec/bin/agent_groups` flags:
- `-h` help; `-q` quiet (no confirmation output); `-d` debug output.
- `-l` list all groups.
- `-l -g ID` list agents in a group.
- `-c -g ID` list configuration files in a group.
- `-a -g ID [-q]` create a group.
- `-r -g ID [-q]` remove a group, affecting agents assigned to it.
- `-a -i AGENT -g ID [-q]` add a group to an agent's group list.
- `-a -f -i AGENT -g ID [-q]` replace an agent's groups with the given group.
- `-r -i AGENT [-q]` remove an agent from all groups, returning it to `default`.
- `-r -i AGENT -g ID [-q]` remove an agent from one group.
- `-s -i AGENT` show an agent's groups.
- `-S -i AGENT` show an agent's shared-file sync status.

Examples from the page:
- `agent_groups -a -g debian` creates group `debian`.
- `agent_groups -a -i 002 -g debian` assigns it to agent 002.
- `agent_groups -s -i 002` shows agent 002's groups.
- `agent_groups -l -g debian` lists agents in `debian`.

Gotcha: `-r -g ID` removes a whole group and impacts every agent in it, whereas `-r -i AGENT -g ID` only detaches one agent. `-S -i AGENT` shows an agent's shared-file sync status.

## Checked

2026-11-03. Confirmed against the Wazuh page "agent_groups": every flag combination in the list above and the four examples. Removed: the claim that `-S` is the way to confirm an edited group agent.conf arrived (the page only says it shows the shared-file sync status). The centralized configuration page separately shows `agent_groups -S -i` and `group_config_status` for checking sync.

Method: documentation only; no commands were run.
