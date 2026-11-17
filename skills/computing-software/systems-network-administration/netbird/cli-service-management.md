---
id: computing-software.systems-network-administration.netbird.cli-service-management
name: cli-service-management
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, service-install, service-reconfigure, service-env, daemon]
level: practitioner
status: docs-checked
description: "Manage the NetBird daemon with netbird service: install, start, stop, restart, reconfigure with service-env, reset-params, and install-time feature restrictions."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/cli.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/lazy-connection.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run `netbird service` subcommands with elevated permissions.

- `install`: install the daemon. Global flags configure it (for example `--log-level debug`, `--config /path/to/config.json`). Service-specific flags: `--disable-networks`, `--disable-profiles`, `--disable-update-settings` (lock those features for non-admin users) and `--service-env KEY=VALUE[,KEY=VALUE]`.
- `start`, `stop`, `restart`, `status`: control the daemon.
- `uninstall`: remove the service.
- `reconfigure [--service-env KEY=VALUE]`: stops the service, updates its configuration and restarts it if it was running.
- `reset-params`: remove the saved `service.json` so the next install uses defaults.

Install parameters (including `--disable-profiles`, `--disable-update-settings`, `--service-env`) are persisted to `service.json` and survive uninstall/reinstall. To clear them run `netbird service reset-params` then `netbird service reconfigure`. `--disable-networks` is also persisted there and has no environment-variable equivalent; `NB_DISABLE_PROFILES` and `NB_DISABLE_UPDATE_SETTINGS` exist for the other two.

Environment variables the daemon should see are set with `--service-env`. Example from the lazy-connection docs:

```
sudo netbird service reconfigure --service-env NB_LAZY_CONN=on
```

Typical managed-machine install:
```
sudo netbird service install --setup-key <KEY> --disable-profiles --disable-update-settings
```

## Checked

2026-11-04: read the CLI page (get-started/cli) service sections and the lazy-connection page. Confirmed every subcommand, flag, the service.json persistence note and the NB_LAZY_CONN example. Removed the claim about binary-tarball or Homebrew installs, which the pages do not state.

Method: documentation only; no commands were run.
