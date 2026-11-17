---
id: computing-software.systems-network-administration.pi-hole.ntp-server-and-time-sync
name: ntp-server-and-time-sync
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-ntp, ntp-sync, rtc-update]
level: advanced
status: docs-checked
description: "Run Pi-hole's built-in NTP server and sync the system clock to an upstream NTP server, optionally updating an RTC."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NTP server and time sync in FTL

FTL can both serve and consume time.

**Serve NTP** (default enabled for both):

- `ntp.ipv4.active` / `ntp.ipv6.active`: act as an NTP server.
- `ntp.ipv4.address` / `ntp.ipv6.address`: address to listen on; empty means the wildcard (`0.0.0.0` or `::`).

**Sync the system clock** (`[ntp.sync]`):

| Option | Default | Meaning |
| --- | --- | --- |
| `active` | `true` | Try to synchronise system time with an upstream NTP server |
| `server` | `pool.ntp.org` | Upstream; choose one close to you to minimise offset from routing paths |
| `interval` | `3600` | Seconds between attempts |
| `count` | `8` | Syncs performed and averaged before the time is updated |

**Real-time clock** (`[ntp.sync.rtc]`):

- `set` (default `false`): update the RTC if available.
- `device`: path such as `/dev/rtc0`, or empty to auto-discover.
- `utc` (default `true`): set the RTC to UTC.

In Docker, the example compose file has a commented-out `123:123/udp` port mapping and lists the `SYS_TIME` capability, which the Docker configuration page says FTL needs to set the system time via NTP.

**Checklist**

1. Decide whether Pi-hole should be the network's NTP server.
2. Pick a nearby upstream.

## Checked

2026-11-03. Read the `[ntp.ipv4]`, `[ntp.ipv6]`, `[ntp.sync]` and `[ntp.sync.rtc]` sections of the FTL configuration reference (all defaults and meanings), the Docker configuration page (`CAP_SYS_TIME`) and the Docker quick start (`123:123/udp` commented out, `SYS_TIME`). Reworded the Docker sentence to what those pages show; removed the RTC board advice.

Method: documentation only; no commands were run.
