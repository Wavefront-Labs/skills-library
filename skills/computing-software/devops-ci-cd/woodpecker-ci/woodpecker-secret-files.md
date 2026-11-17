---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-secret-files
name: woodpecker-secret-files
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [file-secrets, docker-secrets, env-file]
level: practitioner
status: docs-checked
description: "Keep Woodpecker server secrets out of Compose files using the _FILE variable options."
sources: ["https://woodpecker-ci.org/docs/administration/installation/docker-compose"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker sensitive configuration via files

An `.env` file next to the Compose file separates configuration from secrets but is still not very secure. Docker secrets are awkward for environment variables, so Woodpecker accepts a `*_FILE` variant for all sensitive configuration variables. It reads the value from the file. If the original variable is also set, the original wins.

```yaml
services:
  woodpecker-server:
    environment:
      - WOODPECKER_AGENT_SECRET_FILE=/run/secrets/woodpecker-agent-secret
    secrets:
      - woodpecker-agent-secret

secrets:
  woodpecker-agent-secret:
    external: true
```

Create the Docker secret with:

```bash
echo "my_agent_secret_key" | docker secret create woodpecker-agent-secret -
```

Documented `_FILE` options include:

- `WOODPECKER_AGENT_SECRET_FILE` (server and agent)
- `WOODPECKER_GRPC_SECRET_FILE`
- `WOODPECKER_DATABASE_DATASOURCE_FILE`
- `WOODPECKER_PROMETHEUS_AUTH_TOKEN_FILE`
- forge credentials such as `WOODPECKER_GITHUB_CLIENT_FILE`, `WOODPECKER_GITHUB_SECRET_FILE`, `WOODPECKER_GITEA_SECRET_FILE`, `WOODPECKER_GITLAB_SECRET_FILE`

On the gRPC secret file: keep it persistent and readable only by the server.

The same pattern works for any sensitive server or agent variable, so credentials never appear in Compose files, process listings or version control. Remember the plain variable overrides the file when both are set.

## Checked

2026-11-03. Read the Woodpecker Docker Compose installation page and server configuration page and confirmed the *_FILE option for sensitive variables, the original variable winning when both are set, and the file-variant names listed. Removed: the Bitbucket Datacenter _FILE variables, which no fetched page documents. 

Method: documentation only; no commands were run.
