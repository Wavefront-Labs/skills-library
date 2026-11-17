---
id: computing-software.collaboration-platform-administration.matrix-synapse.tls-listener-and-client-well-known
name: tls-listener-and-client-well-known
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, tls, certificate, listeners, public-baseurl, well-known, client, cors, fullchain]
level: practitioner
status: docs-checked
description: "Serve Synapse over HTTPS with a TLS listener and certificate paths, or via proxy; publish the client .well-known file with CORS headers and set public_baseurl to match."
sources:
  - https://element-hq.github.io/synapse/latest/setup/installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Out of the box Synapse listens on `http://localhost:8008`, fine for testing only. The recommended route to HTTPS is a reverse proxy; alternatively Synapse can serve TLS itself. Add a TLS-enabled listener:

```yaml
listeners:
  - port: 8448
    type: http
    tls: true
    resources:
      - names: [client, federation]
```

Then set `tls_certificate_path` and `tls_private_key_path`; you provision the certificates yourself. If using your own certificate, use a `.pem` with the full chain including intermediates (with certbot, use `fullchain.pem`, not `cert.pem`).

The client well-known is optional but lets users type their full ID (`@user:<server_name>`) into clients that support well-known lookup, which then auto-configure the homeserver and identity server URLs. `https://<server_name>/.well-known/matrix/client` should return:

```json
{
  "m.homeserver": {
    "base_url": "https://<matrix.example.com>"
  }
}
```

An `m.identity_server` object with its own `base_url` can be added. Browser clients need CORS headers; the docs recommend `Access-Control-Allow-Origin: *`. The nginx form is:

```nginx
location /.well-known/matrix/client {
    return 200 '{"m.homeserver": {"base_url": "https://<matrix.example.com>"}}';
    default_type application/json;
    add_header Access-Control-Allow-Origin *;
}
```

Also set `public_baseurl` in `homeserver.yaml` to the URL clients use, the same value as the `base_url` above:

```yaml
public_baseurl: "https://<matrix.example.com>"
```

Server-to-server delegation uses a different file, covered in the delegation skill.

## Checked

2026-11-09. Confirmed against the Synapse installation page: default localhost:8008 listener, reverse proxy as the recommended route, the TLS listener example, certificate options and fullchain guidance, client well-known JSON, CORS header and public_baseurl. Nothing removed.

Method: docs-checked 2026-11-09 against element-hq.github.io/synapse/latest/setup/installation.html (TLS, well-known and public_baseurl sections).
