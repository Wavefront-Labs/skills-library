---
id: computing-software.messaging-and-integration.dapr.self-hosted-init-slim-without-docker
name: self-hosted-init-slim-without-docker
category: computing-software
field: messaging-and-integration
product: dapr
tags: [self-hosted, dapr-init, slim, placement, actors, no-docker, redis, actorstatestore]
level: practitioner
status: docs-checked
description: "Run Dapr self-hosted without Docker via dapr init --slim: daprd and placement binaries, what is missing (Redis, Zipkin), enabling actors with actorStateStore."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/self-hosted/self-hosted-no-docker.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/self-hosted/self-hosted-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default self-hosted init uses Docker and provisions a Redis container (default state store and pub/sub), a Zipkin container for tracing, and a default configuration and components folder in the user Dapr directory. Podman can replace Docker.

Slim init skips all of that:

```bash
dapr init --slim
```

It installs two binaries, `daprd` and `placement`. No default components are created, so apart from service invocation no building block works until you add components yourself (for example run Redis locally and write a component for it).

Actors need two things: the placement service running, and a transactional state store that supports ETags. The `placement` binary is installed in the `bin` folder of the user Dapr directory. Run it directly; on Windows pass a port:

```bash
%USERPROFILE%/.dapr/bin/placement.exe -port 6050
```

Its startup log shows the Raft server on 127.0.0.1:8201, the placement service on port 50005 (6050 in the Windows example), a healthz server on :8080 and a metrics server on :9090.

Mark the state store component as the actor store with metadata:

```yaml
  - name: actorStateStore
    value: "true"
```

Default name resolution in self-hosted mode is mDNS; where mDNS is unavailable (for example some VMs) use the HashiCorp Consul name resolution component for service invocation.

Remove the binaries with the self-hosted uninstall steps.

## Checked

Method: docs-checked 2026-11-09 against dapr/docs v1.15 self-hosted-no-docker.md (read in full) and self-hosted-overview.md (read in full)
