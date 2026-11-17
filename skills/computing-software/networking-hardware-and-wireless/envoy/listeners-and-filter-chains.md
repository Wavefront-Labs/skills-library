---
id: computing-software.networking-hardware-and-wireless.envoy.listeners-and-filter-chains
name: listeners-and-filter-chains
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, listener, filter-chain, filter-chain-match, default-filter-chain, l4-filters]
level: practitioner
status: docs-checked
description: "Structure an Envoy listener with ordered filter chains selected by filter_chain_match, plus a default_filter_chain, and know what happens on no match."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/listeners/listeners.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/listeners/listener_filters.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# listeners and filter chains
An Envoy process can run any number of listeners (TCP or UDP), but the docs recommend one Envoy per machine. Each TCP listener holds `filter_chains`; a chain is selected per connection by its `filter_chain_match`, then the chain's connection-local network (L3/L4) filter stack is instantiated. The chain with the most specific match criteria wins.

```yaml
listeners:
- name: ingress
  address: { socket_address: { address: 0.0.0.0, port_value: 8443 } }
  filter_chains:
  - filter_chain_match: { server_names: ["api.example.com"] }
    filters: [ { name: envoy.filters.network.http_connection_manager } ]
  default_filter_chain:
    filters: [ { name: envoy.filters.network.tcp_proxy } ]
```
This is an illustrative skeleton; each filter needs its `typed_config` with an `@type`.

Gotcha: if no chain matches and no `default_filter_chain` is configured, the connection is closed, which clients see as a reset. SNI matching on `server_names` relies on the `envoy.filters.listener.tls_inspector` listener filter, which sets the detected transport protocol and server name.

Verify: the admin `GET /listeners` lists bound listeners and `GET /config_dump` shows the active chains. UDP listeners use UDP listener filters instead; they are instantiated once per worker and see every datagram that worker receives.

## Checked

2026-11-03. Confirmed against: listeners.rst, listener_filters.rst (default_filter_chain, closed if no match) and listener_components.proto (server_names, tls_inspector). Removed or corrected: the version hedge.

Method: documentation only; no commands were run.
