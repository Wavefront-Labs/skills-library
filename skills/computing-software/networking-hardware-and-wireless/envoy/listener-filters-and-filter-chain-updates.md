---
id: computing-software.networking-hardware-and-wireless.envoy.listener-filters-and-filter-chain-updates
name: listener-filters-and-filter-chain-updates
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, listener-filters, filter-chain-only-update, draining, lds-warming, hot-update]
level: practitioner
status: docs-checked
description: "How Envoy listener filters run before network filters and how a filter-chain-only listener update keeps matching connections open."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/listeners/listener_filters.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/listeners/lds.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# listener filters and filter chain updates
Listener filters run on a freshly accepted socket before any network filter and may change connection metadata, for example to influence which filter chain or cluster is used. They can stop and later continue iteration, which is how a call to a rate limit service can be inserted. Their purpose is to add system integration without touching Envoy core.

When LDS pushes a changed listener, the listener manager checks whether it is a "filter chain only update". If so it adds, updates and removes chains in place. Connections owned by removed chains are drained; if an old and new chain are protobuf-equivalent the chain's runtime info survives and its connections stay open. Adding or removing `additional_addresses` on a TCP listener is handled the same way: sockets for kept addresses stay, removed addresses stop accepting.

Other LDS rules from the docs:
- Every listener needs a unique `name` (a UUID is generated if absent), so give dynamic listeners stable names.
- A new or changed listener is warmed first, so any RDS it references is fetched before it takes traffic.
- Otherwise a changed listener is built as an entirely new listener (same listen socket if the address is unchanged).
- A removed listener drains for `--drain-time-s`.

Gotcha: a change to global listener attributes, not only chains, is not a chain-only update. Verify with the admin `/listeners` output and listener manager stats before and after a push.

## Checked
2026-11-03. Confirmed against listener_filters.rst and lds.rst. Removed or corrected: nothing.
Method: documentation only; no commands were run.
