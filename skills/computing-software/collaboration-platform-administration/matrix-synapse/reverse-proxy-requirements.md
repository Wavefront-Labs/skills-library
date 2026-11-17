---
id: computing-software.collaboration-platform-administration.matrix-synapse.reverse-proxy-requirements
name: reverse-proxy-requirements
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, reverse-proxy, x-forwarded-for, x-forwarded-proto, x-forwarded, listeners, nocanon, health-check]
level: practitioner
status: docs-checked
description: "Put a reverse proxy in front of Synapse: paths to forward, X-Forwarded headers, the x_forwarded listener flag, no URI normalisation, client versus federation port, and /health."
sources:
  - https://element-hq.github.io/synapse/latest/reverse_proxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A reverse proxy lets clients use port 443 without Synapse binding a privileged port. Forward requests for `/_matrix` and `/_synapse/client` to Synapse and set the `X-Forwarded-For` and `X-Forwarded-Proto` request headers.

Clients default to port 443 and servers to 8448; the docs call these the client port and federation port. In the examples, clients use `https://matrix.example.com` and other servers use `https://example.com:8448`.

Critical rule: the proxy must not canonicalise or normalise the requested URI, for example by decoding `%xx` escapes. Apache does so unless you specify `nocanon`. In nginx, do not add any path, even a single `/`, after the port in `proxy_pass`, or signature verification errors result.

Homeserver side: set `x_forwarded: true` in the port 8008 listener so Synapse records client IPs and builds redirect URLs correctly, and consider `bind_addresses: ['127.0.0.1']` to listen on localhost only. Do not bind to 127.0.0.1 in a containerised Synapse, as that stops it answering proxied traffic. You can also set `request_id_header` so Synapse reuses the proxy's request ID.

Other details from the page's examples: nginx needs `client_max_body_size` raised to match `max_upload_size` (the example uses 50M) and `proxy_http_version 1.1` because responses may be chunked. Apache needs `AllowEncodedSlashes NoDecode`, and missing `ProxyPreserveHost on` can cause a redirect loop. Apache's `mod_security2` appears incompatible with Synapse; disable `SecRuleEngine` for those VirtualHosts.

Each HTTP listener exposes `/health`, which always returns 200 OK and is not logged. Admin endpoints live under `/_synapse/admin`; the docs advise against exposing them publicly without good reason.

## Checked

2026-11-04. Confirmed against the Synapse reverse proxy page: forwarded paths and headers, URI normalisation rule, x_forwarded and bind_addresses, request_id_header, nginx and Apache notes, /health, admin endpoints. Nothing removed.
Method: documentation only; no commands were run.
