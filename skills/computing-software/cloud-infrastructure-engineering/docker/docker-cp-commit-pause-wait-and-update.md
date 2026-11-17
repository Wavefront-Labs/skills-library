---
id: computing-software.cloud-infrastructure-engineering.docker.docker-cp-commit-pause-wait-and-update
name: docker-cp-commit-pause-wait-and-update
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-cp, docker-commit, docker-pause, docker-wait, docker-update, container-lifecycle, resource-limits]
level: practitioner
description: "Operate on existing containers: copy files with docker cp, snapshot with commit (and why not to), freeze with pause, block on exit with wait, and change limits live with update."
sources: ["https://docs.docker.com/reference/cli/docker/container/cp/", "https://docs.docker.com/reference/cli/docker/container/commit/", "https://docs.docker.com/reference/cli/docker/container/pause/", "https://docs.docker.com/reference/cli/docker/container/wait/", "https://docs.docker.com/reference/cli/docker/container/update/", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# docker cp, commit, pause, wait and update

## cp
```sh
docker cp app:/var/log/app/error.log ./            # out
docker cp ./hotfix.conf app:/etc/app/app.conf      # in (works on stopped containers too)
docker cp app:/srv/data - | tar -tv                # stream as tar
docker cp -a ./dir app:/opt/                       # -a keeps uid/gid
```
- Paths: trailing `/.` copies directory **contents**; without it the directory itself.
- Certain system files cannot be copied: resources under `/proc`, `/sys`, `/dev`, tmpfs mounts and mounts created by the user in the container; copy those with `tar` inside `docker exec` instead.

## commit
```sh
docker commit -m "debug snapshot" -c 'CMD ["sleep","infinity"]' app forensics/app:incident-42
```
Uses: preserve a broken container's filesystem for forensics, or capture state before
deleting. **Not** a build method: no Dockerfile, not reproducible, includes junk and
secrets from the writable layer. Data in mounted volumes is not included. The container is paused during commit by default (`--no-pause` disables that).

## pause / unpause
```sh
docker pause app && docker unpause app
```
On Linux `docker pause` uses the freezer cgroup, so processes are suspended without being sent a signal and cannot tell. On Windows only Hyper-V containers can be paused. Useful for a consistent `cp` or snapshot.

## wait
```sh
docker run -d --name job app:1 migrate
code=$(docker wait job); docker logs job; docker rm job; exit "$code"
```
Blocks until the container stops and prints its exit code. `docker wait` returns 0 for a container that had already exited before the command ran, so when the job may finish first read `docker inspect -f '{{.State.ExitCode}}'` instead. The Engine API's
`/containers/{id}/wait` takes `condition=not-running|next-exit|removed`.

## update (live resource changes)
```sh
docker update --memory 2g --memory-swap 2g app
docker update --cpus 1.5 --cpu-shares 512 app
docker update --pids-limit 512 app
docker update --restart unless-stopped app
```
`docker update` changes resource limits and the restart policy of running containers dynamically; a new restart policy takes effect instantly. It is not supported for Windows containers.

## Verify
`docker inspect -f '{{.HostConfig.Memory}} {{.HostConfig.NanoCpus}} {{.HostConfig.RestartPolicy.Name}}' app`
reflects updates; `docker stats --no-stream app` shows current usage.

## Checked
2026-10-25, against docker/docs engine pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master) and the Engine API swagger. Confirmed: `docker cp` works on running or stopped containers, streams tar with `-`, `-a` copies uid/gid, cannot copy `/proc`, `/sys`, `/dev`, tmpfs and user-created mounts; `commit` options `-c` (CMD, ENTRYPOINT, ENV, EXPOSE, LABEL, ONBUILD, USER, VOLUME, WORKDIR), `-m`, `--no-pause`, volume data excluded, container paused by default; pause uses the freezer cgroup on Linux and only Hyper-V containers on Windows; `docker wait` prints exit codes and returns 0 for an already-exited container; the wait API conditions `not-running`, `next-exit`, `removed`; `docker update` options `--memory`, `--memory-swap`, `--cpus`, `--cpu-shares`, `--pids-limit`, `--restart`, unsupported on Windows. Removed: volumes-work claim (docs say the opposite), read-only-rootfs and distroless claims, network-timeout and health-check-while-paused claims, memory-lowering and non-updatable-fields claims. Note: the commit page text says `--pause` while its options table lists `--no-pause`.
Method: documentation only; no commands were run.
