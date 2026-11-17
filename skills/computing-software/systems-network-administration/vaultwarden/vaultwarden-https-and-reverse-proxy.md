---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-https-and-reverse-proxy
name: vaultwarden-https-and-reverse-proxy
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, https, tls, rocket-tls, reverse-proxy, caddy, web-crypto, fullchain]
level: practitioner
status: docs-checked
description: "Put HTTPS in front of Vaultwarden: why the web vault needs it, why a reverse proxy beats Rocket built-in TLS, and the ROCKET_TLS certificate rules if you must use it."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Enabling-HTTPS", "https://github.com/dani-garcia/vaultwarden/wiki/Hardening-Guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden HTTPS

The Bitwarden web vault depends on web crypto APIs that browsers only expose in secure contexts, so HTTPS is effectively mandatory. The recommended method is a reverse proxy that terminates TLS (Caddy is suggested for beginners because it obtains Let's Encrypt certificates automatically). The wiki calls Rocket's own HTTPS "relatively immature and limited" and the hardening guide says it is not production ready.

If you must terminate TLS in Vaultwarden:

```
ROCKET_TLS={certs="/path/to/certs.pem",key="/path/to/key.pem"}
```

- Both files must be PEM; the extension does not matter.
- Use RSA keys and certificates. Rocket cannot parse ECC/ECDSA, and the error message is misleading.
- Use `fullchain.pem`, not `cert.pem`: clients such as Android need the intermediate certificate.
- In Docker the paths are those inside the container; if the files are symlinks, both link and target must be reachable there.
- On a non-443 port, include the port when connecting.

Hardening notes: serve only under the hostname (strict SNI), and redact the `access_token` query parameter in proxy logs. Behind a proxy, pass the client IP (for example via `X-Real-IP`) or the logs and Fail2Ban only ever see 127.0.0.1.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Enabling-HTTPS and Hardening-Guide.
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
