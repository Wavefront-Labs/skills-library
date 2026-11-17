---
id: computing-software.networking-hardware-and-wireless.traefik.acme-certificate-resolvers
name: acme-certificate-resolvers
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, acme, letsencrypt, certresolver, httpchallenge, tlschallenge, dnschallenge]
level: practitioner
status: docs-checked
description: "Obtain Let's Encrypt certificates with an ACME certificatesResolver using HTTP, TLS or DNS challenges and persistent acme.json storage."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/tls/certificate-resolvers/acme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# acme certificate resolvers
Define a resolver in the install config, then name it on routers with `tls.certResolver`.

```yaml
certificatesResolvers:
  myresolver:
    acme:
      email: you@example.com
      storage: acme.json
      httpChallenge:
        entryPoint: web
```
Options: `storage` (required), `caServer` (defaults to Let's Encrypt production), `preferredChain`, `keyType` (default RSA4096), `eab.kid` / `eab.hmacEncoded` for external account binding, and `certificatesDuration` (2160 hours). Challenges: `httpChallenge.entryPoint` (must be reachable on port 80) with `delay`, `tlsChallenge` (needs port 443), and `dnsChallenge.provider` with `resolvers` and `propagation` (`delayBeforeChecks`, `disableChecks`, `requireAllRNS`, `disableANSChecks`). Wildcard certificates need the DNS challenge.

Gotchas: the reference says redirection is fully compatible with the HTTP-01 challenge. Wildcard certificates can only be generated through a DNS-01 challenge, and a double wildcard such as `*.*.local.com` is not possible. By default Traefik manages 90-day certificates and starts renewing them 30 days before expiry.

## Checked
2026-11-03. Confirmed against the Traefik ACME certificate resolver reference page: options and defaults (`storage`, `caServer`, `keyType`, `certificatesDuration` 2160, challenge options), the port 80 and 443 reachability requirements, the redirection note and the wildcard/DNS-01 rule. Removed: the unsupported advice that `acme.json` loss causes rate limits, the staging-first advice, the claim that a redirect can block the HTTP challenge (the page says the opposite), and the openssl Verify step.
Method: documentation only; no commands were run.


