---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-server-cli-flags
name: portainer-server-cli-flags
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [cli, flags, configuration, logging, ports]
level: practitioner
status: docs-checked
description: "Reference the most useful Portainer Server command-line flags for admin bootstrap, ports, logging, TLS, snapshots and reverse-proxy use."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flags are appended after the image name in the run command.

- Bootstrap: `--admin-password` (bcrypt hash) or `--admin-password-file` (path to a file holding the plain text password) set the first admin; they cannot change the password later. `--license-key` is Business Edition only.
- Ports: `--bind` (default `:9000`), `--bind-https` (`:9443`), `--http-disabled` to serve HTTPS only, `--tunnel-addr` and `--tunnel-port` for the Edge tunnel (use `--tunnel-port 8001` together with `-p 8001:8001` to change it).
- Data: `--data` (default `/data`), `--compact-db` to reclaim disk space at startup.
- Docker connection: `-H`/`--host`, `--tlsverify`, `--tlscacert`, `--tlscert`, `--tlskey`, `--tlsskipverify`.
- Logging: `--log-level` (for example DEBUG) and `--log-mode` (`PRETTY`, `NOCOLOR`, `JSON`).
- Behaviour: `--snapshot-interval` (default 5m), `--edge-compute`, `--hide-label`, `--templates`, `--logo`.
- Proxy: `--base-url` for subpaths and `--trusted-origins` for Origin invalid errors.
- Security: `--no-csp` disables the Content-Security-Policy header, which the docs strongly advise against.
- Certificates: `--sslcert`, `--sslkey` (defaults `/certs/portainer.crt` and `/certs/portainer.key` on Linux); `--mtlscacert`, `--mtlscert` and `--mtlskey` are Business Edition only.

`--http-enabled` serves HTTP as well as HTTPS, while `--http-disabled` overrides it. `--sslcacert` is deprecated in favour of mTLS. `--version` prints the version. Debug logging can also be enabled through Settings.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Fixed: the mTLS flags are Business Edition only; added the file nature of the password-file flag and the certificate defaults. Removed: the claim that Settings debug logging needs no restart and is handy briefly.

Method: documentation only; no commands were run.
