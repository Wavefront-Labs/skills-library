---
id: computing-software.messaging-and-integration.prosody.http-ports-interfaces
name: http-ports-interfaces
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, http, https, ports, interfaces, http-paths]
level: practitioner
status: docs-checked
description: "Prosody HTTP server defaults: http_ports 5280 on localhost, https_ports 5281 on all interfaces, https_certificate, https_ssl, and http_paths."
sources:
  - https://prosody.im/doc/http
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP ports and interfaces

Defaults:

```lua
http_ports = { 5280 }
http_interfaces = { "127.0.0.1", "::1" }

https_ports = { 5281 }
https_interfaces = { "*", "::" }
```

HTTP listens on localhost only; HTTPS on all interfaces. HTTP plugins are reachable through both, so a default public base URL is on port 5281.

Certificates: `https_certificate` picks a certificate by path (key alongside); `https_ssl` sets one global certificate and disables SNI.

Move a module's path with `http_paths`:

```lua
http_paths = { bosh = "/http-bind" }
```

Verify: `prosodyctl shell http list` shows each module's URL, and `https://example.com:5281/` answers with a valid certificate.

## Checked

2026-11-04. Read the Prosody HTTP server page: the default http_ports, http_interfaces, https_ports and https_interfaces values, plugins reachable through both services with https://host:5281/ as the base URL, https_certificate with the key beside it, https_ssl disabling SNI, and http_paths all match. Nothing removed.

Method: documentation only; no commands were run.
