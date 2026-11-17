---
id: computing-software.systems-network-administration.pi-hole.pihole-command-cheatsheet
name: pihole-command-cheatsheet
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-command, pihole-cli, wrapper-script]
level: intro
status: docs-checked
description: "Find the right pihole subcommand for allowlists, gravity, logs, status, passwords, updates and reloads."
sources: ["https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The pihole command at a glance

`pihole` (script at `/usr/local/bin/pihole`) is a wrapper used by both the CLI and the web interface. It elevates the caller with `sudo` but only for what the wrapper exposes. Run `pihole --help` for usage.

| Task | Command |
| --- | --- |
| Allow or deny domains | `pihole allow`, `pihole deny` |
| Regex entries | `pihole --regex`, `--wild`, `--allow-regex`, `--allow-wild` |
| Rebuild blocklists | `pihole updateGravity` (`pihole -g`) |
| Query lists for a domain | `pihole query` (`pihole -q`) |
| Status | `pihole status` |
| Pause blocking | `pihole disable 5m`, `pihole enable` |
| Live log | `pihole tail` |
| Empty the log | `pihole flush` |
| Log on/off | `pihole logging off` |
| Diagnose | `pihole debug` |
| Set web password | `pihole setpassword` |
| Reload lists only | `pihole reloadlists` |
| Flush and reload DNS cache | `pihole reloaddns` |
| Clear network table | `pihole networkflush [--arp]` |
| Update | `pihole updatePihole` (`pihole -up`) |
| Versions | `pihole version` (`pihole -v`) |
| Repair | `pihole repair` |
| Switch branches | `pihole checkout` |
| Remove | `pihole uninstall` |

`reloadlists` and `reloaddns` do not re-read `*.conf` files. The page lists `--help` for `pihole allow`, `deny`, the regex options, `logging`, `query`, `disable`, `enable` and `checkout`; most other subcommands show no help command.

## Checked

2026-11-03. Read The pihole Command page: every row of the table (including the `-g`, `-q`, `-up`, `-v` short forms), the wrapper location `/usr/local/bin/pihole`, the sudo elevation description and the `reloadlists` and `reloaddns` notes. Narrowed the `--help` sentence to the subcommands the page lists a help command for.

Method: documentation only; no commands were run.
