---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-blocking-queries
name: consul-blocking-queries
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, blocking-queries, consul-watch, x-consul-index]
level: practitioner
status: docs-checked
description: "Long-poll the Consul HTTP API with index and wait parameters to react to changes without tight polling loops."
sources: ["https://developer.hashicorp.com/consul/docs/architecture/anti-entropy", "https://developer.hashicorp.com/consul/commands/kv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Most read endpoints support blocking queries: pass the last `X-Consul-Index` you saw as `?index=` and an optional `wait=`, and the server holds the request until data changes or the wait ends.

```sh
curl -si 'localhost:8500/v1/health/service/web?passing&index=0&wait=30s' | grep -i x-consul-index
curl -s  'localhost:8500/v1/health/service/web?passing&index=1234&wait=30s'
consul watch -type=service -service=web ./handler.sh
```

Gotchas: the index can go backwards (after a Raft snapshot restore, when the KV list item with the highest index is removed, or after an upgrade); if the returned index is lower than the previous one, reset it to 0. After each response check the index is at least 1, or the client busy-loops. A return is no guarantee of a change (the wait may have elapsed or an idempotent write occurred), so compare before acting. `wait` defaults to 5 minutes and is limited to 10 minutes; up to wait/16 extra random time is added. Rate limit the loop rather than sleeping each iteration: the docs suggest a token bucket with burst 2, degrading to polling about every 15 seconds when values churn.

Verify: the second call returns only after you change something (register or deregister an instance) or after the wait time.

## Checked

2026-11-03. Confirmed against the Blocking Queries page of the HTTP API docs (X-Consul-Index, index and wait parameters, 5 and 10 minute wait, wait/16 jitter, index reset and sanity check, rate limiting advice) and the consul watch command page. Removed: the `?stale` advice, the proxy idle timeout advice and the consul-template backoff claim, which the pages do not state.

Method: documentation only; no commands were run.
