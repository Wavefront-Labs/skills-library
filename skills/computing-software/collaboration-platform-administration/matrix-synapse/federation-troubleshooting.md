---
id: computing-software.collaboration-platform-administration.matrix-synapse.federation-troubleshooting
name: federation-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, federation, troubleshooting, federation-tester, 401, 308-redirect, reverse-proxy]
level: practitioner
status: docs-checked
description: "Diagnose Synapse federation failures: use the federation tester and its JSON API, recognise the 401 Unauthorized join failure, and avoid the 308 redirect trap."
sources:
  - https://element-hq.github.io/synapse/latest/federate.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Federation lets users on different servers share rooms, which requires other servers to reach yours. By default the `server_name` is also the host others contact, on port 8448 over TLS. The preferred way to listen on 8448 is a reverse proxy; if Synapse runs elsewhere or on another port, use delegation instead.

Start diagnosis with the Matrix federation tester at `https://matrix.org/federationtester`. The JSON API behind it, `https://matrix.org/federationtester/api/report?server_name=DOMAIN` (replace `DOMAIN` with your `server_name`), returns extra detail when hit directly.

Typical symptoms and what they mean:

- When your server tries to join a room and is rejected with `401: Unauthorized`, other servers in the room generally could not access yours. Joining a room over federation needs connections in both directions.
- People on other servers cannot join rooms you invite them to. This is commonly an incorrectly configured reverse proxy; check the proxy against the reverse proxy documentation.

Known issue from the docs: HTTP `308 Permanent Redirect` responses are not followed by federating servers because of a missing feature in the HTTP library Synapse uses. This can produce `M_UNKNOWN` or `401 Unauthorized`. It affects apex-to-www redirects (for example `example.com` to `www.example.com`) and the Kubernetes Nginx Ingress module, which uses 308 by default. Switching to `301 Moved Permanently` may be an option. The docs say 308 will be supported properly in a future release.

To join a room as a first test, the docs suggest `#synapse:matrix.org`.

## Checked

2026-11-04. Confirmed against the Synapse Setting up federation page: default port and reverse proxy, federation tester and JSON API, 401 and invite symptoms, 308 redirect issue. Trimmed two inferences not on the page.
Method: documentation only; no commands were run.
