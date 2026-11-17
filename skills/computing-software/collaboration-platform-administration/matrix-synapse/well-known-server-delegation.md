---
id: computing-software.collaboration-platform-administration.matrix-synapse.well-known-server-delegation
name: well-known-server-delegation
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, delegation, well-known, federation, server-name, port-8448]
level: practitioner
status: docs-checked
description: "Delegate Matrix federation traffic with /.well-known/matrix/server so server_name stays example.com while Synapse runs elsewhere, including serve_server_wellknown and SRV caveats."
sources:
  - https://element-hq.github.io/synapse/latest/delegate.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Your `server_name` is the domain at the end of user IDs and room aliases, and by default other homeservers try to reach you at `https://<server_name>:8448/`. Delegation lets you keep `server_name: example.com` while federation traffic goes to a different host or port, for example `synapse.example.com:443`.

You need delegation only when your APIs are not reachable on port 8448 at the domain `server_name` points to. If a reverse proxy already serves TLS for that domain on 8448, skip it.

The recommended method is `.well-known`. `https://<server_name>/.well-known/matrix/server` (always fetched on the default HTTPS port 443) must return JSON with an `m.server` key:

```json
{
    "m.server": "synapse.example.com:443"
}
```

The port is optional and defaults to 8448 when omitted. You can serve the file from nginx, Apache or HAProxy; the reverse proxy page has examples.

If `https://<server_name>` is routed to Synapse itself, you can instead set this in `homeserver.yaml`:

```yaml
serve_server_wellknown: true
```

This only works when the apex name goes to Synapse, so it is generally unsuitable when Synapse lives at a subdomain.

SRV DNS delegation exists but the docs say it is generally not recommended: TLS certificates are hard to configure correctly and it offers little over `.well-known`. SRV also covers only server-to-server traffic. Global client defaults (a Jitsi endpoint, say) still need files under `/.well-known/` on the `server_name` domain.

Check the result with the federation tester described in the federation setup docs.

## Checked

2026-11-04. Confirmed against the Synapse Delegation page and the Setting up federation page (federation tester): well-known file, m.server format and default port 8448, serve_server_wellknown, SRV caveats, when delegation is needed. Nothing removed.
Method: documentation only; no commands were run.
