---
id: computing-software.networking-hardware-and-wireless.strongswan.swanctl-load-commands
name: swanctl-load-commands
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, swanctl, load-all, load-creds, load-conns, vici]
level: intro
status: docs-checked
description: "Load and reload strongSwan configuration with swanctl --load-all, --load-creds, --load-conns, --load-pools and --load-authorities, including --clear, --noprompt and --file."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctl.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlLoadAll.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlLoadCreds.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlLoadConns.html
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlLoadPools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# swanctl load commands
`swanctl` configures, controls and monitors the charon daemon through the vici interface plugin. It reads `swanctl.conf` and the credential directories and pushes them to the daemon.

| Command | Short | Loads |
|---|---|---|
| `--load-creds` | `-s` | private keys, public keys, X.509 certificates, pre-shared secrets |
| `--load-conns` | `-c` | connection configurations |
| `--load-pools` | `-a` | IPv4 and/or IPv6 address pools |
| `--load-authorities` | `-b` | certification authority information |
| `--load-all` | `-q` | all four in one command |

Options on `--load-all` and `--load-creds`: `--clear` (`-c`) clears previously loaded credentials, `--noprompt` (`-n`) does not prompt for passwords, `--file` (`-f`) uses a custom path to swanctl.conf. `--load-conns` and `--load-pools` take `--file` only.

Global options: `--debug` (`-v`, default 1), `--options` (`-+`, read options from a file), `--uri` (`-u`, service URI to connect to); most commands also accept `--raw` and `--pretty`. Since 6.0.5 the short option for `--version` is `-V` and for `--uninstall` is `-U` (per the page).

Typical output reports `loaded connection 'home'` and `successfully loaded 1 connections, 0 unloaded`.

## Checked
2026-11-04. Confirmed against the swanctl, --load-all, --load-creds, --load-conns and --load-pools pages: command table with short options, per-command options, global options, the 6.0.5 short-option change and the sample output. Removed the claim that reloading shows removed connections as unloaded (not on the pages). The --load-authorities page was not fetched; its short option and purpose come from the swanctl page.

Method: documentation only; no commands were run.
