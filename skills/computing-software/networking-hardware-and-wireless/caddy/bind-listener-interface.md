---
id: computing-software.networking-hardware-and-wireless.caddy.bind-listener-interface
name: bind-listener-interface
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [bind, listener, loopback, unix-socket, interface, caddyfile]
level: practitioner
status: docs-checked
description: "Restrict which interface or Unix socket a Caddy site listens on with the bind directive, including IPv6, socket permissions and the inconsistent-binding trap."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/bind
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop a site listening on every interface, or listen on a Unix socket.

Syntax: `bind <hosts...>`. It takes hosts only, never a port; the port still comes from the site address (default 443). Values are network addresses, so Unix sockets are accepted.

Examples from the page: `bind 127.0.0.1` makes the site reachable only from the machine; `bind 127.0.0.1 [::1]` adds IPv6 loopback; `example.com:8080 { bind 10.0.0.1 }` binds `10.0.0.1:8080`; `bind unix//run/caddy` listens on a Unix domain socket at `/run/caddy`; and `bind unix//run/caddy|0222` sets the socket file permission to 0222 so all users can write (the default is `0200`, owner-only write).

The same hostname can be served differently per interface by repeating the site block: `example.com { bind 10.0.0.1  respond "One" }` and `example.com { bind 10.0.0.2  respond "Two" }`.

The trap: binding sites inconsistently. If two sites on the same port resolve to `127.0.0.1` and only one has `bind 127.0.0.1`, the other binds the wildcard on that port, the operating system prefers the more specific socket, and only one site stays reachable, because virtual hosts are not shared across different listeners. Either bind every site on a port the same way or none of them.

## Checked

2026-11-03: read caddyfile/directives/bind against this skill. Confirmed: bind <hosts...> syntax, no port, unix socket form with |0222, default 0200, per-interface site blocks and the inconsistent-binding trap.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
