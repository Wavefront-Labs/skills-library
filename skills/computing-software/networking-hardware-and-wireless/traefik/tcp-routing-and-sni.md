---
id: computing-software.networking-hardware-and-wireless.traefik.tcp-routing-and-sni
name: tcp-routing-and-sni
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, tcp-router, hostsni, alpn, tls-passthrough, tcp]
level: practitioner
status: docs-checked
description: "Route raw TCP with HostSNI, ClientIP and ALPN rules, TLS passthrough versus termination, and TCP-before-HTTP precedence."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/tcp/routing/router.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/tcp/routing/rules-and-priority.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/tcp/tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tcp routing and sni
TCP routers sit under `tcp.routers` and match connections with `HostSNI`, `HostSNIRegexp`, `ClientIP` and `ALPN`. If HTTP and TCP routers share an entrypoint, TCP routers are evaluated first and the HTTP routers apply only when no TCP router matches. Router names cannot contain `@`.

```yaml
tcp:
  routers:
    db:
      entryPoints: [tcp-ep]
      rule: "HostSNI(`db.example.com`)"
      service: db-svc
      tls:
        passthrough: true
```
A router with a `tls` block handles only TLS connections and by default terminates them. `passthrough: true` forwards encrypted bytes untouched. SNI is a TLS extension, so non-TLS routers can only use `HostSNI(`*`)` as a catch-all. `*.example.com` matches foo.example.com but not foo.bar.example.com, while `**.example.com` matches both (v3 rule syntax, the default).

Gotchas: do not confuse `HostSNI` with HTTP `Host`. Non-ASCII domains need punycode-encoded values. Prefer a `HostSNI` wildcard over `HostSNIRegexp`, because it allows attaching a TLS option and is more efficient. The character `@` is not allowed in a router name.

## Checked
2026-11-03. Confirmed against the Traefik TCP router, rules and priority, and TCP TLS reference pages: matchers, TCP-before-HTTP evaluation, the `HostSNI(`*`)` non-TLS case, TLS termination by default and `passthrough`, wildcard behaviour, punycode and the `@` rule. Removed: the apex-matching claim, the claim about database drivers sending no SNI, and the openssl Verify step.
Method: documentation only; no commands were run.


