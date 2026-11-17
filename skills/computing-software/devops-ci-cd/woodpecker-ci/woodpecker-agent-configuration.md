---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-agent-configuration
name: woodpecker-agent-configuration
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [agent, max-workflows, agent-config]
level: practitioner
status: docs-checked
description: "Configure a Woodpecker agent: server address, secret, parallel workflows, labels and healthcheck."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/agent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker agent configuration

The minimum agent configuration:

```ini
WOODPECKER_SERVER=localhost:9000
WOODPECKER_AGENT_SECRET="your-shared-secret-goes-here"
```

Set automatically and overridable: `WOODPECKER_HOSTNAME` (the OS hostname) and `WOODPECKER_MAX_WORKFLOWS` (1).

Settings:

- `WOODPECKER_MAX_WORKFLOWS` parallel workflows on this agent.
- `WOODPECKER_AGENT_SINGLE_WORKFLOW` (default false) makes the agent exit after one workflow and forces max workflows to 1, for ephemeral machines such as those an autoscaler provisions.
- `WOODPECKER_AGENT_LABELS` custom labels like `key=value,second-key=*`; a `!` key prefix makes the label mandatory on the workflow. Defaults: `platform`, `hostname`, `backend`, `repo=*`.
- `WOODPECKER_BACKEND`: `auto-detect` (default), `docker`, `local` or `kubernetes`.
- `WOODPECKER_AGENT_CONFIG_FILE` (default `/etc/woodpecker/agent.conf`) where the agent stores its assigned ID.
- `WOODPECKER_HEALTHCHECK` (true) and `WOODPECKER_HEALTHCHECK_ADDR` (`:3000`).
- `WOODPECKER_RETRY_TIMEOUT` (`2m`): how long to keep reconnecting; 0 retries forever.
- `WOODPECKER_LOG_ENTRY_STREAM_BUFFER_SIZE` (100) log lines buffered before blocking.
- `WOODPECKER_CONNECT_RETRY_COUNT` (5) and `WOODPECKER_CONNECT_RETRY_DELAY` (`2s`).

Backend settings use `WOODPECKER_BACKEND_DOCKER_*`, `WOODPECKER_BACKEND_K8S_*` and `WOODPECKER_BACKEND_LOCAL_*`.

Run several agents when you need different backends or labels per machine, and give each its own config file location so IDs do not collide. Check the healthcheck port is free on hosts running more than one agent.

## Checked

2026-11-03. Read the Woodpecker agent configuration page and confirmed minimum agent settings, AGENT_LABELS including the ! mandatory prefix and default labels, BACKEND values, healthcheck, retry and log buffer settings, BACKEND_DOCKER_*, BACKEND_K8S_* and BACKEND_LOCAL_* groups. Nothing removed. 

Method: documentation only; no commands were run.
