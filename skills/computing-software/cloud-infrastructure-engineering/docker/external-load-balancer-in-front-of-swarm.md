---
id: computing-software.cloud-infrastructure-engineering.docker.external-load-balancer-in-front-of-swarm
name: external-load-balancer-in-front-of-swarm
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, swarm-load-balancer, traefik-swarm, routing-mesh, haproxy, publish-mode-host, client-ip, keepalived, ingress]
level: advanced
status: docs-checked
description: "Put HAProxy, a cloud LB or Traefik in front of Docker Swarm: mesh vs host-mode publishing, node health checks, preserving client IPs, Traefik swarm provider labels, keepalived VIPs."
sources: ["https://docs.docker.com/engine/swarm/ingress/", "https://doc.traefik.io/traefik/providers/swarm/", "https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/providers/swarm.md", "https://github.com/haproxy/haproxy/blob/master/doc/configuration.txt", "https://docs.docker.com/reference/cli/docker/service/ps/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External load balancer in front of Swarm

## Two architectures
**A. LB → routing mesh on every node.** Publish normally (`-p 443:8443`, mode ingress); the
port is open on all nodes and the mesh forwards to any task. Point the LB at all (or a
stable subset of) nodes.
- Simple, survives task moves.
- If the LB terminates HTTP, pass client details in headers such as `X-Forwarded-For` and configure the app to trust them.
- Extra hop: LB → node → (maybe another node) → task.

**B. LB → edge proxy in host mode.** Run a proxy (Traefik/HAProxy/nginx) as a `global`
service on labelled edge nodes with `mode=host` ports; it routes to services over overlay
networks by DNS name.
```bash
docker service create --name edge --mode global \
  --constraint node.labels.edge==true \
  --publish published=443,target=443,mode=host \
  --publish published=80,target=80,mode=host \
  --network public ... traefik:<tag>
```
- Only edge nodes need to be in the LB pool.

## HAProxy in front (pattern A)
```
frontend https_in
    bind :443
    mode tcp
    default_backend swarm_nodes
backend swarm_nodes
    mode tcp
    balance roundrobin
    option httpchk GET /healthz
    http-check expect status 200
    server n1 10.0.0.11:443 check check-ssl verify none
    server n2 10.0.0.12:443 check check-ssl verify none
    server n3 10.0.0.13:443 check check-ssl verify none
```
Health-check a real endpoint through the published port, not just TCP: the mesh accepts
connections on a node even if no task runs on it.

## Traefik as the Swarm edge (pattern B)
Traefik v3 has a dedicated Swarm provider; labels go under **`deploy.labels`** (service
labels), not container labels (Traefik reads service labels in Swarm mode):
```yaml
services:
  traefik:
    image: traefik:<tag>
    command:
      - --providers.swarm.endpoint=unix:///var/run/docker.sock
      - --providers.swarm.exposedbydefault=false
      - --providers.swarm.network=public
      - --entrypoints.websecure.address=:443
    ports:
      - { target: 443, published: 443, mode: host }
    volumes: [/var/run/docker.sock:/var/run/docker.sock:ro]
    deploy:
      mode: global
      placement: { constraints: [node.role == manager] }   # socket access to swarm API
  api:
    networks: [public]
    deploy:
      replicas: 3
      labels:
        - traefik.enable=true
        - traefik.http.routers.api.rule=Host(`api.example.com`)
        - traefik.http.services.api.loadbalancer.server.port=8080   # mandatory in swarm
```

## On-prem without a cloud LB
A VRRP daemon such as keepalived can float a VIP between edge nodes, with DNS pointing at the VIP
(configure it from the keepalived documentation; not covered here).

## Operations
- `docker node update --availability drain n2` moves tasks away; also take n2 out of the LB pool
  before maintenance.
- LB health check interval × fall count = how long a dead node receives traffic.

## Verify
```bash
for i in $(seq 10); do curl -s https://api.example.com/whoami | grep -i hostname; done   # spread across tasks
docker service ps edge --format '{{.Node}} {{.CurrentState}}'
```

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master), the Traefik repository docs (head 2026-10-23, Swarm provider pages) and HAProxy doc/configuration.txt (master). Confirmed: external LB may balance to every node on the published port even where no task runs; host-mode publishing bypasses the mesh and only nodes with a task listen; `--endpoint-mode dnsrr` cannot be combined with ingress publishing; Traefik Swarm provider options `providers.swarm.endpoint`, `exposedByDefault`, `network`, labels on services (`deploy.labels`), `loadbalancer.server.port` mandatory for Swarm, Traefik should run on managers for the Swarm API; HAProxy `option httpchk`, `http-check expect status`, `check-ssl`, `verify none` exist. Removed: mesh SNAT / client-IP claims, pinned Traefik tag, Traefik v2 flag, dnsrr/VIP behaviour for Traefik, keepalived container details, drained-node traffic claim. keepalived itself was not checked.
Method: documentation only; no commands were run.
