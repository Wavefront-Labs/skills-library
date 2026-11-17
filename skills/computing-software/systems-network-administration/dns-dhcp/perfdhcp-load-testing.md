---
id: computing-software.systems-network-administration.dns-dhcp.perfdhcp-load-testing
name: perfdhcp-load-testing
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp-troubleshooting, perfdhcp, kea, load-testing, capacity, dhcp-performance, relay-simulation]
level: practitioner
status: gated
description: "Load-test DHCP servers with perfdhcp: DORA/SARR rates, simulating many clients and relays, measuring drops and latency, and sizing Kea backends before a mass-reboot event."
sources:
  - https://kea.readthedocs.io/en/latest/man/perfdhcp.8.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# perfdhcp load testing

The worst DHCP day is a power restore or controller reboot when every client asks at once. Measure
capacity before it happens.

## Basics (ships with Kea)
```
perfdhcp -4 -r 500 -R 10000 -p 60 -l 10.0.5.1 10.0.0.11
#  -r 500     500 exchanges (DORA) per second
#  -R 10000   simulate 10,000 distinct clients (MACs); default 1
#  -p 60      run 60 seconds (-n N stops after N transactions instead; both can be given)
#  -l 10.0.5.1  local address to send from (DHCPv4); the last argument is the server
perfdhcp -6 -r 200 -R 5000 -p 30 -l eth1 2001:db8::11
```
These command lines were not executed: perfdhcp ships only with Kea builds that are not available on
this Windows machine, so flag meanings come from the perfdhcp man page and source, and the measured
behaviour of the exact combinations is unconfirmed (gated: unconfirmed, source is paywalled or blocked).

For DHCPv4 `-l` takes a local hostname/address (default: the interface address that routes to the
server); for DHCPv6 it takes the interface name. `-4` is the default. The tool prints a periodic
report (`-t` sets the interval in seconds) and a final one with the exchanges that were not
completed and response latencies; a request with no answer within one second counts as lost.
Increase `-r` until drops appear; that is the practical ceiling for this configuration. `-i` runs
only the two-packet exchange (DO or SA) and `--scenario avalanche` models retransmitting clients
after a stall.

## Simulate relayed traffic
Production DHCP is relayed; test that path:
```
perfdhcp -4 -r 300 -R 20000 -l 10.0.5.1 -b mac=00:0c:01:00:00:00 -o 82,010473773031 10.0.0.11
perfdhcp -6 -r 200 -R 5000 -A 1 -l eth1 2001:db8::11    # relayed DHCPv6 traffic
```
In the Kea source, DHCPv4 packets from perfdhcp always carry `giaddr` set to the local socket address
(the `-l` address) and hops 1, so the server's subnet selection sees a relayed packet from that
address: use an address inside the subnet under test, or one named in the subnet's `relay`
setting. `-b mac=...` sets the base MAC; `-o code,hexstring` adds a raw option (here option 82
carrying circuit-id sub-option 1, length 4, "sw01" = 73 77 30 31); perfdhcp inserts options as
given without checking them. `-A 1` simulates one DHCPv6 relay agent (1 is the only value supported)
and `--or 1:38,<hex>` adds an option to the relay message. `-J file` takes a list of relay addresses
to spread traffic over many subnets or shared networks; for DHCPv4 start Kea with the environment
variable `KEA_TEST_SEND_RESPONSES_TO_SOURCE` set so it replies to the source address. The relayed
examples above are unconfirmed (gated: unconfirmed, source is paywalled or blocked): the option 82 hex and the `-l` source address were not tried
against a running Kea.

## What limits Kea throughput
- Lease backend: the ARM calls memfile the simplest and fastest; MySQL/PostgreSQL depend on database
  latency. In HA the server answering a lease-changing query waits for the partner's acknowledgement
  (and for backups too with `wait-backup-ack`), which adds a round trip.
- Hooks and verbose logging add per-packet work; measure with and without them.
- Multi-threading: `"multi-threading": {"enable-multi-threading": true, "thread-pool-size": 4,
  "packet-queue-size": 64}`. The ARM defaults are enabled, pool size 0 (auto-detect) and queue
  size 64; it has been on by default since the Kea 2.3.5 development release (stable from 2.4).

## Safety
Never run against production servers during business hours: perfdhcp creates real leases that
consume pool addresses. Use a lab copy of the config, or a dedicated test subnet, and clean up
afterwards (`lease4-wipe` with the test subnet's id removes all its leases without DNS updates or
hook calls).

## Verify
- [ ] Measured rate at < 1 % drops exceeds the expected peak (clients x renewal burst / seconds), with
  headroom.
