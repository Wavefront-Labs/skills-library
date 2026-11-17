---
id: computing-software.cloud-infrastructure-engineering.docker.extra-hosts-and-dns-settings-in-compose
name: extra-hosts-and-dns-settings-in-compose
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, container-dns, extra-hosts, compose-dns, add-host, host-gateway, dns-search]
level: practitioner
status: docs-checked
description: "Control name resolution per Compose service: extra_hosts (incl. host-gateway), dns, dns_search and dns_opt, list vs map syntax, IPv6 entries and the embedded DNS server."
sources: ["https://docs.docker.com/reference/compose-file/services/#extra_hosts", "https://docs.docker.com/reference/compose-file/services/#dns", "https://docs.docker.com/compose/how-tos/networking/", "https://docs.docker.com/engine/network/", "https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/reference/cli/docker/container/run/#add-host"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extra_hosts and DNS settings in Compose

## extra_hosts
```yaml
services:
  app:
    image: app:1.0
    extra_hosts:
      - "host.docker.internal:host-gateway"     # reach the Docker host
      - "legacy-db.corp=10.20.0.15"             # "=" is the preferred separator
      - "ipv6only.example=[2001:db8::10]"       # IPv6 may be wrapped in square brackets
```
Map form:
```yaml
    extra_hosts:
      legacy-db.corp: 10.20.0.15
      host.docker.internal: host-gateway
```
- The short syntax is `HOSTNAME=IP`; `=` is preferred and `:` is also accepted (accepting
  `:` was introduced in Compose 2.24.1).
- Compose adds matching entries to the container's network configuration, which on Linux
  means extra lines in `/etc/hosts`.
- `host-gateway` is a special value. On Linux it resolves to the host's IP on the default
  bridge network (the dockerd reference says the IPv4 address of the default bridge, and its
  IPv6 address if it has one); on Docker Desktop it resolves to the same internal address as
  `host.docker.internal`. It can be changed with the dockerd `--host-gateway-ip` option, or
  the `host-gateway-ips` key (an array) in `daemon.json` (the older `host-gateway-ip` string
  key is still accepted).
- Use `extra_hosts` for hosts missing from DNS, pinning a name during migrations, or
  testing against a specific backend.

## DNS options
```yaml
services:
  app:
    dns: [10.0.0.2, 10.0.0.3]
    dns_search: [corp.example.com]
    dns_opt: ["use-vc", "no-tld-query"]
```
`dns` sets custom DNS servers (a single value or a list), `dns_search` sets search domains,
and `dns_opt` passes options to the container's DNS resolver (`/etc/resolv.conf` on Linux).
Containers on a custom network (Compose creates one by default) use Docker's embedded DNS
server at `127.0.0.11`, which forwards external lookups to the DNS servers configured on
the host unless you override them with `--dns`/`dns`. Service names keep resolving on the
project network.

## CLI equivalents
`--add-host name:ip`, `--dns`, `--dns-search`, `--dns-option` (all in the `docker run`
reference).

## Verify
```bash
docker compose exec app cat /etc/hosts /etc/resolv.conf
docker compose config                  # shows the normalised extra_hosts
```

## Gotchas
- With `network_mode: host`, service-name DNS resolution does not work (the container uses
  the host's network stack), as the Compose networking guide states.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), docker/cli
`docs/reference` (dockerd and run), Compose v5.6.1. Method: documentation only; no commands
were run.
Confirmed in the Compose file reference: `extra_hosts` short and long syntax, separator
rules and the 2.24.1 note, `dns`, `dns_search`, `dns_opt` examples and descriptions; in the
Compose networking guide: `host-gateway` meaning on Linux, Mac and Windows and
`network_mode: host`; in the Docker networking page: the embedded DNS server address and
forwarding; in the dockerd reference: `host-gateway-ip` and `host-gateway-ips`; in the run
reference: `--add-host`, `--dns`, `--dns-option`, `--dns-search`. Removed: the
`getent`/`yq` verification, musl and ndots remarks, the `use-vc`/`ndots` option mix (kept
only options shown in the reference), and the VPN split-DNS warning.
