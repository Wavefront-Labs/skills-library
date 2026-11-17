---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-ingress-publish-modes-and-endpoint-modes
name: swarm-ingress-publish-modes-and-endpoint-modes
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, routing-mesh, swarm-ingress, ingress-network, ingress-subnet, publish-mode-host, mode-host, endpoint-mode, vip, dnsrr]
level: advanced
description: "Choose routing mesh (ingress) vs host-mode publishing, recreate the ingress network with a custom subnet or MTU, and pick VIP vs dnsrr endpoint mode for service discovery."
sources: ["https://docs.docker.com/engine/swarm/ingress/", "https://docs.docker.com/engine/swarm/networking/", "https://github.com/compose-spec/compose-spec/blob/main/deploy.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Swarm ingress, publish modes and endpoint modes

## Routing mesh vs host mode
```yaml
ports:
  - target: 80
    published: 8080
    mode: ingress          # default: every node listens on 8080 and IPVS-balances to any task
  - target: 9100
    published: 9100
    mode: host             # only nodes running a task listen; goes straight to the local task
```
| | ingress | host |
|---|---|---|
| Any node accepts traffic | yes | only where a task runs |
| Multiple tasks per node on same port | yes | no (port conflict) |
| Typical | stateless web behind an LB | global services such as a DNS cache or an edge proxy |
For an edge proxy: run it `mode: global` with host-mode ports (the Docker docs use a global `dns-cache` service for host mode).

## Customising the ingress network
Default ingress subnet `10.0.0.0/24` collides with many VPCs. Recreate it (no services may
publish ports meanwhile):
```sh
docker network rm ingress                        # confirm; publishing services must be removed first
docker network create --driver overlay --ingress \
  --subnet 10.250.0.0/24 --gateway 10.250.0.1 \
  --opt com.docker.network.driver.mtu=1450 my-ingress
```
Then redeploy services. Do it right after `swarm init` to avoid downtime.

## Endpoint modes
```yaml
deploy:
  endpoint_mode: vip      # default: service name -> one virtual IP, IPVS load-balances
  # endpoint_mode: dnsrr  # service name -> A records of all task IPs
```
- **vip**: the service name resolves to one virtual IP that load-balances across tasks.
- **dnsrr**: a DNS query for the service name returns task IPs and the client connects directly; use it with your own load balancer. dnsrr services
  **can't** use ingress-mode published ports - use host mode or a proxy.
- `tasks.<service>` DNS name always returns individual task IPs, even in vip mode -
  useful when clients need individual task addresses.

## Verify
```sh
docker network inspect ingress -f '{{json .IPAM.Config}}'
docker run --rm --network shop_default <image-with-dig> dig +short api tasks.api   # the network must be attachable
curl -s http://<any-node>:8080/      # ingress: works on nodes without tasks
```

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: default ingress network subnet shown as 10.0.0.0/24; recreating ingress means removing it (services publishing ports must be removed first) and `docker network create --driver overlay --ingress --subnet --gateway --opt com.docker.network.driver.mtu=...`; host mode bypasses the routing mesh and only nodes running a task listen; `--endpoint-mode dnsrr` cannot be used with `mode=ingress`; `tasks.<service>` DNS returns all task IPs; `endpoint_mode` values vip and dnsrr. Removed: client-IP preservation claims, VIP connection-stickiness and gRPC/database claims, pinned third-party image.
Method: documentation only; no commands were run.
