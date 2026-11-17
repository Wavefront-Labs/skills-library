---
id: computing-software.systems-network-administration.headscale.cli-help-and-socket
name: cli-help-and-socket
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, cli, help, unix-socket, permissions]
level: intro
status: docs-checked
description: "Use the headscale CLI: built-in help, running it in a container, and the unix socket permissions that make non-root commands fail."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/getting-started.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headscale CLI basics

```
headscale help
headscale <COMMAND> --help
```

In a container, prefix with `docker exec -it headscale`.

## Socket permissions

The CLI talks to the server over a unix socket. Config keys (from the example config):

```yaml
unix_socket: /var/run/headscale/headscale.sock
unix_socket_permission: "0770"
```

Quote the permission: YAML reads an unquoted `0770` as the number 504.

By default only the user `headscale` or `root` can access the unix socket (`/var/run/headscale/headscale.sock`). For another local user, use `sudo`, run the commands as user `headscale`, or add your user to the `headscale` group. To verify, run `headscale users list`.

## Other config

Use `-c` or `--config` (or env `HEADSCALE_CONFIG`) to point at a different config file (configuration page).

## Common commands used elsewhere

- `headscale users create <USER>`, `headscale users list`
- `headscale nodes list`
- `headscale preauthkeys create --user <USER>`
- `headscale auth register --user <USER> --auth-id <AUTH_ID>`

## Checked

2026-11-04. Confirmed against the Headscale getting-started page (help, container prefix, socket access methods, user and registration commands) and config-example.yaml (`unix_socket`, quoted `unix_socket_permission`). Removed the Gotcha about the remote CLI, which neither cited page covers.

Method: documentation only; no commands were run.
