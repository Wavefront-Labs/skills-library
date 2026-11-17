---
id: computing-software.systems-network-administration.linux.time-sync-with-chrony
name: time-sync-with-chrony
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, chrony, chronyd, chronyc, ntp, time-sync, timesync, systemd-timesyncd, ntp-server, nts, clock-drift, makestep, hwclock, rtc, leap-second, pps, timedatectl, rhcsa, networking, sysadmin, chrony-conf, chrony-allow]
level: practitioner
status: docs-checked
description: "Keep Linux clocks correct with chrony: client config, serving time to a LAN, NTS, step vs slew, and reading chronyc tracking and sources to prove it is synchronised."
sources:
  - https://github.com/mlichvar/chrony/blob/master/doc/chrony.conf.adoc
  - https://github.com/mlichvar/chrony/blob/master/doc/chronyc.adoc
  - https://github.com/mlichvar/chrony/blob/master/doc/chronyd.adoc
  - https://github.com/mlichvar/chrony/blob/master/doc/faq.adoc
  - https://github.com/systemd/systemd/blob/main/man/timedatectl.xml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Time synchronisation with chrony — because Kerberos, TLS and logs all assume it

**Goal:** every host within milliseconds of a trusted source, surviving reboots,
suspend, and bad upstreams, with an internal NTP tier for isolated networks.

## 1. Client
```bash
dnf install chrony    # or your distribution's package manager
```
`chrony.conf` (its location depends on the distribution, for example `/etc/chrony.conf`):
```
pool 2.pool.ntp.org iburst maxsources 4     # or your internal servers:
server ntp1.corp.example iburst nts          # nts = authenticated NTP (needs a cert on the server)
server ntp2.corp.example iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3                               # step the clock if off by >1 s, first 3 updates only
rtcsync                                      # kernel copies system time to the RTC every 11 min (Linux)
leapsectz right/UTC                          # leap seconds taken from the right/UTC time zone in tzdata
logdir /var/log/chrony
```
```bash
systemctl enable --now chronyd
chronyc tracking            # Leap status: Normal; System time offset; Stratum
chronyc sources -v          # ^* = currently synced source, ^+ combined, ^? unreachable, ^x false ticker
chronyc sourcestats
chronyc makestep            # force an immediate step (after VM restore, long suspend)
timedatectl                 # "System clock synchronized: yes", "NTP service: active"
```
- `iburst` starts with a burst of 4-8 requests so the first clock update comes sooner.
- `makestep 1.0 3` is the boot-time rescue; after that chrony slews so time never jumps
  backwards (databases and Kerberos hate jumps). `makestep 1 -1` = always step (appliances only).
- Cloud: use your provider's documented time source (the provider documentation was not checked here).
- Run only one time daemon.
  Containers don't run chrony — they inherit the host clock.

## 2. Serving time to a LAN
```
# on ntp1.corp.example, in addition to upstream servers:
allow 10.0.0.0/8
local stratum 10              # keep serving (as a fallback) if upstream dies — isolated networks only
ntsdumpdir /var/lib/chrony
ntsservercert /etc/pki/tls/certs/ntp1.crt
ntsserverkey  /etc/pki/tls/private/ntp1.key   # NTS-KE service, default port 4460
```
Open 123/udp for NTP and 4460/tcp for NTS-KE. Two or more
internal servers peering (`peer ntp2.corp.example`) stops the LAN losing time when one dies.
For reliable operation a client should have at least three servers (chrony FAQ).

## 3. Hardware clock and time zones
```bash
hwclock --show; hwclock --systohc           # RTC; chrony's rtcsync does this automatically
timedatectl set-timezone Europe/London      # the system clock is always UTC; TZ is a display setting
timedatectl set-local-rtc 0                 # RTC in UTC (1 only for Windows dual-boot)
timedatectl set-ntp true                    # enables chronyd (or timesyncd) via systemd
```

## 4. Troubleshooting
| `chronyc` says | Meaning / fix |
|---|---|
| `Leap status : Not synchronised` | no reachable source: `chronyc sources` shows `^?`; firewall 123/udp, DNS, or `allow` on server |
| `^x` on a source | false ticker — disagrees with the majority; remove it |
| offset keeps growing | check `chronyc tracking` (Frequency, Skew) and `sourcestats`; a VM may need a host or PTP source |
| `chronyc` cannot reach `chronyd` | check privileges and, for remote use, `cmdallow` |
| clock far off after resume or restore | `makestep` only steps within its first updates; use `chronyc makestep` |

`chronyc -N authdata` shows NTS state; `chronyd -q 'server pool.ntp.org iburst'` is a
one-shot set-and-exit (like old `ntpdate`).

## Verify
- [ ] `chronyc tracking` shows `Leap status: Normal` and a small System time offset.
- [ ] `chronyc sources` shows one `^*` and ≥2 other `^+` sources reachable (`Reach 377`).
- [ ] After reboot, `timedatectl` reports `System clock synchronized: yes` once chronyd has a source.

## Checked

2026-10-26. chrony repository (mlichvar/chrony, docs on master, 2026-10): makestep threshold and limit semantics, rtcsync 11 minute kernel copy on Linux, leapsectz right/UTC, nts option and NTS-KE default port 4460, ntsservercert and ntsserverkey, local, allow, peer, cmdallow, maxsources; chronyc sources legend (^*, ^+, ^?, ^x), Reach 377, tracking Leap status; chronyd -q one-shot mode; FAQ advice on at least three servers. timedatectl(1): set-ntp, set-timezone, set-local-rtc. Removed provider-specific time servers, the 500 ppm and 5 minute Kerberos figures, firewall-cmd, the systemd-sleep hook, threshold figures and the set-time remark, which were not confirmed. The pool.ntp.org host names are examples.

Method: documentation only; no commands were run.
