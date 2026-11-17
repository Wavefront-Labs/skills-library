---
id: computing-software.systems-network-administration.syncthing.relay-connections
name: relay-connections
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, relaying, relay, relay-pool]
level: practitioner
status: docs-checked
description: "Understand when Syncthing uses relays, how to point clients at private relays, and what a relay operator can see."
sources: ["https://docs.syncthing.net/users/relaying.html", "https://docs.syncthing.net/users/faq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relaying

## When it is used
Added in version 0.12.0. Relaying is enabled by default (`relaysEnabled` in the config) and is only used if two devices are unable to communicate directly. When connected via a relay, Syncthing periodically retries a direct connection and, if one is established, stops communicating via the relay. The transfer rate is much lower than a direct connection would allow.

## Using specific relays
Add the required relay servers to the Sync Protocol Listen Address field, under Actions and Settings, to use them exclusively of the public pool. The format is `relay://<host name|IP>[:port]/?id=<relay device ID>`:

```
relay://private-relay.example.com:443/?id=<relay device ID>
```
The relay's device ID is output on start-up.

## Security
The connection between two devices is still end to end encrypted; the relay only retransmits the encrypted data much like a router. A device must register with a relay to be reachable over it, so the relay knows the device's IP and device ID, much like a discovery server. The relay operator can see the amount of traffic flowing between devices.

## Unexpected addresses
Per the FAQ, outgoing connections to odd and unexpected addresses are most likely relay servers, run by volunteers all over the world; they usually listen on ports 443 or 22067, though that is up to the operator. Compare the address with the current list of active relays (relays.syncthing.net). Relays do not and cannot see the data transmitted via them.

## Improving speed
If the Connection Type in the Remote Devices list starts with `Relay`, a direct connection could not be established; the FAQ points to the Firewall Setup suggestions to enable direct connections. To run your own relay, see the relay-server-strelaysrv skill.

## Checked
2026-11-04. Read Relaying, the FAQ entries on relays and the unknown-address question, and the config page (`relaysEnabled`): version, default, retry behaviour, address format, security paragraph, port numbers and the Relay connection type check.
Method: documentation only; no commands were run.
