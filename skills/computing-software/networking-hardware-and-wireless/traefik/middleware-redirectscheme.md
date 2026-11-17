---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-redirectscheme
name: middleware-redirectscheme
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, redirectscheme, https-redirect, permanent, port, middleware]
level: practitioner
status: docs-checked
description: "Redirect to another scheme such as https with redirectScheme, including permanent redirects, ports and trusting the last proxy hop."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/redirectscheme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware redirectscheme
`redirectScheme` redirects the request when its scheme differs from the configured one. Options: `scheme` (required; scheme of the new URL), `permanent` (default false) and `port` (port of the new URL; set a string, not a number).

```yaml
http:
  middlewares:
    test-redirectscheme:
      redirectScheme:
        scheme: https
        permanent: true
        port: "443"
```
Gotcha: when another reverse proxy sits between the client and Traefik, that last hop must be trusted on the entrypoint. Otherwise Traefik cleans up the `X-Forwarded` headers from it, and this middleware, which relies on them to determine the scheme, does not work as intended.

## Checked
2026-11-03. Confirmed against the Traefik redirectScheme reference page (docs/content/reference/routing-configuration/http/middlewares/redirectscheme.md): options, defaults, string port, trusted last-hop warning. Removed: the 301/308 versus 302/307 status claim, the entrypoint `http.redirections` suggestion, the "redirect loops" wording, and the curl Verify step.
Method: documentation only; no commands were run.
