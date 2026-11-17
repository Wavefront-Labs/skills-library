---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-userspace-implementation-and-config-protocol
name: wireguard-userspace-implementation-and-config-protocol
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wireguard-go, userspace, uapi-socket, get-set-protocol, tun, cross-platform, wireguard-rs]
level: advanced
status: docs-checked
description: "Run WireGuard in userspace with wireguard-go and speak the get/set configuration protocol over its UNIX socket."
sources: ["https://www.wireguard.com/xplatform/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Userspace implementations and the configuration protocol

Where Linux users write `ip link add wg0 type wireguard`, non-Linux users write `wireguard-go wg0`; the cross-platform page says wg(8) configures every implementation the same way. A userspace implementation takes `[-f/--foreground] INTERFACE-NAME`, creates a TUN device, daemonizes, and opens a stream UNIX socket at `/var/run/wireguard/wg0.sock` (or `/run/wireguard/wg0.sock`); on Windows a named pipe `\\.\pipe\WireGuard\wg0`. `wg(8)` finds interfaces by scanning `*.sock` in that directory, so configuration works the same as for the kernel module. The process should exit on SIGINT/SIGTERM, removal of the TUN device, or deletion of the socket file.

The text protocol has two commands, both version 1, each ending with an empty line:

```
get=1
<blank>

set=1
private_key=<hex>
listen_port=51820
replace_peers=true
public_key=<hex>
endpoint=192.0.2.1:51820
replace_allowed_ips=true
allowed_ip=10.0.0.2/32
<blank>
```

Replies end with `errno=0` and a blank line (a nonzero errno on failure). Keys are lowercase hex here, not base64. Other keys: `fwmark`, `preshared_key`, `persistent_keepalive_interval`, `remove=true`, `update_only=true`. An all-zero `private_key` or `preshared_key` removes the key.

Debug output on userspace builds: `export LOG_LEVEL=verbose`.

Verify: `wg show` lists the interface once the userspace process is running.

## Checked

2026-11-03. Confirmed: Invocation, TUN creation, socket paths, Windows named pipe, wg(8) discovery of *.sock, exit conditions, get/set version 1, blank-line framing, errno replies, hex keys, all listed keys, all-zero key removal and LOG_LEVEL=verbose against the cross-platform interface page and the quick start. Removed: the management-tool advice sentence and the ls verify.

Method: documentation only; no commands were run.
