---
id: computing-software.systems-network-administration.dns-dhcp.bind-in-containers
name: bind-in-containers
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, bind-docker, containers, kubernetes, isc-docker-image]
level: practitioner
status: docs-checked
description: "Run BIND in Docker or Kubernetes: the ISC image, volumes for config/cache/keys, host networking vs port publishing, signals, logging and health checks."
sources:
  - https://github.com/isc-projects/bind9-docker
  - https://hub.docker.com/r/internetsystemsconsortium/bind9
  - https://kubernetes.io/docs/tutorials/services/source-ip/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIND in containers

## ISC image
```
docker run -d --name bind9 --restart unless-stopped \
  -p 53:53/udp -p 53:53/tcp -p 127.0.0.1:953:953/tcp \
  -v /srv/bind/config:/etc/bind \
  -v /srv/bind/cache:/var/cache/bind \
  -v /srv/bind/records:/var/lib/bind \
  -v /srv/bind/log:/var/log \
  internetsystemsconsortium/bind9:9.20   # tags follow the ISC image branches v9.18, v9.20, v9.21
```
- `/etc/bind`: named.conf and static zones (read-only is fine).
- `/var/lib/bind`: writable, persistent location for secondary, dynamic and signed zone files and journals (the image creates it owned by `bind`).
- `/var/cache/bind`: the `bind` user's home and the working directory for cache and state files.
- Mounting a volume over `/etc/bind` hides the image's default `named.conf`, so supply your own.
- Keep DNSSEC key material (`key-directory`) on a persistent, backed-up volume; losing it on a redeploy breaks signed zones.

## Networking
- Source-address-based ACLs only work if the client address is preserved. With published ports, check query logs for real client IPs; `--network host` avoids Docker NAT.
- On Kubernetes, `externalTrafficPolicy: Local` on a NodePort or LoadBalancer Service preserves the client source IP (see the Kubernetes source-IP tutorial). Expose both UDP and TCP 53.

## Config and reload
- `docker exec bind9 rndc reload` after config changes; or `named-checkconf` in CI before deploy.
- The image starts `named -u bind` (build argument `UID`/`GID` default 53); mounted directories must be writable by that UID.

## Logs
The image's default command is `-f -c /etc/bind/named.conf -L /var/log/bind/default.log`: foreground, logging to a file under `/var/log/bind` (the declared `/var/log` volume). Override `CMD` with `-g` to log to stderr instead. For a health check, query a name your server is authoritative for.

## Gotchas
- Container restarts lose cache unless cache dumps are persisted: resolvers cold-start; stagger restarts.

## Verify
- [ ] `dig @<host> example.com` returns answers with real client IPs in query logs, and zones persist across `docker rm`/recreate.

## Checked

Date: 2026-10-26. Documentation: isc-projects/bind9-docker branch v9.20 (Dockerfile, built from BIND 9.20.30 on Alpine) and the Kubernetes website tutorial source-ip.md, read 2026-10-26. Confirmed: VOLUME list (/etc/bind, /var/cache/bind, /var/lib/bind, /var/log), exposed ports 53/853/443/953, bind user UID/GID 53, entrypoint named -u bind, default CMD, externalTrafficPolicy Local preserving source IP. Removed the unconfirmed health-check name, hostNetwork and host-time claims.

Method: documentation only; no commands were run.
