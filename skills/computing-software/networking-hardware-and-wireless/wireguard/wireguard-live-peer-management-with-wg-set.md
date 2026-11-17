---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-live-peer-management-with-wg-set
name: wireguard-live-peer-management-with-wg-set
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wg-set, add-peer, remove-peer, allowed-ips-incremental, listen-port, fwmark, runtime-reconfiguration]
level: practitioner
status: docs-checked
description: "Add, change and remove peers and allowed IPs on a running WireGuard interface with wg set, including incremental +/- edits."
sources: ["https://man7.org/linux/man-pages/man8/wg.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Live peer management with wg set

`wg set <interface>` changes a running interface without a restart. Syntax:

```
wg set wg0 [listen-port N] [fwmark N] [private-key FILE]
   peer PUBKEY [remove] [preshared-key FILE] [endpoint IP:PORT]
        [persistent-keepalive SECONDS] [allowed-ips [+|-]CIDR[,...]]
```

Examples:

```bash
wg set wg0 peer PUBKEY allowed-ips 10.0.0.2/32 endpoint 198.51.100.7:51820
wg set wg0 peer PUBKEY allowed-ips +10.0.5.0/24      # add one prefix
wg set wg0 peer PUBKEY allowed-ips -10.0.5.0/24      # remove one prefix
wg set wg0 peer PUBKEY allowed-ips ""                # remove all allowed IPs
wg set wg0 peer PUBKEY remove                        # delete the peer
wg set wg0 peer PUBKEY persistent-keepalive 25
wg set wg0 listen-port 0                             # port chosen randomly when the interface comes up
```

Rules to remember: without `+` or `-`, `allowed-ips` replaces the whole list. Several peers can be named in one command. `listen-port` unset or `0` means random. `fwmark` and `persistent-keepalive` accept `0` or `off` to disable. `private-key` and `preshared-key` take file paths (an empty file such as `/dev/null` clears the key).

Changes made with `wg set` are runtime only. Persist them with `wg-quick save wg0` or by editing the config file (if `SaveConfig = true`, wg-quick rewrites the file from interface state at shutdown, overwriting hand edits).

Verify: `wg show wg0 allowed-ips` lists each peer's allowed IPs.

## Checked

2026-11-03. Confirmed: wg set syntax, remove, endpoint, persistent-keepalive (0 or off disables), incremental +/- allowed-ips, empty string clearing allowed IPs, listen-port random when unset or 0, fwmark 0 or off, file-path keys with /dev/null removal, and wg-quick save, against the wg(8) and wg-quick(8) man pages. Removed: the 'next bring-up' wording for listen-port 0 and the 'runtime only' claim is kept only as the wg-quick save pointer.

Method: documentation only; no commands were run.
