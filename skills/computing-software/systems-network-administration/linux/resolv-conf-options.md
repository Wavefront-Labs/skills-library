---
id: computing-software.systems-network-administration.linux.resolv-conf-options
name: resolv-conf-options
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, resolv-conf, resolv-conf-options, ndots, edns0, single-request-reopen, dns-timeout, kubernetes-dns]
level: practitioner
status: docs-checked
description: "Tune glibc resolver behaviour in resolv.conf: nameserver limits, search and ndots, timeout/attempts/rotate, edns0, single-request(-reopen), trust-ad, and who overwrites the file."
sources:
  - https://man7.org/linux/man-pages/man5/resolv.conf.5.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-resolved.service.html
  - https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# resolv.conf options

## Who owns the file?
`ls -l /etc/resolv.conf` — symlink to `/run/systemd/resolve/stub-resolv.conf` (resolved stub 127.0.0.53),
`/run/NetworkManager/resolv.conf`, or a plain file. Edits to generated files are overwritten; configure the owner
(nmcli `ipv4.dns-options`, netplan, resolved.conf, dhclient) instead.

## Directives
```
nameserver 10.0.0.53          # max 3 used (MAXNS)
nameserver 10.0.1.53
search corp.example.com example.com   # glibc 2.25 and earlier: max 6 domains, 256 characters; no limit since 2.26
options timeout:2 attempts:2 rotate edns0 ndots:1
```
| Option | Effect |
|---|---|
| `timeout:N` | seconds per query attempt (default 5, capped at 30) — 5 s stalls on a dead first server are this |
| `attempts:N` | how many times the resolver sends a query to its name servers before giving up (default 2, capped at 5) |
| `rotate` | round-robin between servers instead of always the first |
| `ndots:N` | names with fewer than N dots try search domains first (default 1, capped at 15; Kubernetes pods default to 5 → many extra lookups) |
| `edns0` | enables the EDNS0 DNS extensions (RFC 2671) |
| `single-request` / `single-request-reopen` | single-request sends the IPv4 and IPv6 lookups sequentially (for DNS servers that mishandle parallel queries); -reopen closes and reopens the socket before the second request when a server returns only one reply |
| `trust-ad` (glibc 2.31+) | keep the AD bit in answers; safe only if the local system trusts the validating resolver and the path to it |
| `no-aaaa` (glibc 2.36+) | suppress AAAA queries |

Per-process override: `RES_OPTIONS="timeout:1 attempts:1" cmd`, `LOCALDOMAIN="corp.example.com"`.

## Diagnose
`getent ahosts name` (uses resolv.conf/nsswitch like apps) vs `dig name` (bypasses search and nsswitch);
`strace -e trace=network -f getent hosts name` to watch query order.

## Verify
- [ ] Resolution latency `time getent hosts name` is low; options persist across reboot/DHCP renewal.

## Checked
2026-10-27. Checked against man7.org resolv.conf(5) (man-pages 6.19, page dated 2026-08-22), the Kubernetes DNS for Services and Pods page and glibc NEWS. Confirmed: MAXNS is 3; search list limits and the glibc 2.26 change; timeout default 5 capped at 30; attempts default 2 capped at 5; ndots default 1 capped at 15; rotate, edns0, single-request, single-request-reopen, trust-ad (glibc 2.31), no-aaaa (glibc 2.36); RES_OPTIONS and LOCALDOMAIN; Kubernetes pods get ndots:5. The description of single-request-reopen and edns0 was rewritten to the manual wording.

Method: documentation only; no commands were run.
