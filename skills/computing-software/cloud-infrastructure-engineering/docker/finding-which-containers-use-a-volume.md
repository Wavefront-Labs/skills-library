---
id: computing-software.cloud-infrastructure-engineering.docker.finding-which-containers-use-a-volume
name: finding-which-containers-use-a-volume
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-in-use, volume-prune, ps-filter, volume-inspect, cleanup, data-safety]
level: practitioner
status: docs-checked
description: "Before deleting or pruning volumes, map volumes to containers (running and stopped), find dangling and anonymous ones, check Compose ownership labels, and measure their sizes."
sources: ["https://docs.docker.com/reference/cli/docker/container/ls/#volume", "https://docs.docker.com/reference/cli/docker/volume/prune/", "https://docs.docker.com/reference/cli/docker/system/df/", "https://docs.docker.com/reference/cli/docker/volume/ls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding which containers use a volume

## Volume -> containers
```bash
docker ps -a --filter volume=pgdata --format '{{.Names}}\t{{.Status}}'
```
The `volume` filter matches containers that mounted a given volume or bind mount; add `-a` to
include stopped ones. Dangling volumes are those not referenced by any container, so a volume
used only by a stopped container is not dangling.

## All volumes with their users
```bash
for v in $(docker volume ls -q); do
  users=$(docker ps -a --filter volume="$v" --format '{{.Names}}' | paste -sd, -)
  printf '%-40s %s\n' "$v" "${users:--}"
done
```

## Container -> volumes
```bash
docker inspect -f '{{range .Mounts}}{{.Type}} {{.Name}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' web
```

## Dangling, anonymous and owned-by-Compose
```bash
docker volume ls -f dangling=true                                 # not referenced by any container
docker volume inspect -f '{{.Labels}} {{.CreatedAt}}' <vol>
```
`docker volume prune` removes only unused **anonymous** volumes by default; `--all` (`-a`) also
removes unused named volumes.

## Size before deleting
```bash
docker system df -v        # includes a per-volume usage listing
sudo du -sh "$(docker volume inspect -f '{{.Mountpoint}}' pgdata)"
```

## Safe deletion routine
1. Identify users (above); if a stopped container holds it, confirm the service is retired.
2. Back up: `docker run --rm -v pgdata:/v -v $PWD:/b alpine tar czf /b/pgdata.tgz -C /v .`
3. Remove the container, then `docker volume rm pgdata`.

## Gotchas
- `docker compose down -v` removes the named volumes declared in the Compose file and anonymous
  volumes attached to containers; double-check before using it on servers.
- `docker volume prune --all` also removes unused named volumes; check the list first.

## Checked

Date: 2026-10-24. Documentation release: Docker CLI references for `ps`, `volume ls`, `volume prune`, `system df` and Compose `down` (docker/cli, docker/compose main).
Confirmed: the `docker ps --filter volume=` filter, dangling filter semantics, `volume prune` default (anonymous only) and
`--all`, `system df -v` output, and `compose down -v` behaviour. Removed: the exact `volume is in use` message, the
anonymous label and 64-hex name claim, Compose project label names, `--volumes-from` and Swarm statements, which
no documentation page checked states.

Method: documentation only; no commands were run.
