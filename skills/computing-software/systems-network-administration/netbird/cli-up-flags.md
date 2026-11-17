---
id: computing-software.systems-network-administration.netbird.cli-up-flags
name: cli-up-flags
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, netbird-up, interface-name, wireguard-port, mtu, foreground-mode]
level: practitioner
status: docs-checked
description: "Key netbird up flags: SSH server, inbound and LAN blocking, DNS, firewall, IPv6, interface name, MTU, WireGuard port, foreground mode, profile and browser options."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`netbird up` logs in if needed and connects. `netbird login` authenticates without connecting and accepts `--no-browser` and `--profile`.

Flags worth knowing on `up`:
- `--allow-server-ssh`, `--disable-ssh-auth`, `--ssh-jwt-cache-ttl`: built-in SSH server behaviour.
- `--block-inbound`: refuse inbound connections.
- `--block-lan-access`: block access to local networks when this peer is a router or exit node.
- `--disable-auto-connect`: do not connect automatically when the service starts.
- `--disable-dns`, `--dns-resolver-address`, `--extra-dns-labels`.
- `--disable-firewall`, `--disable-ipv6` (v0.68.0+).
- `--disable-client-routes`, `--disable-server-routes`.
- `--external-ip-map`: map external IPs.
- `-F, --foreground-mode`: run in the foreground.
- `--interface-name`: WireGuard interface, default `wt0`.
- `--mtu`: default 1280.
- `--wireguard-port`: default 51820.
- `-N, --network-monitor`: defaults to true on Windows and macOS, false on Linux and FreeBSD; disable with `--network-monitor=false`.
- `--no-browser`: do not open the browser for SSO login.
- `--profile`: profile to use; the last used profile if omitted.

Boolean flags that default to true need `=false` to turn off; string flags accept an empty string to clear a previous value.

Example: `netbird up --setup-key <KEY> --management-url <URL> --interface-name wt0`.

`netbird down` disconnects and returns the daemon to Idle.

## Checked

2026-11-04: read the CLI page (get-started/cli) in full. Confirmed the flag list, defaults (wt0, 1280, 51820), network-monitor defaults, IPv6 version gate, flag-value syntax and the down/Idle behaviour. Removed the unstated "useful on headless hosts" remark and the generic `--help` advice.

Method: documentation only; no commands were run.
