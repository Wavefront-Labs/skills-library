---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-grpc-and-agent-secrets
name: woodpecker-grpc-and-agent-secrets
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [grpc, agent-secret, jwt, ha]
level: advanced
status: docs-checked
description: "Configure Woodpecker gRPC listeners and the secrets that authenticate agents."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker gRPC and agent secrets

Agents talk to the server over gRPC. Relevant server settings:

- `WOODPECKER_GRPC_ADDR` (default `:9000`): bind to a specific interface, such as `localhost:9000`, or use a unix socket with the `unix://` prefix.
- `WOODPECKER_AGENT_SECRET`: shared secret for server and agents, generated with `openssl rand -hex 32`. `WOODPECKER_AGENT_SECRET_FILE` reads it from a file.
- `WOODPECKER_GRPC_SECRET`: the secret used to sign JWTs for gRPC connections. If empty, the server generates a temporary one and logs a warning; it is not persisted and changes on each restart. Set it explicitly, especially for high availability setups with multiple servers. `WOODPECKER_GRPC_SECRET_FILE` reads it from a file.
- `WOODPECKER_KEEPALIVE_MIN_TIME`: minimum time a client should wait before sending keepalive pings, for example `10s`.

After the gRPC secret is rotated, connected agents reauthenticate when the server rejects their old token. They do not need a restart as long as `WOODPECKER_AGENT_SECRET` is unchanged.

Agent-side TLS: `WOODPECKER_GRPC_SECURE` (default false) turns on a secure transport; `WOODPECKER_GRPC_SKIP_VERIFY` (default true) controls certificate verification and applies only when secure is true.

Restrict who may add agents with `WOODPECKER_DISABLE_USER_AGENT_REGISTRATION=true`, which blocks users registering their own agents for repositories they administer.

## Checked

2026-11-03. Read the Woodpecker server configuration page and confirmed GRPC_ADDR, AGENT_SECRET, GRPC_SECRET behaviour, KEEPALIVE_MIN_TIME, GRPC_SECURE, GRPC_SKIP_VERIFY and DISABLE_USER_AGENT_REGISTRATION. Nothing removed. 

Method: documentation only; no commands were run.
