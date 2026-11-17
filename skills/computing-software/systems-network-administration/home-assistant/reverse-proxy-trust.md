---
id: computing-software.systems-network-administration.home-assistant.reverse-proxy-trust
name: reverse-proxy-trust
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [reverse-proxy, trusted-proxies, x-forwarded-for]
level: advanced
status: docs-checked
description: "Make Home Assistant accept requests from a reverse proxy by enabling Trust X-Forwarded-For and listing Trusted proxies in the Network settings."
sources:
  - https://www.home-assistant.io/docs/configuration/remote/
  - https://www.home-assistant.io/docs/authentication/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: put Home Assistant behind a reverse proxy without requests being blocked.

A reverse proxy is an intermediary server in front of Home Assistant. Without explicit trust, requests through it are blocked by design.

Steps:

1. Go to Settings > System > Network.
2. Under HTTP server, turn on Trust X-Forwarded-For.
3. Add the proxy to Trusted proxies.
4. Set the external address under Home Assistant URL if you have not (see the remote-access-options skill).

Details of the proxy settings live in the HTTP integration documentation under reverse proxies. If the proxy or a CDN caches responses, the HTTP integration docs also have a section on caching behind a reverse proxy or CDN.

Interaction with trusted networks authentication:

You cannot trust a network that you also use in `trusted_proxies`. The `trusted_networks` authentication provider then fails with an error that the computer is not allowed. Keep proxy addresses out of the trusted network ranges, for example:

```yaml
homeassistant:
  auth_providers:
    - type: trusted_networks
      trusted_networks:
        - 192.168.0.0/24
    - type: homeassistant
```

Make sure the proxy address is not inside the listed range. Always keep `type: homeassistant` as a fallback (see the auth-providers skill).

## Checked

2026-11-04. Confirmed against the Remote access page and the Network configuration page. Dropped the unsupported 'Save, then' wording from step 4.

Method: documentation only; no commands were run.
