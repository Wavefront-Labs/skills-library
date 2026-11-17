---
id: computing-software.cloud-infrastructure-engineering.docker.userland-proxy-and-hairpin-nat
name: userland-proxy-and-hairpin-nat
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, userland-proxy, hairpin-nat, docker-proxy, port-publishing, route-localnet, dnat, source-ip, daemon-json]
level: advanced
status: docs-checked
description: "Understand docker-proxy vs pure iptables port publishing: which traffic each path handles, hairpin NAT, source-IP effects, and when to set userland-proxy false."
sources: ["https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/engine/network/port-publishing/", "https://docs.docker.com/engine/network/drivers/host/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# userland-proxy and hairpin NAT

## What the userland proxy is
For `-p 8080:80` Docker sets up NAT/port-mapping firewall rules and, by default, uses a
`docker-proxy` process. The `dockerd` reference describes the option as "use userland proxy for
loopback traffic" (default true); the binary path is set by `userland-proxy-path`.
- With the proxy enabled and an IPv4-only bridge network, IPv6 host addresses map to the container's IPv4 address.
- **Hairpin**: a container connecting to `<host-ip>:8080` that maps back to itself or a
  neighbour on the same bridge.

```bash
ps -ef | grep docker-proxy        # proxy processes for published ports
```

## `"userland-proxy": false`
```json
{ "userland-proxy": false }
```
Set it in `/etc/docker/daemon.json` and restart the daemon.

Reasons to disable the proxy:
- **Big port ranges**: a proxy per published port costs memory and startup time (the host driver page notes host mode avoids a userland-proxy per port).
- Uniform behaviour: all paths go through firewall rules you can trace.

Reason to keep it (the default):
- IPv6-to-IPv4 mapping: IPv6 host addresses reach containers on an IPv4-only bridge only while `userland-proxy` is true. Without it, publish only to IPv4 or enable IPv6 on the network.

## Debugging hairpin failures
Symptom: container A calls `http://<host-public-ip>:8080` (served by container B on the same
host) and times out, while external clients work.
```bash
sudo iptables -t nat -S | grep -E 'MASQUERADE|DNAT'
```
When possible, call the service by container name on a shared network instead of via the host's published address.

## Verify
```bash
docker run -d --name web -p 8080:80 nginx
curl -s localhost:8080 >/dev/null && docker logs web | tail -1
docker run --rm --add-host=host.docker.internal:host-gateway curlimages/curl -s -o /dev/null -w '%{http_code}' http://host.docker.internal:8080   # access via the host address
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the `dockerd` reference (`--userland-proxy` described as for loopback traffic, default true, `userland-proxy-path`), the port publishing page (IPv6-to-IPv4 mapping needs `--userland-proxy=true`) and the host driver page (no per-port userland-proxy in host mode). Removed unconfirmed mechanism claims: `route_localnet` handling, bridge hairpin mode, which path the container sees as source IP, CIS scanner behaviour, cloud load-balancer hairpin limits, and the `awk` pipeline.

Method: documentation only; no commands were run.
