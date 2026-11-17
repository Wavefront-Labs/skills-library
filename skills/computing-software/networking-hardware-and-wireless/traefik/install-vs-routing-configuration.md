---
id: computing-software.networking-hardware-and-wireless.traefik.install-vs-routing-configuration
name: install-vs-routing-configuration
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, static-configuration, dynamic-configuration, traefik-yml, cli-flags, environment-variables]
level: practitioner
status: docs-checked
description: "Separate Traefik install configuration (file, CLI or env, mutually exclusive) from hot-reloaded routing configuration."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/getting-started/configuration-overview.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/dynamic-configuration-methods.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# install vs routing configuration
Traefik has two kinds of configuration. The install (startup, formerly static) configuration sets providers and entrypoints and is read at start. The routing (formerly dynamic) configuration defines routers, services and middlewares, comes from providers, and is hot-reloaded without dropping connections.

The install configuration has three mutually exclusive sources, evaluated in this order: a configuration file, command-line arguments, environment variables. At startup Traefik looks for `traefik.yml` (or `traefik.yaml` / `traefik.toml`) in `/etc/traefik/`, `$XDG_CONFIG_HOME/` and `$HOME/.config/`.

```yaml
# traefik.yml
providers:
  file:
    directory: "/etc/traefik/dynamic"
entryPoints:
  web:
    address: ":80"
```
Naming a sub-option parent is enough to enable it with defaults: `--providers.docker` enables the Docker provider without `--providers.docker.endpoint`.

Gotcha: do not mix sources; if you pass a CLI flag, the file is not merged in. Put routing data in providers, not the install file.

## Checked
2026-11-03. Confirmed against the Traefik configuration overview page: install versus routing configuration, hot reload, the three mutually exclusive sources evaluated in order, the `traefik.yml` search locations and the `--providers.docker` default behaviour. Removed: the claim about HTTPS certificates changing without restart and the debug-logging Verify step.
Method: documentation only; no commands were run.


