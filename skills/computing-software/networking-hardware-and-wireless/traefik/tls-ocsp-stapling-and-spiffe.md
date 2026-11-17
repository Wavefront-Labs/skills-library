---
id: computing-software.networking-hardware-and-wireless.traefik.tls-ocsp-stapling-and-spiffe
name: tls-ocsp-stapling-and-spiffe
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, ocsp, stapling, spiffe, svid, workload-api]
level: practitioner
status: docs-checked
description: "Enable OCSP stapling and SPIFFE workload identity in Traefik, with the caveats on in-memory cache and startup waiting."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/tls/ocsp.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/tls/spiffe.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls ocsp stapling and spiffe
OCSP stapling is switched on with `ocsp: {}` in the install config. Traefik checks every certificate in the store that provides an OCSP responder URL, including the default certificate, and staples the response to the TLS handshake. The check runs when the certificate is loaded and then once every hour until it is successful, at the halfway point before the update date. Responses are cached in memory and not persisted across restarts; after a certificate is no longer provided its response has a 24 hour TTL. `ocsp.responderOverrides` sets responder URLs to use instead of the certificate's.

Traefik can connect to the SPIFFE Workload API to obtain an X509-SVID that secures connections to SPIFFE-enabled backends; `spiffe.workloadAPIAddr` is the address of the Workload API.

```yaml
ocsp: {}
spiffe:
  workloadAPIAddr: localhost
```
A ServersTransport must opt in to SPIFFE to use the identity for backend connections.

Gotchas: with SPIFFE enabled, Traefik waits for the first SVID before starting. If it hangs, check that Traefik is registered as a workload in your SPIFFE infrastructure.

## Checked
2026-11-03. Confirmed against the Traefik OCSP and SPIFFE reference pages: `ocsp: {}`, check timing, caching and TTL, `responderOverrides`, `spiffe.workloadAPIAddr`, the stall warning and the per-ServersTransport opt-in. Removed: the socket path example (the page uses `localhost`), the start-the-agent advice, the failing-responder claim and the openssl Verify step.
Method: documentation only; no commands were run.

