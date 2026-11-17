---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-agent-registration-and-filters
name: woodpecker-agent-registration-and-filters
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [agent-token, agent-filters, organization-agents]
level: sme
status: docs-checked
description: "Register Woodpecker agents with system or agent tokens and restrict them with server-side filters."
sources:
  - https://woodpecker-ci.org/docs/administration/configuration/agent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker agent registration and filters

Registration: an agent connects with the token in `WOODPECKER_AGENT_SECRET`.

- System token: the same value on server and agents. On first contact the server registers the agent and returns a unique ID, which the agent stores in `WOODPECKER_AGENT_CONFIG_FILE`. Later startups use the system token and the ID.
- Agent token: unique to one agent. An administrator registers it in the UI at `Settings -> Agents -> Add agent` and gives the generated token to the agent via `WOODPECKER_AGENT_SECRET`.

Agent filters: labels from `WOODPECKER_AGENT_LABELS` are self-reported, so an agent can claim any label and they cannot restrict what it picks up. Agent filters are stored in the server database, applied whenever the agent asks for work, and invisible to the agent. Syntax matches labels:

- `key=value` matches workflows whose label `key` is `value`
- `key=*` matches any value
- `!key=value` additionally requires the workflow to have that label

Manage filters in the UI: instance agents at `Settings -> Agents`, organization agents at `Organization settings -> Agents`, personal agents at `User settings -> Agents`. A filter wins over a reported label with the same key. Changes apply next time the agent requests work. Organization and personal agents always get an `org-id` filter enforced.

Organization agents only: enabling it means instance-wide agents never pick up that organization's workflows. If no organization agent is online they stay pending. It applies to pipelines started afterwards.

## Checked

2026-11-08. Read the Woodpecker Agent configuration page (registration, filters, organization agents only, environment variables) in full and confirmed every claim; nothing was removed.

Method: documentation only; no commands were run.
