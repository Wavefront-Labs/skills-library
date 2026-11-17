---
id: computing-software.cloud-infrastructure-engineering.docker.container-dns-flags-and-resolution-failures
name: container-dns-flags-and-resolution-failures
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dns, dns-config, container-dns, dns-flag, dns-opt, systemd-resolved, resolv-conf-127-0-0-53, dns-forwarding, dns-resolution-failure]
level: practitioner
description: "Fix container DNS: --dns/--dns-search/--dns-opt and daemon dns, how Docker handles a 127.0.0.53 systemd-resolved stub, and debugging external lookup failures."
sources: ["https://docs.docker.com/engine/network/#dns-services", "https://docs.docker.com/reference/cli/docker/container/run/#dns", "https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file", "https://docs.docker.com/engine/daemon/troubleshoot/#dns-resolver-issues", "https://github.com/moby/moby/tree/master/daemon/libnetwork/internal/resolvconf"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Container DNS flags and resolution failures

## How containers get DNS
- **Default bridge**: container `/etc/resolv.conf` is a copy of the host's with loopback nameservers removed.
- **User-defined networks / Compose**: `nameserver 127.0.0.11` (embedded DNS). It answers
  container names and forwards everything else to the upstreams taken from the host
  resolv.conf (or `--dns`).

## Flags
```sh
docker run --dns 10.0.0.2 --dns 1.1.1.1 --dns-search corp.example.com \
  --dns-option ndots:1 --dns-option timeout:2 --dns-option attempts:2 app:1
```
Daemon-wide: `{"dns": ["10.0.0.2"], "dns-search": ["corp.example.com"], "dns-opts": ["ndots:1"]}`.
Compose: `dns:`, `dns_search:`, `dns_opt:`.
`ndots:1` limits search-domain expansion when apps resolve external names.

## systemd-resolved hosts (127.0.0.53)
Host `/etc/resolv.conf` -> `nameserver 127.0.0.53` (stub). A container's own loopback is not the host's, so for **default-bridge** containers Docker:
- uses `/run/systemd/resolve/resolv.conf` (the real upstreams) when `127.0.0.53` is the only nameserver, and
- drops loopback nameservers and, if none remain, uses the defaults `8.8.8.8`/`8.8.4.4` (plus Google's IPv6 pair when IPv6 is enabled) - which breaks
  internal/split DNS where public DNS is blocked.
On **user-defined networks** the embedded resolver forwards from the host's network namespace, so host loopback resolvers remain usable.
Fix: set `dns` in daemon.json to your real resolvers.

## Debugging failures
```sh
docker run --rm --network mynet nicolaka/netshoot dig +short example.com
docker run --rm --network mynet nicolaka/netshoot dig @127.0.0.11 example.com
docker exec app cat /etc/resolv.conf
docker run --rm --network host nicolaka/netshoot dig example.com      # does the host resolve?
```
| Symptom | Likely cause |
|---|---|
| container names resolve, internet names don't | upstream unreachable (firewall, 127.0.0.53, VPN DNS) |
| works on host, fails in container | default-bridge container fell back to `8.8.8.8` (no usable host upstream) |
| nothing resolves on default bridge | host resolv.conf only had loopback entries |

## Gotchas
- Configure DNS with flags or daemon settings rather than by editing `/etc/resolv.conf` inside a container.
- `--dns` on a user-defined network sets the **upstream** of 127.0.0.11, not the container's nameserver line.
- `--network host` uses the host resolver directly.

## Verify
`dig` through 127.0.0.11 and directly to the configured upstream both answer.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the networking overview (embedded DNS 127.0.0.11, `--dns`/`--dns-search`/`--dns-opt`, resolution order), the `docker run` reference (`--dns-option`), the `dockerd` reference (`dns`, `dns-opts`, `dns-search`), the Compose reference (`dns`, `dns_search`, `dns_opt`) and the moby resolvconf source (127.0.0.53 detection, loopback removal, default servers, host-namespace forwarding for the embedded resolver). Removed the intermittent-delay and Alpine rows and the log-line claim, which no documentation covers.

Method: documentation only; no commands were run.
