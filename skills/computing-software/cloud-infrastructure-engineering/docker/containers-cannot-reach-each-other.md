---
id: computing-software.cloud-infrastructure-engineering.docker.containers-cannot-reach-each-other
name: containers-cannot-reach-each-other
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, network-troubleshooting, inter-container-connectivity, bind-0-0-0-0, user-defined-network, embedded-dns, connection-refused]
level: practitioner
status: docs-checked
description: "Fix container-to-container failures: not on one network, no DNS on the default bridge, app bound to 127.0.0.1, published vs container ports, icc=false, startup order."
sources: ["https://docs.docker.com/engine/network/", "https://docs.docker.com/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge", "https://docs.docker.com/compose/how-tos/networking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Containers cannot reach each other

## Read the error first
| Error from the client container | Meaning |
|---|---|
| `Name does not resolve` / `unknown host` | DNS: not on a shared user-defined network, wrong name |
| `Connection refused` | Name resolved, nothing listening on that IP:port (wrong port, bound to 127.0.0.1, not started yet) |
| Timeout | Packets dropped: different networks, `icc=false`, firewall rule, wrong IP |

## Checklist
1. **Same user-defined network?**
```bash
docker inspect -f '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' api
docker inspect -f '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' db
```
The default `bridge` network has no name resolution between containers. Compose puts a
project's services on `<project>_default`; services from **different** projects need a shared
external network.

2. **Right name?** Containers resolve each other by container name or network alias (in Compose, the service name).
```bash
docker exec api getent hosts db
```

3. **Right port?** Inside the network use the **container** port, not the published host
port: `db:5432`, not `localhost:15432`. `localhost` inside a container is that container.

4. **Listening on all interfaces?**
```bash
docker exec db ss -ltn        # 127.0.0.1:5432 = only reachable from inside db
```
Configure the app to bind `0.0.0.0` (or `::`).

5. **Started and ready?** `depends_on` alone only orders start; add
`condition: service_healthy` with a healthcheck, or retry in the client.

6. **icc / segmentation**: networks created with `com.docker.network.bridge.enable_icc=false`
(or daemon `"icc": false`, which applies to the default bridge) disable inter-container connectivity by design. Check `docker network inspect`.

7. **Test from inside the network**:
```bash
docker run --rm --network container:api nicolaka/netshoot \
  sh -c 'nslookup db; nc -vz db 5432; curl -sv http://web:8080/health'
```

## Gotchas
- A `--network host` container has no IP of its own; other containers reach it through the host's address, and it reaches bridge containers through their published ports.
- Swarm services on overlay networks need the network to be attachable for standalone
  containers to join.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the bridge driver page (default bridge has no name resolution; user-defined bridges resolve by name or alias), the networking overview, the Compose reference (`depends_on` `service_healthy`), the host driver page and the `dockerd` reference (`icc` applies to the default bridge). Removed per-framework bind flags, the `jq` pipeline and the hostname-resolution claim.

Method: documentation only; no commands were run.
