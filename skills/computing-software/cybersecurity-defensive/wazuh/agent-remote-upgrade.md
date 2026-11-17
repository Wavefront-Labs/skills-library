---
id: computing-software.cybersecurity-defensive.wazuh.agent-remote-upgrade
name: agent-remote-upgrade
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [agent-upgrade, remote-upgrade, outdated-agents, upgrade-result, wait-for-complete]
level: practitioner
status: docs-checked
description: "Upgrade Wazuh agents remotely from the server with agent_upgrade or the API: list outdated agents, create upgrade tasks, check results, and large-fleet timeouts."
sources:
  - https://documentation.wazuh.com/current/user-manual/agent/agent-management/remote-upgrading/upgrading-agent.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CLI on the Wazuh server:
- `/var/ossec/bin/agent_upgrade -l` lists outdated agents.
- `/var/ossec/bin/agent_upgrade -a <ID> [ID...]` upgrades one or more agents.
- `/var/ossec/bin/agent_control -i <ID>` confirms the client version afterwards.

RESTful API (port 55000, Bearer token required):
- `GET /agents/outdated` lists outdated agents.
- `PUT /agents/upgrade?agents_list=...` creates upgrade tasks.
- `GET /agents/upgrade_result?agents_list=...` checks task status (for example "Updated").
- `GET /agents?agents_list=...&select=version` confirms versions.

Notes:
- The docs recommend the API over the CLI for Wazuh clusters.
- `agents_list=all` upgrades every agent.
- With more than 3000 agents, set `wait_for_complete=true` to avoid API timeouts.
- Agents restart automatically after upgrading.
- The page examples use `curl -k`, which skips certificate verification; supply the CA in production.

## Checked

2026-11-03. Confirmed against the Wazuh page "Upgrading the Wazuh agent": `agent_upgrade -l` and `-a`, `agent_control -i`, the API endpoints GET /agents/outdated, PUT /agents/upgrade, GET /agents/upgrade_result and GET /agents with select=version, the cluster recommendation, `agents_list=all`, the 3000-agent `wait_for_complete=true` advice, and automatic restart. Removed: the "failure mode" about asynchronous upgrades and polling (not on the page).

Method: documentation only; no commands were run.
