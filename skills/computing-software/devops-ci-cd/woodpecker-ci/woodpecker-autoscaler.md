---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-autoscaler
name: woodpecker-autoscaler
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [autoscaler, cloud-agents, hetzner]
level: advanced
status: docs-checked
description: "Scale Woodpecker agents on demand with the autoscaler container."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/autoscaler"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker autoscaler

The autoscaler is a separate project (woodpecker-ci/autoscaler) that scales agents with load. It is not feature-complete yet; progress is tracked in its roadmap.

Docker Compose setup next to the server:

```yaml
services:
  woodpecker-autoscaler:
    image: woodpeckerci/autoscaler:next
    restart: always
    depends_on:
      - woodpecker-server
    environment:
      - WOODPECKER_SERVER=https://your-woodpecker-server.tld
      - WOODPECKER_TOKEN=${WOODPECKER_TOKEN}
      - WOODPECKER_MIN_AGENTS=0
      - WOODPECKER_MAX_AGENTS=3
      - WOODPECKER_WORKFLOWS_PER_AGENT=2
      - WOODPECKER_GRPC_ADDR=grpc.your-woodpecker-server.tld
      - WOODPECKER_GRPC_SECURE=true
      - WOODPECKER_AGENT_ENV=
      - WOODPECKER_PROVIDER=hetznercloud
      - WOODPECKER_HETZNERCLOUD_API_TOKEN=${WOODPECKER_HETZNERCLOUD_API_TOKEN}
```

Notes:

- `WOODPECKER_TOKEN` is the API token from your user page in the Woodpecker UI.
- `WOODPECKER_GRPC_ADDR` is the server's gRPC address, publicly reachable by agents, without `https://`. Use a reverse proxy to expose it, such as the Caddy example.
- `WOODPECKER_WORKFLOWS_PER_AGENT` is how many workflows each agent runs at once.
- `WOODPECKER_AGENT_ENV` passes optional environment variables to the agents.
- `WOODPECKER_PROVIDER` selects the cloud provider.

VMs are destroyed after the builds finish, after a short transition time. Agents it creates can use `WOODPECKER_AGENT_SINGLE_WORKFLOW` for one-shot machines.

## Checked

2026-11-03. Read the Woodpecker autoscaler page and confirmed autoscaler behaviour and settings described in the skill. Nothing removed. 

Method: documentation only; no commands were run.
