---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-troubleshooting-false-down-and-ipv6
name: uptime-kuma-troubleshooting-false-down-and-ipv6
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [uptime-kuma-down, docker-networking, ipv6, curl-from-container, false-down, firewall]
level: practitioner
status: docs-checked
description: "Debug Uptime Kuma reporting DOWN for reachable services: test from inside the container and enable Docker IPv6."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Troubleshooting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting false DOWN reports

When a monitor says DOWN but the service is reachable from your own machine, first decide whether Uptime Kuma, Docker networking or a firewall is at fault. Test from the monitor's own network position:

```bash
docker exec -it uptime-kuma bash
apt update && apt --yes install curl
curl https://example.com
ping example.com
```

Remember Docker has several network types and only some can reach the local network or remote networks.

IPv6: Docker does not support IPv6 out of the box. If the target is IPv6-only, enable IPv6 in the Docker daemon per Docker docs. In Compose, add a network with `enable_ipv6: true` and attach the service:

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:2
    volumes:
      - ./data:/app/data
    ports:
      - 3001:3001
    restart: unless-stopped
    networks:
      - uptime-kuma-net
networks:
  uptime-kuma-net:
    enable_ipv6: true
```

Related settings: `NODE_EXTRA_CA_CERTS` adds self-signed CA certificates and `NODE_OPTIONS=--insecure-http-parser` helps with `Invalid header value char` errors when a site uses a WAF (Environment Variables page). In v2, newly created monitors default to 0 retries (migration guide).

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Troubleshooting page (container debugging, Docker network types, IPv6 compose example), Environment Variables page and Migration From v1 To v2 (default retries). Removed: The unconfirmed bridge-network advice, the claim that the environment variable page lists false-DOWN causes, and the verify line.

Method: documentation only; no commands were run.
