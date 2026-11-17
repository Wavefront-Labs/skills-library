---
id: computing-software.qa-testing-engineering.test-automation.toxiproxy-network-fault-testing
name: toxiproxy-network-fault-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [toxiproxy-toxics, toxiproxy, network-fault-injection, reliability-testing, resilience-testing]
level: advanced
status: gated
description: "Simulate network faults between a service and its dependencies with Toxiproxy: latency, bandwidth, timeouts, resets and slicer toxics from tests or CLI."
sources:
  - https://github.com/Shopify/toxiproxy
  - https://java.testcontainers.org/modules/toxiproxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network fault simulation with Toxiproxy

**Goal:** verify the application behaves well (timeouts, retries, fallbacks, error messages) when a dependency is slow, flaky or gone, deterministically in automated tests.

## How it works
Toxiproxy is a TCP proxy controlled by an HTTP API (port 8474). Point the app at the proxy port instead of the real dependency, then add or remove "toxics".

```bash
toxiproxy-server &
toxiproxy-cli create -l localhost:26379 -u localhost:6379 redis
toxiproxy-cli toxic add -t latency -a latency=1000 -a jitter=200 redis
toxiproxy-cli toxic add -t timeout -a timeout=0 redis     # data dropped, connection held while the upstream connection stays open
toxiproxy-cli toggle redis                                  # disable = connection refused
toxiproxy-cli toxic remove -n latency_downstream redis
```

## Toxic types
`latency` (+jitter), `bandwidth` (KB/s), `slow_close`, `timeout` (stop data; `timeout=0` holds the connection until the toxic is removed), `reset_peer` (TCP RST), `slicer` (split packets), `limit_data` (close after N bytes) and `packet_loss` (newer, `loss_rate` 0.0-1.0). Toxics attach to the `downstream` stream (server to client) by default; add `--upstream`/`-u` (CLI) or `stream=upstream` for the other direction. Run against Toxiproxy 2.13.0 on Windows: `create`, `latency` (1000 ms plus jitter turned a 0.25 s request into 1.35 s), `toggle` (connection refused), `reset_peer`, `bandwidth`, `slow_close`, `slicer` and `limit_data` all worked; a downstream `timeout=0` against an upstream that closes immediately returned an empty reply at once, while an upstream `timeout=0` hung the client until its own timeout. Each can apply `upstream` or `downstream` and to a `toxicity` fraction (0.5 = half the connections).

## In tests (Testcontainers) (gated: unconfirmed, source is paywalled or blocked)
Docker and a JDK were not available, so this Java snippet and the container image tag were not run (the 2.9.0 tag predates the 2.13.0 release).

```java
ToxiproxyContainer toxiproxy = new ToxiproxyContainer("ghcr.io/shopify/toxiproxy:2.9.0").withNetwork(net);
ToxiproxyClient client = new ToxiproxyClient(toxiproxy.getHost(), toxiproxy.getControlPort());
Proxy proxy = client.createProxy("pg", "0.0.0.0:8666", "postgres:5432");
proxy.toxics().latency("slow", ToxicDirection.DOWNSTREAM, 3000);
// assert the API returns 503 within its 2 s timeout instead of hanging
proxy.toxics().get("slow").remove();
```

## Test ideas
- Latency just below and above the client timeout.
- Dependency hangs (`timeout=0` on the upstream direction for a guaranteed hang): does the thread/connection pool exhaust?
- Reset mid-response: partial reads handled, no corrupted cache entries.
- Recovery: remove the toxic and confirm the circuit closes and pools heal without a restart.

## Verify
Each dependency has tests for slow, hung, refused and reset, and the app returns its designed degraded response within its timeout in each case.
