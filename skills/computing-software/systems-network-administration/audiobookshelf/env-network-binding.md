---
id: computing-software.systems-network-administration.audiobookshelf.env-network-binding
name: env-network-binding
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [environment-variables, host, port, proxy-support, http-proxy]
level: practitioner
status: docs-checked
description: "Control the Audiobookshelf bind address and port with HOST and PORT, and understand the experimental EXP_PROXY_SUPPORT option."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/linux/4.linux-install-rpm.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/linux/5.linux-install-nix.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Network variables from the environment page:

| Variable | Default | Meaning |
| --- | --- | --- |
| `HOST` | unset | Address to bind. Use `127.0.0.1` for localhost only, or leave unset for all interfaces. |
| `PORT` | unset | TCP port to listen on. |
| `EXP_PROXY_SUPPORT` | unset | Experimental: respects `HTTP_PROXY` and `HTTPS_PROXY` environment variables and disables the SSRF request filter. |

Examples: the RHEL package config uses `HOST=127.0.0.1` so the service is only reachable through a reverse proxy on the same machine; setting `HOST=0.0.0.0` listens on all interfaces. On NixOS the equivalent flags are `--host` and `--port`. In Docker, leave the container on its internal port 80 and change only the published port in the `ports:` mapping.

Note the side effect: enabling `EXP_PROXY_SUPPORT` also turns off the SSRF filter, so only use it when your outbound traffic must go through a proxy and you accept losing that protection.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Environment Configuration page (Network table), RHEL install page, NixOS page.

Method: documentation only; no commands were run.
