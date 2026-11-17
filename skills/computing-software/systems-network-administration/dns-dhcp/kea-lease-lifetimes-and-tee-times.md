---
id: computing-software.systems-network-administration.dns-dhcp.kea-lease-lifetimes-and-tee-times
name: kea-lease-lifetimes-and-tee-times
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [kea, kea-dhcp4, valid-lifetime, calculate-tee-times, renew-timer, lease-time-design, cache-threshold]
level: practitioner
status: verified
description: "Choose DHCP lease times per network type and set them in Kea: valid/min/max-lifetime, renew and rebind timers or calculate-tee-times, lease caching, and the effect on pool sizing."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#sending-t1-option-58-and-t2-option-59
  - https://www.rfc-editor.org/rfc/rfc2131#section-4.4.5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea lease lifetimes and T1/T2

## Picking lifetimes
Kea's own default `valid-lifetime` is 4000 s. The table below is practitioner judgement, not
Kea documentation: starting points to adjust from measured churn.

| Network | Typical lease | Why |
|---|---|---|
| Guest Wi-Fi, events, cafés | 30 min - 2 h | high churn; short leases free addresses fast |
| Corporate Wi-Fi | 4 - 8 h | roaming users come and go daily |
| Wired desktops | 1 - 8 days | stable; fewer renewals |
| Servers/infrastructure via DHCP | reservations, long leases | stability |
| VoIP phones | 1 day+ | avoid churn; phones re-register on change |
Short leases mean more DHCP traffic and a harder dependency on the server; during a DHCP outage,
clients lose addresses after the lease expires. Long leases make pools fill with departed clients.

## Kea settings
```json
"valid-lifetime": 28800,
"min-valid-lifetime": 3600,
"max-valid-lifetime": 86400,
"calculate-tee-times": true,          // default false; T1 = 50 %, T2 = 87.5 % of the actual lifetime
"t1-percent": 0.5,                    // defaults 0.50 and 0.875, per RFC 2131
"t2-percent": 0.875
```
By default kea-dhcp4 sends neither T1 nor T2. Explicit `renew-timer` / `rebind-timer` win over
calculation, so do not set them at global scope if some subnets should calculate. T2 is only sent
if it is below the valid lifetime, and T1 only if it is below T2 (or below the valid lifetime when
T2 is not sent). Lifetimes can be set globally, per shared network, per subnet, and per client class
(e.g. shorter for a `guest` class); min/default/max form a triplet and a client that asks for a
time with option 51 gets it clamped into that range.

## Lease caching (reduce DB writes)
```json
"cache-threshold": 0.25,
"cache-max-age": 600
```
A client that asks again gets its existing lease back, changing only the client-last-transmission
time (no disk or database write), if the lease age is under `cache-threshold` x valid lifetime
(0.25 means 25 %) and, when `cache-max-age` is set, under that many seconds; a lease with a
2000 s lifetime and threshold .25 is reusable for 500 s. Any important change (DDNS parameters,
hostname, a shorter lifetime) makes it not reusable. Since Kea 3.0.0 the default threshold is
0.25 with no max age, so caching is already on; set `cache-threshold` to 0.0 or `cache-max-age`
to 0 to disable it. It can be set globally, per shared network and per subnet. Useful with SQL
backends and chatty clients.

## Pool sizing with lease time
Addresses held ~ arrival rate x lease time (Little's law), because a departed client keeps its
address until the lease expires. With 2,000 distinct visitors spread evenly over 24 h (83 an hour),
an 8 h lease holds about 667 addresses and a 1 h lease about 83; a /22 has 1,022 usable
addresses. Real arrivals are bursty, so size for the busiest hours, not the daily average. Watch
the `assigned-addresses` and `total-addresses` statistics (per subnet: `subnet[N].assigned-addresses`).

## Verify
- [ ] A capture or Kea log shows option 51 (lease), 58 (T1) and 59 (T2) with the intended values,
  and pool utilisation stays below ~80 % at peak (Stork's utilisation bars turn warning at 80 %
  and critical at 90 %).
