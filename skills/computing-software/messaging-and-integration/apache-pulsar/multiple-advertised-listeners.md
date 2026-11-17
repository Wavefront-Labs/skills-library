---
id: computing-software.messaging-and-integration.apache-pulsar.multiple-advertised-listeners
name: multiple-advertised-listeners
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [advertised-listeners, bind-addresses, internal-listener-name, topic-lookup, nat, direct-broker-access]
level: advanced
status: docs-checked
description: "Let internal and external Pulsar clients reach brokers directly: advertisedListeners, bindAddresses, internalListenerName, lookup behaviour, NAT setup and HTTP admin listeners."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-multiple-advertised-listeners.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give clients in different networks a reachable broker address without a Pulsar proxy.

Why: topic lookup returns the owning broker address. Without extra config, external clients would get internal addresses and fail to connect. The deployment needs network perimeter security and should be used only with trusted clients in trusted networks.

Lookup: the client connects to a broker via the service URL (a load balancer in front of any broker), the broker finds the topic owner, returns the advertised address matching the listener the client came through (decided by the port, when `bindAddresses` is set), and the client connects straight to the owner.

Options (all in broker.conf):
- `advertisedListeners`: `<listener_name>:<protocol>://<host>:<port>,...` with schemes `pulsar`, `pulsar+ssl`, `http`, `https`.
- `bindAddresses`: maps listener and scheme to a local socket. Required for HTTP/HTTPS listener selection.
- `internalListenerName`: listener used for broker-to-broker traffic; defaults to `internal`.

Example:
```properties
advertisedListeners=internal:pulsar://192.168.1.11:6650,internal:pulsar+ssl://192.168.1.11:6651,external:pulsar://external-broker-1.example.com:6650,external:pulsar+ssl://external-broker-1.example.com:6651
bindAddresses=internal:pulsar://0.0.0.0:6650,internal:pulsar+ssl://0.0.0.0:6651,external:pulsar://0.0.0.0:16650,external:pulsar+ssl://0.0.0.0:16651
internalListenerName=internal
```

Network work: register a unique DNS name per broker, map each external IP and port by NAT or proxy to the internal IP and external listener port, and add a load balancer on the external listener port to any healthy broker.

Clients then need no `listenerName`; they just use the right service URL, such as `pulsar+ssl://external-brokers.example.com:6651`. The older `listenerName` setting is unnecessary when `bindAddresses` is correct.

Gotchas:
- The default internal listener derives URLs from `advertisedAddress` and the broker port settings. Declaring URLs under the internal name overrides them, so pointing it at an external load balancer can break broker-to-broker lookups and admin forwarding.
- Each local IP and port can belong to only one listener and scheme; use distinct external binding ports.
- For direct admin access, HTTPS requests on a listener's dedicated bind port keep that listener on owner or leader redirects; with hostname verification the broker certificates must match the hostnames clients use.

Verify: from an external client perform a lookup and confirm the returned address is the external one.

## Checked

2026-11-03. Confirmed against the Pulsar multiple advertised listeners page: `advertisedListeners`, `bindAddresses` (needed for HTTP/HTTPS listener selection), `internalListenerName` default `internal` and its derived URLs, one listener per IP and port, trusted-network note, `listenerName` no longer needed with correct bindings, and dedicated bind-port redirects with hostname verification.

Method: documentation only; no commands were run.
