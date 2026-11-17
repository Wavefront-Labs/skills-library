---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-docker-compose-install
name: woodpecker-docker-compose-install
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [docker-compose, installation, deployment]
level: practitioner
status: docs-checked
description: "Deploy a Woodpecker server and Docker agent with Docker Compose, including ports and secrets."
sources: ["https://woodpecker-ci.org/docs/administration/installation/docker-compose"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Woodpecker with Docker Compose

Register an OAuth app with your forge first. The example connects to GitHub.

```yaml
services:
  woodpecker-server:
    image: woodpeckerci/woodpecker-server:v3
    ports:
      - 8000:8000
    volumes:
      - woodpecker-server-data:/var/lib/woodpecker/
    environment:
      - WOODPECKER_OPEN=true
      - WOODPECKER_HOST=${WOODPECKER_HOST}
      - WOODPECKER_GITHUB=true
      - WOODPECKER_GITHUB_CLIENT=${WOODPECKER_GITHUB_CLIENT}
      - WOODPECKER_GITHUB_SECRET=${WOODPECKER_GITHUB_SECRET}
      - WOODPECKER_AGENT_SECRET=${WOODPECKER_AGENT_SECRET}
  woodpecker-agent:
    image: woodpeckerci/woodpecker-agent:v3
    command: agent
    restart: always
    depends_on:
      - woodpecker-server
    volumes:
      - woodpecker-agent-config:/etc/woodpecker
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WOODPECKER_SERVER=woodpecker-server:9000
      - WOODPECKER_AGENT_SECRET=${WOODPECKER_AGENT_SECRET}
volumes:
  woodpecker-server-data:
  woodpecker-agent-config:
```

Key points:

- Persist `/var/lib/woodpecker`; the bundled SQLite database there holds all users and repositories.
- `WOODPECKER_HOST` is the public address as `<scheme>://<hostname>` with no trailing slash.
- HTTP uses port 8000; the agent connects to gRPC on 9000. Change them with `WOODPECKER_SERVER_ADDR` and `WOODPECKER_GRPC_ADDR`.
- Generate the shared secret with `openssl rand -hex 32`.
- For agents connecting over the internet set `WOODPECKER_GRPC_SECURE=true` on the agent.

The agent needs the Docker socket mounted so it can start step containers on the host. The agent config volume keeps the ID the server assigns to it. Pin the image tag rather than floating on a branch build.

## Checked

2026-11-03. Read the Woodpecker Docker Compose installation page and confirmed the server and agent Compose configuration and variables. Nothing removed. 

Method: documentation only; no commands were run.
