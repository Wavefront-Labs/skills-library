---
id: computing-software.networking-hardware-and-wireless.traefik.serverstransport-backend-tls
name: serverstransport-backend-tls
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, serverstransport, insecureskipverify, rootcas, forwardingtimeouts, backend-tls]
level: practitioner
status: docs-checked
description: "Configure TLS and timeouts for Traefik-to-backend connections with ServersTransport instead of skipping verification globally."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/load-balancing/serverstransport.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# serverstransport backend tls
`serversTransport` shapes how Traefik talks to backends. Fields: `serverName`, `certificates` (client certificate for mTLS to the backend), `insecureSkipVerify`, `rootCAs`, `cipherSuites`, `minVersion`, `maxVersion`, `maxIdleConnsPerHost` (0 means 2), `disableHTTP2`, `peerCertSANs` (list of type/value) and `forwardingTimeouts` with `dialTimeout` (30s), `responseHeaderTimeout` (0s, no limit), `readTimeout` and `writeTimeout`.

```yaml
http:
  serversTransports:
    internal-ca:
      serverName: backend.internal
      rootCAs:
        - /certs/internal-ca.pem
      forwardingTimeouts:
        responseHeaderTimeout: 60s
  services:
    app:
      loadBalancer:
        serversTransport: internal-ca
        servers:
          - url: "https://10.0.0.5:8443"
```
Gotchas: `insecureSkipVerify: true` removes backend authentication; prefer `rootCAs` plus `serverName`. Slow backends hit `responseHeaderTimeout` only if you set it above zero. The transport is referenced by name, with `@provider` when defined elsewhere.

## Checked
2026-11-03. Confirmed against the Traefik ServersTransport reference page and the HTTP service page: all listed fields and defaults (`maxIdleConnsPerHost` 0 uses 2, `dialTimeout` 30s, `responseHeaderTimeout` 0s means no timeout), `@provider` naming such as `customTransport@file`, and `insecureSkipVerify` meaning. Removed: the curl and backend-log Verify step.
Method: documentation only; no commands were run.


