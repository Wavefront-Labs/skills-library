---
id: computing-software.cloud-infrastructure-engineering.docker.docker-swarm-orchestration
name: docker-swarm-orchestration
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, docker-swarm, stack-deploy, docker-stack, raft, manager-quorum, worker-node, overlay-network, ingress-mesh, routing-mesh, docker-secret, docker-config, rolling-update, service-constraint, placement-preference, swarmkit]
level: advanced
status: docs-checked
description: "Operating Docker Swarm where it's still a reasonable fit: raft manager quorum math, stack deploy, secrets/configs, the ingress mesh, and when Swarm is the wrong tool."
sources: ["https://docs.docker.com/engine/swarm/", "https://docs.docker.com/engine/swarm/admin_guide/", "https://docs.docker.com/engine/swarm/secrets/", "https://docs.docker.com/engine/swarm/networking/", "https://docs.docker.com/reference/cli/docker/service/create/", "https://docs.docker.com/reference/cli/docker/service/logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Swarm orchestration (still relevant, narrower than it was)

**Goal:** know when Swarm is the actually-correct, lower-overhead choice versus Kubernetes,
and operate the parts that bite (raft quorum, secrets, rolling updates) without having
re-learned it from a Kubernetes mental model. Swarm mode is built into Docker Engine; much newer ecosystem tooling targets Kubernetes first.

## When Swarm is the right call
Small-to-mid fleet (single-digit to low tens of nodes), a team that already knows `docker`
CLI and doesn't want to run/patch a control plane, and workloads that don't need
Kubernetes-specific ecosystem pieces (CRDs, operators, service mesh sidecars, HPA on custom
metrics). `docker swarm init` to a working multi-service deployment with secrets, overlay
networking and rolling updates is minutes, not a day of kubeadm/manifests. Wrong call once
you need autoscaling on anything beyond replica count, a wide tool ecosystem (Helm charts,
most SaaS integrations target k8s first), or you're already running Kubernetes elsewhere
and would rather not maintain two orchestrator skillsets.

## Raft quorum — the thing that actually causes incidents
Manager nodes run a raft consensus group; quorum needs `floor(n/2)+1` managers reachable.
3 managers tolerate 1 loss, 5 tolerate 2 — **always use an odd number**, and never exactly
2 (no fault tolerance, and an even count doesn't help quorum math). Losing quorum (not just
losing a manager) freezes **all** orchestration — existing containers keep running via the
local engine, but you cannot deploy, scale, or even run most `docker service` commands
until quorum is restored. Recovery from total manager loss:
`docker swarm init --force-new-cluster --advertise-addr <ip>` on a surviving manager — it removes all
other managers from the swarm, so it's a last resort, not a routine operation.
```
docker node ls                      # check manager/worker roles and Reachability column
docker node promote <worker-id>     # grow manager count; do this before decommissioning one
```

## Stacks, services, and the ingress mesh
`docker stack deploy -c docker-compose.yml mystack` reads a Compose file's `deploy:` key
(replicas, resources, restart_policy, placement) — a different consumer of the same file
format `docker-compose-for-local-dev` covers; Swarm ignores `build:` in stack files (images
must already exist in a registry every node can pull). The **ingress routing mesh**: every
node in the swarm listens on a published service port and load-balances to a healthy task
wherever it runs, via an IPVS-based overlay network — so you can hit any node's IP on the
published port and reach the service, not just nodes currently running a replica. This is
different from Kubernetes' NodePort/Service model and is Swarm's single most useful
default (no separate load balancer object to create for basic cases).

## Secrets and configs
`docker secret create db_password -` (stdin, never a file arg left on disk) mounts at
`/run/secrets/<name>` inside Linux containers in an **in-memory filesystem**, stored encrypted in
the Raft log and absent from images committed from the container — meaningfully different from a Compose `.env`
file or a plain `environment:` value, which both land in `docker inspect` output. `docker
config create` is the equivalent for non-secret config files. Rotating a secret requires
removing it from every service using it and adding a new one with a new name (secrets are
immutable by id) — plan a naming convention (`db_password_v2`) rather than being surprised
mid-incident.

## Rolling updates and placement
```
docker service update --image app:1.3.0 --update-parallelism 2 --update-delay 10s \
  --update-failure-action rollback --update-monitor 30s myservice
```
`--update-failure-action rollback` plus `--update-monitor` is the built-in canary-ish
safety net. The default failure action is `pause`, which leaves the update half-done until someone
notices; `--update-monitor` defaults to 5s.
Placement constraints (`--constraint node.labels.ssd==true`) and preferences
(`--placement-pref spread=node.labels.zone`) are Swarm's (much simpler than Kubernetes')
scheduling knobs — fine for "spread across these three racks," not a fit for complex
bin-packing or taints/tolerations-style logic.

## Gotchas
- Overlay network encryption (`--opt encrypted` on `docker network create -d overlay`) is
  off by default — enable it for any multi-host traffic crossing untrusted networks.
- `docker service logs` only works with the `json-file` or `journald` log driver; other
  drivers (shipped straight to a log aggregator) make this command return nothing, which
  looks like a broken service when it's a logging-config mismatch.

## Verify
`docker node ls` shows all managers `Reachable` and exactly one `Leader`; `docker service
ps myservice` shows the expected replica count all `Running`, and a manual `docker service
update --force` completes without triggering the configured rollback.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: quorum needs a majority, an odd manager count is recommended and more than two managers; `--force-new-cluster` keeps one manager (removes the others); secrets mount at `/run/secrets/<name>` in an in-memory filesystem on Linux; `docker stack deploy` ignores `build`; ingress uses IPVS; overlay application traffic is unencrypted unless `--opt encrypted`; `docker service logs` works only with `json-file` or `journald`; update failure action default `pause` and `--update-monitor` default 5s. Removed: claims about maintenance-mode status and vendor support.
Method: documentation only; no commands were run.
