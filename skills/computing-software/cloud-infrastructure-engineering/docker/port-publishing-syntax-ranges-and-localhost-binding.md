---
id: computing-software.cloud-infrastructure-engineering.docker.port-publishing-syntax-ranges-and-localhost-binding
name: port-publishing-syntax-ranges-and-localhost-binding
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, port-publishing, port-mapping, publish, expose, publish-udp, bind-address, port-range, localhost-binding, ip-flag, publish-all, docker-port, ephemeral-ports, expose-vs-publish]
level: practitioner
description: "Publish ports precisely: -p ip:host:container/proto, ranges, -P with EXPOSE and docker port, binding to 127.0.0.1 by default with the daemon ip option."
sources: ["https://docs.docker.com/engine/network/port-publishing/", "https://docs.docker.com/reference/cli/docker/container/run/#publish", "https://docs.docker.com/reference/dockerfile/#expose", "https://docs.docker.com/reference/compose-file/services/#ports"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Port publishing: syntax, ranges and localhost binding

## Syntax
```sh
-p 8080:80                 # all host IPv4+IPv6 addresses :8080 -> container 80/tcp
-p 127.0.0.1:8080:80       # loopback only
-p 10.0.0.5:8080:80        # one host interface
-p 8080:80/udp             # UDP; add both lines for tcp+udp
-p 53:53/tcp -p 53:53/udp
-p 80                      # random host port, all interfaces
-p 8000-8010:8000-8010     # range (equal sizes)
-p 8000-9000:80            # host port range -> container 80 (Compose reference example)
--publish published=8080,target=80,protocol=tcp,mode=host   # long form (Swarm services)
```
Compose long syntax:
```yaml
ports:
  - target: 80
    published: "8080"
    host_ip: 127.0.0.1
    protocol: tcp
    app_protocol: http
```

## Default to loopback
`-p 5432:5432` on a server exposes the database to the world - and Docker's published-port rules
bypass ufw. Make loopback the default for the **default bridge** in daemon.json:
```json
{ "ip": "127.0.0.1" }
```
Then `-p 8080:80` on the default bridge binds 127.0.0.1 unless an IP is given explicitly. For one user-defined network:
`docker network create -o com.docker.network.bridge.host_binding_ipv4=127.0.0.1 internal-net`; for all user-defined bridges use daemon `default-network-opts` with the same option under `bridge`. The default bind address does not affect Swarm services (always `0.0.0.0`). In releases older than 28.0.0, hosts on the same L2 segment can reach ports published to localhost.

## EXPOSE, -P and docker port
- `EXPOSE 8080` is **documentation + metadata**; it publishes nothing and doesn't restrict
  anything. Containers on the same network reach every listening port regardless.
- `-P` / `--publish-all` publishes every exposed port (`EXPOSE` or `--expose`) to random host ports from the
  ephemeral range (`/proc/sys/net/ipv4/ip_local_port_range`).
```sh
docker run -d -P --name web nginx
docker port web               # 80/tcp -> 0.0.0.0:<random port>
docker port web 80/tcp
```
Useful for tests running many copies in parallel.

## Gotchas
- For very large port ranges the host driver page recommends host networking, which needs no NAT and no userland-proxy per port.
- With `userland-proxy` on (default), published ports are served by `docker-proxy` for loopback traffic.
- IPv6: `-p 8080:80` also binds `[::]:8080` when IPv6 is available; `-p [::1]:8080:80` for v6 loopback.

## Verify
```sh
ss -ltnp | grep 8080            # shows 127.0.0.1:8080 when localhost-bound
docker port web
nc -zv <public-ip> 8080         # from another host: should fail for loopback-bound ports
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the port publishing page (flag table, loopback binding with `127.0.0.1`/`::1`, the 28.0.0 localhost warning, `ip` key for the default bridge, `host_binding_ipv4`, `default-network-opts`, Swarm exception), the `docker run` reference (`-P`, ephemeral range) and the Compose ports reference (long syntax fields `target`, `published`, `host_ip`, `protocol`, `app_protocol`; range examples). Corrected the daemon `ip` key scope (default bridge only) and removed `127.0.0.1::80` plus the typical-range figure.

Method: documentation only; no commands were run.
