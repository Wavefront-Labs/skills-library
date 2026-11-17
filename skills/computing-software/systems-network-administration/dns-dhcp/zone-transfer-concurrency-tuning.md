---
id: computing-software.systems-network-administration.dns-dhcp.zone-transfer-concurrency-tuning
name: zone-transfer-concurrency-tuning
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, transfers-in, transfers-out, transfers-per-ns, bind, zone-transfers]
level: practitioner
status: docs-checked
description: "Tune BIND zone transfer concurrency (transfers-in, transfers-out, transfers-per-ns, serial-query-rate) for servers with thousands of zones."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-transfers-in
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-serial-query-rate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer concurrency tuning

Defaults suit a handful of zones. With thousands (hosting, catalog zones), secondaries take hours
to catch up after a restart or a bulk change.

## Settings
```
options {
    transfers-in 50;          // default 10: concurrent inbound transfers on a secondary
    transfers-per-ns 10;      // default 2: concurrent inbound transfers from one primary
    transfers-out 50;         // default 10: concurrent outbound; requests over the limit are refused
    serial-query-rate 100;    // default 20: SOA refresh queries per second
    notify-rate 100;          // default 20: NOTIFYs per second
    startup-notify-rate 50;
    max-transfer-time-in 120; // minutes (default 120)
    max-transfer-idle-in 60;  // minutes (default 60)
};
```
Per primary: `server 192.0.2.53 { transfers 20; };` overrides transfers-per-ns.

## Signs of a bottleneck
- Secondary SOA serials lagging behind the primary for minutes after changes, or many zones refreshing at once after a restart.
- Transfer requests refused on the primary because `transfers-out` is exceeded.

## Sizing
Rough estimate: total transfer time = zones x average transfer time / concurrency. IXFR keeps per-change transfers small, so concurrency mostly matters after restarts and new-zone bursts. The ARM notes that raising `transfers-in` or `transfers-per-ns` speeds convergence but increases load on the local or remote server.

## Primary side
Raise `transfers-out` to cover the number of secondaries times their `transfers-per-ns`; excess requests are refused, not queued. Watch CPU and bandwidth during bursts.

## Verify
- [ ] After a bulk change, all secondaries reach the new serial within the target window with no refused transfers.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27; grammar cross-checked on bind-9.20), read on 2026-10-26. Confirmed: defaults transfers-in 10, transfers-out 10 (excess refused), transfers-per-ns 2 with per-server `transfers` override, serial-query-rate 20/s, notify-rate 20/s, startup-notify-rate 20/s, max-transfer-time-in 120, max-transfer-idle-in 60. Removed unconfirmed log and rndc status strings and the worked timing example.

Method: documentation only; no commands were run.
