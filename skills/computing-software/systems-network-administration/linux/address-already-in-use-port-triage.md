---
id: computing-software.systems-network-administration.linux.address-already-in-use-port-triage
name: address-already-in-use-port-triage
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, port-in-use, address-already-in-use, eaddrinuse, ss-tulpn, so-reuseaddr, systemd-socket-activation]
level: practitioner
status: docs-checked
description: "Triage bind: Address already in use errors: find the owning process with ss or lsof, socket-activated units, TIME_WAIT and SO_REUSEADDR, IPv4/IPv6 dual-stack, and containers."
sources:
  - https://man7.org/linux/man-pages/man8/ss.8.html
  - https://man7.org/linux/man-pages/man7/socket.7.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Address already in use triage

```
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
OSError: [Errno 98] Address already in use
```

## 1. Who holds it
```bash
ss -tulpn 'sport = :80'            # TCP/UDP listeners on port 80 with process (root for other users' PIDs)
ss -tlpn | grep ':8080'
lsof -nP -iTCP:80 -sTCP:LISTEN
fuser -v 80/tcp
```
No process shown but bound? It's kernel-owned or in another network namespace:
- systemd socket activation: `systemctl list-sockets | grep 80` - the **`.socket`** unit owns the port, not a process.
- Containers: list published ports with `docker ps` or `podman ps`; the listener may be a container-runtime helper process.
- `ip netns` and `nsenter -t <pid> -n ss -tlpn` for other namespaces.

## 2. Common situations
| Situation | Fix |
|---|---|
| Old instance still running (failed restart, double start) | `systemctl status app`; kill stray PID; fix the unit so it doesn't fork twice |
| Port owned by a `.socket` unit | `systemctl stop x.socket && systemctl disable x.socket`, or let the service use socket activation |
| App restarts quickly and fails in TIME_WAIT | set `SO_REUSEADDR` in the app (most servers do); TIME_WAIT on a listener's address is normally fine with it |
| Two processes want the same port by design | `SO_REUSEPORT` (both must set it, same user) for load-spreading |
| IPv6 socket already covers IPv4 | binding `[::]:80` with `bindv6only=0` also takes `0.0.0.0:80`; bind one or set `ipv6only=on` (nginx `listen [::]:80 ipv6only=on`) |
| Ephemeral port collision | the port is in `ip_local_port_range` and an outbound connection took it; reserve with `net.ipv4.ip_local_reserved_ports = 8080,9000-9100` |
| Container `-p 80:80` fails | host service already on 80 (`ss` shows it), or a stale proxy process left behind after a crash |

## 3. TIME_WAIT reality check
```bash
ss -tan state time-wait | wc -l
```
TIME_WAIT sockets don't block a new **listen** when `SO_REUSEADDR` is set; they matter for outbound connection exhaustion. `tcp_tw_recycle` is gone from current kernels (tcp(7): Linux 2.4 to 4.11); `tcp_tw_reuse` affects outbound connections only, so read its entry in the kernel ip-sysctl documentation before changing it.

## 4. Privileged ports
`Permission denied` (not "in use") below 1024: grant `CAP_NET_BIND_SERVICE` (`AmbientCapabilities=` in the unit) or lower `net.ipv4.ip_unprivileged_port_start`.

## Verify
- [ ] `ss -tlpn 'sport = :80'` shows exactly the intended process after restart.
- [ ] Service survives `systemctl restart` repeatedly without bind errors.

## Checked

2026-10-28

Confirmed: ss(8) (sport filter syntax), socket.7 (SO_REUSEPORT needs the option on every socket and the same effective UID), ipv6.7 and ip-sysctl (bindv6only), systemd.socket (list-sockets, socket-owned ports, BindIPv6Only), nginx listen ipv6only, ip-sysctl (ip_local_port_range, ip_local_reserved_ports, ip_unprivileged_port_start, tcp_tw_reuse), tcp(7) (tcp_tw_recycle removed), capabilities(7) (CAP_NET_BIND_SERVICE), lsof and fuser manuals.

Removed or corrected: The socket-unit examples, the rootlessport/pasta and docker-proxy claims, the rpc.statd port-pinning remark, and the blanket tcp_tw_reuse=1 advice.

Method: documentation only; no commands were run.
