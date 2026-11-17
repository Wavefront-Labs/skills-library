---
id: computing-software.networking-hardware-and-wireless.haproxy.runtime-api-stats-socket
name: runtime-api-stats-socket
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, runtime-api, stats-socket, socat, show-info, show-stat, admin-level]
level: practitioner
status: docs-checked
description: "Enable the HAProxy runtime API with stats socket, set its level and mode, and query it with socat for info, stat, servers, errors and pools."
sources:
  - https://docs.haproxy.org/3.0/management.html
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runtime api stats socket
The stats socket is not enabled by default. Enable it in `global`:

```
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats timeout 2m
```
`stats socket [<address:port>|<path>] [param*]` binds a UNIX socket or a TCPv4/v6 address and accepts all `bind` parameters. The default socket timeout is 10 seconds; `stats timeout` changes it (milliseconds, or with a unit suffix). Repeat the line for more sockets. A TCP socket is allowed but the management guide calls it dangerous and never done by default.

- `level <level>` restricts what commands the socket accepts: `user` is least privileged (only non-sensitive stats, no changes); `operator` is the default (all data readable, only non-sensitive changes such as clearing max counters); `admin` permits everything and should be used with care. A CLI session can lower its own level with the `operator` or `user` commands but never raise it; `show cli level` reports it.
- `mode <mode>` sets the octal permissions of a UNIX socket (ignored on non-UNIX sockets and some platforms).
- `expose-fd listeners` lets the stats socket pass listener file descriptors to another HAProxy process; it is not required in master-worker mode.
- With `-S <bind>` in master-worker mode HAProxy binds a master CLI; the management guide recommends binding it locally. Worker commands can be prefixed, as in `echo "@1 show ssl cert" | socat /var/run/haproxy.master -`.

Access needs an external tool such as `socat`:
```
socat /var/run/haproxy.sock stdio
socat /var/run/haproxy.sock readline
echo "show info;show stat;show table" | socat /var/run/haproxy.sock stdio
```
- Non-interactive mode is the default: one line is processed, replies are sent and the connection closes. Several commands on one line are separated by `;`; a literal semicolon or backslash in a value needs a preceding backslash. An empty line marks the end of each command's output.
- `prompt` on the first line toggles interactive mode (a `> ` prompt, connection stays open); `prompt timed` also shows uptime. Sending `prompt` again leaves the mode.
- A payload for a command starts after a first line ending in `<<` and ends with an empty line (or a custom end pattern of at most 7 characters set after `<<`). The whole buffer must fit within `tune.bfsize`.
- If several HAProxy processes share a socket, any process may answer and will output its own stats.
- Commands: `help [<command>]` lists keywords; `show info [typed|json] [desc] [float]` (name:value lines by default); `show stat` (CSV by default; `typed` or `json` optional, and `<iid> <type> <sid>` filters with type 1 frontends, 2 backends, 4 servers, ORable); `show servers state [<backend>]`; `show errors [<iid>|<proxy>] [request|response]` (operator or admin levels only); `show sess`; `show activity`; `show pools [byname|bysize|byusage]`; `set maxconn global <n>` (0 restores the initial value); `set maxconn server <backend/server> <n>`; `set rate-limit connections global <n>` (0 disables); `set server <backend>/<server> state [ready|drain|maint]` and `weight <weight>[%]`; `disable server` and `enable server <backend>/<server>`.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 management guide (section 9.3 intro, the `help`, `prompt`, `operator`/`user`, `set maxconn`, `set rate-limit connections`, `set server`, `show info`, `show stat`, `show servers state`, `show errors`, `show pools` entries, and the master CLI `@1` examples) and the configuration manual (`stats socket`, `stats timeout`, bind `level`, `mode`, `expose-fd listeners`). Removed: the claim that `operator` can enable and disable servers, the "no authentication" statement, the `show sess`/`show activity` behaviour descriptions beyond naming them, the reload-recreates-socket gotcha, and the `cut`/`head` verify lines. Only the cited sections of the management guide were read, not the whole document.
Method: documentation only; no commands were run.
