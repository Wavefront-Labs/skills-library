---
id: computing-software.messaging-and-integration.dapr.self-hosted-docker-run-modes
name: self-hosted-docker-run-modes
category: computing-software
field: messaging-and-integration
product: dapr
tags: [self-hosted, docker, docker-compose, host-network, daprd, docker-network, dapr-run]
level: practitioner
status: docs-checked
description: "Choose how to run Dapr with Docker: dapr run for app plus sidecar, daprd container with host networking on Linux, a shared Docker network, or Docker Compose with sidecar services."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/self-hosted/self-hosted-with-docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: Dapr CLI and Docker (Docker Compose optional). Start with `dapr init` to create the control plane containers and default configuration.

Mode 1, app and sidecar as processes:

```bash
dapr run --app-id myapp --app-port 5000 -- dotnet run
```

Mode 2, app as a host process and sidecar as a container. The container must share the host network interface, and the host networking driver is only supported on Linux hosts:

```shell
docker run --net="host" --mount type=bind,source="$(pwd)"/components,target=/components daprio/daprd:edge ./daprd -app-id <my-app-id> -app-port <my-app-port>
```

Mode 3, app and Dapr in one container: not recommended, for local development only. The Dockerfile installs the Dapr CLI, copies a built `daprd`, runs `dapr init --slim`, installs the app and uses `ENTRYPOINT ["dapr"]` with `CMD ["run", "--app-id", "nodeapp", "--app-port", "3000", "node", "app.js"]`. Components such as Redis must still be reachable.

Mode 4, separate containers on a shared network, needed for service invocation between Dapr containers:

```bash
docker network create my-dapr-network
docker run --net=my-dapr-network ...
```

Mode 5, Docker Compose: define the sidecar pattern per app, a service using image `daprio/daprd:edge` with `command: ["./daprd", "--app-id", "nodeapp", "--app-port", "3000", ...]`. In the page example the app service `depends_on` redis and placement, exposes port 50001 because Dapr instances communicate over gRPC, and all join a common network (`hello-dapr`).

Compose syntax itself is outside the Dapr docs; refer to the Docker documentation.

## Checked

2026-11-08. Prerequisites, the dapr run and docker run commands, the Linux-only host network note, the dev-only single container Dockerfile, the shared network commands and the Docker Compose sidecar example confirmed on the Run Dapr in self-hosted mode with Docker page. All claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
