---
id: computing-software.networking-hardware-and-wireless.traefik.entrypoints-core-settings
name: entrypoints-core-settings
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, entrypoints, address, asdefault, listeners, install-configuration]
level: practitioner
status: docs-checked
description: "Define Traefik entrypoints with address, default selection, and the observability and middleware hooks attached at entrypoint level."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/entrypoints.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# entrypoints core settings
An entrypoint is a network listener Traefik opens. The key option is `address` (for example `:80` or `:8443/tcp`). The address format is `[host]:port[/tcp|/udp]` and TCP is the default. `asDefault` marks an entrypoint as one used by HTTP and TCP routers that do not define `entryPoints`; if no entrypoint sets it, all HTTP and TCP entrypoints are the defaults.

```yaml
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: myresolver
```
Related entrypoint settings in the reference: `http.middlewares` (middlewares applied to every router on this entrypoint), `http.tls` with `options` and `certResolver`, `http.sanitizePath`, `http.maxHeaderBytes`, `http.maxHeaderValueCount` (exceeding it gives 431), `http2.maxConcurrentStreams`, `reusePort`, and an `observability` block with `accessLogs`, `metrics`, `tracing` and `traceVerbosity`.

Gotcha: `http.tls` enables TLS on every router attached to the entrypoint, with a generated self-signed certificate if none is set. A router that defines its own `tls` section, even an empty one, replaces the entrypoint TLS settings with no merge.

## Checked
2026-11-03. Confirmed against the Traefik entrypoints reference page: `address` format, `asDefault`, `http.middlewares`, `http.tls` with `options` and `certResolver`, `http.sanitizePath`, `http.maxHeaderBytes`, `http.maxHeaderValueCount` (431), `http2.maxConcurrentStreams`, `reusePort` and the `observability` block with `traceVerbosity`. Removed: the curl and dashboard Verify step.
Method: documentation only; no commands were run.


