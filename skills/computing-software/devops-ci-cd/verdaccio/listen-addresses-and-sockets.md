---
id: computing-software.devops-ci-cd.verdaccio.listen-addresses-and-sockets
name: listen-addresses-and-sockets
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [listen, unix-socket, ipv6, listen-directive, bind-address, port-4873]
level: practitioner
status: docs-checked
description: "Choose Verdaccio's listen address with the listen key: host, port, all interfaces, IPv6, https or a unix socket, and the CLI override."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/server-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default is port 4873. Set it in the config or with `--listen`:

```yaml
listen:
# - localhost:4873            # default
# - http://localhost:4873     # same thing
# - 0.0.0.0:4873              # all addresses (INADDR_ANY)
# - https://example.org:4873  # https
# - "[::1]:4873"              # ipv6
# - unix:/tmp/verdaccio.sock  # unix socket
```
Server setup page: to be reachable from other machines use `listen: 0.0.0.0:4873`; on an Amazon EC2 instance you must change it that way too.

Gotchas:
- The `--listen` / `-l` CLI flag overrides the config key.
- In Docker, any `listen` host:port in `conf/config.yaml` is ignored; use `VERDACCIO_PORT`, `VERDACCIO_PROTOCOL` and `VERDACCIO_ADDRESS` (default `[::]` on 7.x, `0.0.0.0` on 6.x).
- Behind nginx or Apache keep the default local listen and proxy to it.

## Checked

2026-11-04. Confirmed against the Configuration page (listen values), Server Configuration page (0.0.0.0:4873, EC2), CLI page (--listen/-l override) and Docker/Environment pages (ignored listen, VERDACCIO_ADDRESS). Removed: the closing Verify tip.
Method: documentation only; no commands were run.
