---
id: computing-software.networking-hardware-and-wireless.traefik.entrypoint-redirections-and-http3
name: entrypoint-redirections-and-http3
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, redirections, http3, advertisedport, https-redirect, entrypoints]
level: practitioner
status: docs-checked
description: "Redirect an entire entrypoint to HTTPS and enable HTTP/3 with the required TCP entrypoint and advertisedPort."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/entrypoints.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# entrypoint redirections and http3
Redirect all traffic from one entrypoint to another without routers using `http.redirections.entryPoint`: options `to` (required: an entrypoint name such as `websecure`, or a port such as `:443`), `scheme` (default https), `permanent` and `priority`.

```yaml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
          permanent: true
  websecure:
    address: ":443"
    http3:
      advertisedPort: 443
```
HTTP/3 is enabled with `http3` on an entrypoint. It requires a TCP entrypoint, because HTTP/3 always starts as a TCP connection that is then upgraded to UDP; usually that is the entrypoint used for TLS traffic. `http3.advertisedPort` sets the UDP port advertised as the HTTP/3 authority in the alt-svc header; it defaults to the entrypoint's port and is useful when the public port differs from the listening one.

Gotchas: by default Traefik creates an internal ACME router with the highest priority to handle ACME challenges. With `allowACMEByPass: true` on the entrypoint, user-defined routers can handle challenge requests instead, and a configured HTTP redirect then excludes `/.well-known/acme-challenge/`. The HTTP/3 server listens on UDP port N of the TCP entrypoint, so port N cannot be used by another UDP entrypoint, and only routers with TLS are usable with HTTP/3.

## Checked
2026-11-03. Confirmed against the Traefik entrypoints reference page: `http.redirections.entryPoint` options and defaults, `http3`, `http3.advertisedPort`, the HTTP/3 TCP and UDP port note and `allowACMEByPass` behaviour. Removed: the claim that redirections hit ACME challenges by default, the firewall advice and the curl Verify steps.
Method: documentation only; no commands were run.


