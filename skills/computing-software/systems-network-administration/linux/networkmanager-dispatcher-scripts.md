---
id: computing-software.systems-network-administration.linux.networkmanager-dispatcher-scripts
name: networkmanager-dispatcher-scripts
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, networkmanager, nm-dispatcher, dispatcher-scripts, network-events, hooks, pre-up, pre-down, connectivity-change, networking, sysadmin, automation]
level: practitioner
status: docs-checked
description: "Run scripts when NetworkManager brings links up or down: dispatcher directories, event names, environment variables, pre-up/pre-down blocking hooks, permissions and debugging."
sources:
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/NetworkManager-dispatcher.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/NetworkManager.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/src/libnmc-setting/settings-docs.h.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetworkManager dispatcher scripts

**Goal:** react to network state changes (add a policy route when a VPN comes up, mount a
share on the office LAN, restart a daemon that binds an address) without polling.

## 1. Where and how scripts run
- `/etc/NetworkManager/dispatcher.d/` and `/usr/lib/NetworkManager/dispatcher.d/` (and subdirectories) — scripts run in alphabetical order in response to network events by the D-Bus activated `NetworkManager-dispatcher` service; a file in `/etc` takes precedence over an identically named one in `/usr/lib`.
- `dispatcher.d/pre-up.d/` and `pre-down.d/` — for the `pre-up`, `pre-down` (and VPN equivalents) events; NetworkManager waits for these scripts to finish before continuing. `pre-down` is not emitted for forced disconnections such as carrier loss.
- `dispatcher.d/no-wait.d/` — scripts run immediately and in parallel, without waiting for earlier scripts. Once queued, a script always runs, even if a later event makes it obsolete.
- Requirements: a regular executable file owned by root, not writable by group or other, and not setuid.

## 2. Arguments and environment
`$1` = interface name (`none` for the `hostname` action, empty for `connectivity-change` and `dns-change`), `$2` = action:
`up`, `down`, `pre-up`, `pre-down`, `vpn-pre-up`, `vpn-up`, `vpn-pre-down`, `vpn-down`, `hostname`, `dhcp4-change`,
`dhcp6-change`, `connectivity-change`, `reapply`, `dns-change` (plus `device-add`/`device-delete` for generic connections).
Useful variables: `NM_DISPATCHER_ACTION` (since 1.12.0), `CONNECTION_ID`, `CONNECTION_UUID`, `CONNECTION_FILENAME`, `DEVICE_IFACE`, `DEVICE_IP_IFACE`, `IP4_ADDRESS_N`, `IP4_NUM_ADDRESSES`,
`IP4_GATEWAY`, `IP4_NAMESERVERS`, `DHCP4_*` options, `VPN_IP_IFACE`, `CONNECTIVITY_STATE`.

## 3. Example: policy route when a specific profile comes up
```bash
#!/bin/bash
# /etc/NetworkManager/dispatcher.d/50-backup-route
[ "$CONNECTION_ID" = "backup-net" ] || exit 0
case "$2" in
  up)   ip route replace 10.99.0.0/16 via 192.168.77.1 dev "$1" table 100
        ip rule add from 192.168.77.0/24 table 100 priority 1000 2>/dev/null || true ;;
  down) ip rule del from 192.168.77.0/24 table 100 2>/dev/null || true ;;
esac
logger -t nm-dispatch "backup-net $2 on $1"
```
For static routes and rules, prefer the profile itself (`ipv4.routes` takes `ip[/prefix] [next-hop] [metric] [attribute=val]`, for example `nmcli con mod backup-net +ipv4.routes "10.99.0.0/16 192.168.77.1 table=100"`; policy rules belong in `ipv4.routing-rules`, see nm-settings-nmcli for its syntax);
use a dispatcher only for actions NM cannot express.

## 4. Debugging
```bash
journalctl -u NetworkManager-dispatcher -f       # script start/exit status, timeouts
nmcli con down backup-net; nmcli con up backup-net   # trigger the events
```
To see what NM passes, write a throwaway script that dumps its arguments and environment to a file.

## Gotchas
- Scripts outside `no-wait.d` run one after another, so a slow script delays the others; put slow work in `no-wait.d`.
- Output on stdout is captured by the dispatcher only for `device-add`/`device-delete` handlers; use stderr for debug messages that should reach the journal there.
- `up` fires per device *and* `vpn-up` per VPN — filter on `CONNECTION_ID` or `$1` or the script runs too often.

## Verify
- [ ] `ls -l` shows the script owned by root, not group/other-writable and executable; `journalctl -u NetworkManager-dispatcher` shows it ran after a `con up`.
- [ ] The effect (route, mount, service restart) is present after `up` and removed after `down`.

## Checked
Checked 2026-10-25 against the NetworkManager source tree on GitHub (NetworkManager/NetworkManager main, last commit 2026-10-23): script directories and `/etc` over `/usr/lib` precedence, ownership and permission requirements, `pre-up.d`/`pre-down.d`/`no-wait.d` semantics, argument and action list, environment variables listed above, `device-add` stdout handling, `ip4.routes` and `ipv4.routing-rules` property names and the `table=` route attribute (via settings docs). Removed unconfirmed claims: the ~60 second kill timeout, minimal-environment/PATH statement, `systemd-run` advice, networkd-dispatcher note and the routing-rules command-line grammar (not shown in the docs read; verify against nm-settings-nmcli before use).

Method: documentation only; no commands were run.
