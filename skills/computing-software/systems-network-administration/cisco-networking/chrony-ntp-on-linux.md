---
id: computing-software.systems-network-administration.cisco-networking.chrony-ntp-on-linux
name: chrony-ntp-on-linux
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [ntp, chrony, chronyc, linux, time-server, makestep, nts, timekeeping]
level: practitioner
status: docs-checked
description: "Run chrony 4.5 as an NTP client or internal time server on Linux: server and pool, iburst, makestep, rtcsync, allow, local orphan, NTS, and chronyc diagnosis."
sources:
  - https://chrony-project.org/doc/4.5/chrony.conf.html
  - https://chrony-project.org/doc/4.5/chronyc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# chrony on Linux

Network devices often sync to a pair of internal time servers. The config file location differs by distribution (commonly /etc/chrony.conf or /etc/chrony/chrony.conf); check your distribution.

## Client configuration
```
server ntp1.example.net iburst
server ntp2.example.net iburst
pool pool.example.org iburst maxsources 2
makestep 1.0 3
rtcsync
driftfile /var/lib/chrony/drift
```
- `iburst`: chronyd starts with a burst of 4-8 requests to make the first clock update sooner, and repeats the burst when a source goes from offline to online with `online` in chronyc.
- `pool`: same options as `server`, for a name that resolves to multiple addresses that may change over time. `maxsources` sets how many sources to use from the pool: default 4, maximum 16.
- `makestep 1.0 3`: step the system clock if the adjustment is larger than 1.0 seconds, but only in the first 3 clock updates since chronyd started. Normally chronyd slews. The page says that on most systems it is desirable to step only on boot, before programs that rely on time moving monotonically forwards start.
- `rtcsync`: the system time is periodically copied to the RTC and chronyd does not track its drift; cannot be used with `rtcfile`. On Linux the kernel does the copy every 11 minutes.
- The documentation's own examples use `driftfile /var/lib/chrony/drift`, `makestep 1.0 3` and `rtcsync` together.
- Default polling: `minpoll` 6 (64 s), `maxpoll` 10 (1024 s). Intervals under 64 s should generally not be used with public Internet servers, as it might be considered abuse.

## NTS and authentication
- The `nts` option on `server` (or `pool`) enables Network Time Security: no shared key file is needed; NTS-KE uses TLS to obtain keys and cookies. chronyd must be compiled with NTS support.
- The NTS-KE client connects to TCP port 4460 by default (the `ntsport` source option names the port of the server you query, and the `ntsport` directive sets the port chronyd itself serves NTS-KE on, also default 4460). The `key` option is the alternative based on a key file.
- NTP itself uses UDP port 123 by default.
- `nts` and `iburst` do not work in the `peer` directive.

## Serving clients
```
allow 10.0.0.0/8
local stratum 10 orphan
```
- With no `allow`, chronyd is a client only (no clients allowed). With `allow`, it is both a client of its servers and a server for the permitted subnets; `allow` also controls NTS-KE clients when NTS is enabled.
- `local` lets a server appear synchronised to real time even when it never was, for isolated networks. `stratum` range is 1 to 15, default 10, and should be larger than the maximum expected stratum when external servers are reachable. `distance` defaults to 1 second.
- `orphan` makes sources at the local stratum be ignored unless nothing else is selectable and their reference ID is smaller than the local one, so several servers with the same local configuration can sync to each other: each must be configured to poll all the others, and the one with the smallest reference ID wins.
- `port 0` makes chronyd client-only.

## Diagnose
```
chronyc sources -v
chronyc tracking
chronyc sourcestats
chronyc clients
chronyc makestep
```
- `sources` first column M: `^` server, `=` peer, `#` locally connected reference clock. Second column S: `*` best selected source, `+` selected and combined, `-` selectable but not selected, `x` falseticker, `~` too much variability, `?` not selectable (for example unreachable, not synchronised, or not enough measurements). `Reach` is an octal register of the last eight transmissions; 377 means all eight got a valid reply.
- `tracking` shows Reference ID (7F7F0101 with no name means local mode and no external source), Stratum, System time (offset between the NTP clock and the system clock), Root delay, Root dispersion and Leap status (Normal, Insert second, Delete second or Not synchronised). The page gives the error bound `clock_error <= |system_time_offset| + root_dispersion + (0.5 * root_delay)`.
- `clients` lists clients that accessed the server through NTP, command or NTS-KE ports.
- `makestep` with no parameters cancels any remaining slew and jumps the clock immediately; the page warns that certain software is seriously affected by such jumps.

## Not covered by the cited pages
Coexistence with systemd-timesyncd or ntpd, hypervisor time sync, containers, which distributions ship chrony, specific upstream servers, and the firewall rules for a given site.

## Verify
- [ ] `chronyc sources -v` shows `*` on a source with Reach 377.
- [ ] `chronyc tracking` shows Leap status Normal and a small System time offset.
- [ ] On a server, `chronyc clients` lists the devices you expect.

## Checked
Date: 2026-11-08. Pages: chrony 4.5 chrony.conf (137k characters) and chronyc (58k) manuals; searched by directive and read around the hits for server and its options, pool, peer, makestep, rtcsync, allow, local, ports, NTS and example configs; chronyc tracking, makestep, sources, sourcestats and clients sections read in full.
Confirmed: every option and default quoted above, the `^`/`#`/`=` and `*`/`+`/`-`/`x`/`~`/`?` meanings, Reach 377, tracking fields and Leap status values, ports 123 and 4460.
Removed: distribution default claims, named public time servers, the "outbound NTS-KE 4460" firewall statement as a rule, the `local ... orphan` comment as written, stratum and offset thresholds in Verify, timesyncd/ntpd, VM, PHC-on-KVM and container gotchas, and the "Leap status Not synchronised means firewall or DNS" diagnosis (the page defines the status but not that cause).
Method: documentation only; no commands were run.
