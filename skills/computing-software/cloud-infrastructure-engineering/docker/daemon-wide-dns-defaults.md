---
id: computing-software.cloud-infrastructure-engineering.docker.daemon-wide-dns-defaults
name: daemon-wide-dns-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dns-config, daemon-dns, daemon-json, resolv-conf, embedded-dns, dns-search]
level: practitioner
status: docs-checked
description: "Set default DNS servers, search domains and resolver options for all containers in daemon.json, how they interact with the embedded DNS on user networks, and how to verify."
sources: ["https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file", "https://docs.docker.com/engine/network/#dns-services", "https://docs.docker.com/reference/cli/docker/container/run/#dns", "https://docs.docker.com/engine/daemon/troubleshoot/#dns-resolver-issues"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daemon-wide DNS defaults

## daemon.json
```json
{
  "dns": ["10.0.0.2", "10.0.0.3"],
  "dns-search": ["corp.example.com"],
  "dns-opts": ["ndots:1", "timeout:2", "attempts:2"]
}
```
Restart dockerd; applies to containers created afterwards. Per-container flags
(`--dns`, `--dns-search`, `--dns-option`) or Compose `dns:` override these defaults.

## What containers see
- **Default bridge**: `/etc/resolv.conf` in the container lists your `dns` servers directly.
- **User-defined networks** (including Compose): resolv.conf shows `nameserver 127.0.0.11`
  (embedded DNS). Container names resolve there; everything else is forwarded to the `dns`
  servers from daemon.json, or to the host's resolvers if unset. Search domains and options
  are written into the container's resolv.conf.
- Without `dns` set, default-bridge containers get a copy of the host's `/etc/resolv.conf` with loopback entries removed;
  if the host's only nameserver is the systemd-resolved stub `127.0.0.53`, Docker reads `/run/systemd/resolve/resolv.conf` instead, and
  if nothing usable remains it uses Google DNS `8.8.8.8/8.8.4.4`. That fallback surprises locked-down networks:
  set `dns` explicitly there. On user-defined networks the embedded DNS forwards from the host's namespace.

## Typical reasons to set it
- Host uses systemd-resolved stub (127.0.0.53) with split DNS over VPN; containers need the
  real corporate resolvers.
- Egress to public DNS is blocked by firewall.
- Short names (`db`) must resolve in a corporate domain via `dns-search`.

## Verify
```bash
docker run --rm alpine cat /etc/resolv.conf
docker run --rm --network mynet alpine sh -c 'cat /etc/resolv.conf; nslookup intranet.corp.example.com'
cat /etc/docker/daemon.json
```

## Gotchas
- When several `--dns` servers are set on the default bridge, the container's resolver library decides how it queries them (some query in parallel and take the first answer, even `NXDOMAIN`); on a custom network the embedded DNS queries upstreams in order and stops after a success or `NXDOMAIN`.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed the daemon.json keys `dns`, `dns-search`, `dns-opts` in the `dockerd` reference, the per-container flags and the upstream-ordering note in the networking overview, and the loopback/fallback behaviour in the daemon troubleshooting page and the moby resolvconf source. Removed unconfirmed gotchas about Kubernetes ndots, host resolver changes and Docker Desktop DNS forwarding, and the `jq` command.

Method: documentation only; no commands were run.
