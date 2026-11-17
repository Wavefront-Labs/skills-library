---
id: computing-software.systems-network-administration.pi-hole.docker-compose-quickstart
name: docker-compose-quickstart
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [docker-compose-quickstart, pihole-container, pihole-image-tags]
level: intro
status: docs-checked
description: "Run Pi-hole in Docker from the quick-start compose file, with the right ports, volumes, capabilities and image tag."
sources: ["https://docs.pi-hole.net/docker/", "https://docs.pi-hole.net/docker/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pi-hole in Docker: quick start

Save a `docker-compose.yml` like this and adjust it:

```yaml
services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80/tcp"
      - "443:443/tcp"
      #- "67:67/udp"    # only if Pi-hole is the DHCP server
      #- "123:123/udp"  # only if Pi-hole is the NTP server
    environment:
      TZ: 'Europe/London'
      FTLCONF_webserver_api_password: 'a-strong-password'
      FTLCONF_dns_listeningMode: 'ALL'
    volumes:
      - './etc-pihole:/etc/pihole'
    cap_add:
      - NET_ADMIN   # DHCP only
      - SYS_TIME    # NTP client setting the host clock
      - SYS_NICE    # optional extra CPU priority
    restart: unless-stopped
```

Start it with `docker compose up -d` (older systems use `docker-compose`).

**Why these settings**

- `FTLCONF_dns_listeningMode: 'ALL'` is needed with Docker's default `bridge` network.
- The `/etc/pihole` volume keeps databases and configuration across upgrades.
- Without a password variable, a random password is assigned.

**Tags.** `latest` is the newest release, date-based tags such as `2022.04.0` pin a release, and `nightly` is built from the `development` branch and is the most experimental.

**Checklist**

1. Set `TZ` so logs rotate at local midnight.
2. Choose and set the password.
3. Run `docker compose up -d`.
4. Open `http://pi.hole/admin/` to test.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Docker (docker); Docker Configuration (docker/configuration). Nothing needed removing.
Method: documentation only; no commands were run.
