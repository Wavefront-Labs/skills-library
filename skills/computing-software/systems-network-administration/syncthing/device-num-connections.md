---
id: computing-software.systems-network-administration.syncthing.device-num-connections
name: device-num-connections
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, numconnections, multiple-connections, throughput]
level: advanced
status: docs-checked
description: "Use numConnections to open several parallel connections between two Syncthing devices and understand how counts are negotiated."
sources: ["https://docs.syncthing.net/advanced/device-numconnections.html", "https://docs.syncthing.net/users/tuning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# numConnections

A device setting, added in version 1.25.0. A zero value means to use the Syncthing default, which is a single connection.

## Negotiation
- If either side wants a single connection, one is used. Both must be configured for more.
- If both want several, the larger value wins (3 and 8 gives 8).
- A maximum of 128 connections is used under all circumstances; the docs say the return on further connections is likely negligible above about 10 to 20.

## Behaviour
- Additional connections are established over time, roughly one per minute when Syncthing is in a steady state, so the expected number may not show immediately after a change.
- One connection carries metadata such as index updates and pause status. Requests and responses use the others at random. The GUI shows `1 + n`, for example `1 + 3` for four connections.
- Device rate limits apply to the total across all connections, not per connection.
- TCP and QUIC both work. Only connections with the best priority are kept; by default TCP has better priority than QUIC, so a TCP connection causes existing QUIC connections to be closed. Priorities can be configured.
- Over a relay normally only one connection is established, though with lucky timing one relay connection in each direction is possible, shown as `1 + 1`.

## When it helps
- Improving performance by load-balancing traffic over multiple physical links, or in other scenarios.
- The tuning guide says to set it at or above the number of CPU cores available for maximum TLS concurrency, and to set `1` to reduce per-device memory and CPU overhead.

```xml
<device id="..."><numConnections>4</numConnections></device>
```
Both sides must be configured for more than one connection to be used.

## Checked
2026-11-04. Read the numConnections page, Configuration Tuning and the config page (device element `numConnections`): version, zero default, negotiation rules and the 3/8 example, 128 maximum, one-per-minute note, 1 + n GUI display, rate-limit total, TCP/QUIC priority, relay case, and the tuning advice. Moved the load-balancing line into the page's wording.
Method: documentation only; no commands were run.
