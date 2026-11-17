---
id: computing-software.devops-ci-cd.forgejo.docker-access-from-workflows
name: docker-access-from-workflows
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [docker-in-docker, dind, docker-host-automount, docker-build]
level: advanced
status: docs-checked
description: "Give workflows Docker access via a Docker-in-Docker container or by automounting the host socket, with the trade-offs."
sources:
  - https://forgejo.org/docs/latest/admin/actions/docker-access/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Building images in workflows needs extra runner configuration. The docs describe options.

Docker-in-Docker: run a `docker:dind` container (for example `docker run -p 127.0.0.1:2376:2375 --detach --privileged --restart always --name dind_container docker:dind dockerd -H tcp://0.0.0.0:2375 --tls=false`; the page notes no encryption or access control, reachable from the host only). In the runner config set `runner.envs.DOCKER_HOST: tcp://dind_container.docker.internal:2375`, `container.docker_host: 'tcp://127.0.0.1:2376'`, and `container.options: '--add-host=dind_container.docker.internal:host-gateway'`.

Admin notes: it protects the host's Docker resources, but concurrent jobs, or runners sharing one DIND, can see each other's containers. The DIND container has its own `/var/lib/docker`, so images are duplicated, lost if the container is recreated unless volume-mapped, and a persistent volume needs periodic `docker system prune`. Left-over artifacts can be inspected by later runs, and runner resource constraints do not apply to containers workflows create.

Alternative: `container.docker_host: automount` mounts the host's socket at `/var/run/docker.sock` in job containers, exposing the host daemon. If `DOCKER_HOST` is a tcp:// address, which is the case with the OCI image installation, the socket cannot be shared and `automount` acts like the default `-`.

Without such configuration the job container cannot reach a daemon: the default UNIX socket /var/run/docker.sock does not exist inside it, and docker build fails with a message that it cannot connect to the Docker daemon.

## Checked

2026-11-04. Confirmed against the Forgejo Utilizing Docker within Actions page: the failure and its cause, the DIND command and runner settings, the administrator notes for DIND, and the automount behaviour. Added the tcp DOCKER_HOST limitation from the page. LXC and VM sections were not summarised.

Method: documentation only; no commands were run.
