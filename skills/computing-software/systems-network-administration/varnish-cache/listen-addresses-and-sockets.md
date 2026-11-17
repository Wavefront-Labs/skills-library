---
id: computing-software.systems-network-administration.varnish-cache.listen-addresses-and-sockets
name: listen-addresses-and-sockets
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [listen-address, unix-socket, proxy-protocol, varnishd-a]
level: practitioner
status: docs-checked
description: "Configure varnishd -a listeners: named endpoints, IPv4/IPv6 and port ranges, Unix domain sockets with user/group/mode, and the HTTP, PROXY and HTTPS protocols."
sources:
  - https://www.varnish.org/docs/reference/varnishd/
  - https://www.varnish.org/docs/users-guide/command-line/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# listen addresses and sockets

`-a [name=]address[,PROTO|,option=value]`; repeat `-a` for several endpoints. With no `-a` the default is `:80` on all IPv4 and IPv6 interfaces.

- `name` appears in logs and is `local.socket` in VCL; unnamed listeners are `a0`, `a1`, ...
- `PROTO` is `HTTP` (default), `PROXY` (versions 1 and 2) or `HTTPS`.
- Address forms: host name, IPv4, IPv6 in brackets; port number, service name or inclusive non-overlapping range `80-81`.
- Unix domain socket (VCL 4.1 and higher): absolute path, or `@name` for an abstract socket. Options `user=`, `group=`, `mode=` (3-digit octal) do not apply to abstract sockets.

```
-a http=:80
-a localhost:80,HTTP
-a '[fe80::1]:80'
-a '0.0.0.0:8080,[::]:8081'
-a uds=/path/to/listen.sock,PROXY,mode=666
-a @abstract_socket
-a :443,https
```

`-b` can also be a Unix socket path (begins with `/`), VCL 4.1 or later only. `std.port(server.ip)` returns 0 for Unix socket addresses.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the generic Verify tip.

Method: documentation only; no commands were run.
