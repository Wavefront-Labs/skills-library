---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.deterministic-subsetting-implementation
name: deterministic-subsetting-implementation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [subsetting-implementation, deterministic-subsetting-algorithm, subsetting, connection-pooling, load-balancing, grpc]
level: advanced
status: docs-checked
description: "Implement deterministic subsetting so each client connects to a small, balanced subset of backends: subset size choice, the SRE Book algorithm, and behaviour on resizes."
sources: ["https://sre.google/sre-book/load-balancing-datacenter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deterministic subsetting implementation

SRE Book: every connection needs some memory and CPU (periodic health checking) at both ends, which becomes
significant across many machines. Subsetting stops a single client connecting to a very large number of
backends, or a single backend receiving connections from a very large number of clients. Random subsetting
gives very uneven backend load; the book's **deterministic subsetting** balances it.

## Subset size
The book typically uses 20 to 100 backend tasks, but the right size depends on your service. Use a larger
subset if the number of clients is much smaller than the number of backends (so no backend never receives
traffic), or if client load is imbalanced, for example bursts concentrated in one client's subset.

## The algorithm (from the SRE Book)
Clients are assigned to "rounds"; in each round, all backends are shuffled with the same seed (the round
number) and dealt out in contiguous subsets to the clients of that round.
```python
import random
def subset(backends, client_id, subset_size):
    subset_count = len(backends) // subset_size
    round_ = client_id // subset_count
    rng = random.Random(round_)               # same shuffle for all clients in the round
    shuffled = backends[:]
    rng.shuffle(shuffled)
    subset_id = client_id % subset_count
    start = subset_id * subset_size
    return shuffled[start:start + subset_size]

# self-check: every backend gets roughly the same number of clients
if __name__ == "__main__":
    backends = [f"b{i}" for i in range(300)]
    from collections import Counter
    c = Counter(b for cid in range(1000) for b in subset(backends, cid, 30))
    assert max(c.values()) - min(c.values()) <= 1, c
```
The algorithm uses the client's integer id to pick a round and a subset, so give clients consecutive ids
(for example a task index) and the same backend list order.

## Behaviour on change
- The book wants the algorithm to handle restarts, failures and resizes of clients or backends with minimal
  connection churn (each replacement backend means new TCP connections and likely application-level
  negotiation), without knowing those numbers in advance. Check how the shuffle behaves when the backend list
  changes in your deployment.

## Where to implement
- In the client's load-balancing library, or by whatever component hands each client its endpoint list.

## Gotchas
- Client ids that are not consecutive integers break the round structure; map them to indices.
- Uneven per-client load (some clients much busier) still unbalances backends; combine with
  least-loaded or weighted policies.

## Verify
- [ ] Self-check passes for your client/backend counts.
- [ ] Production: per-backend connection counts are close to uniform (the book notes any overloaded backend forces overprovisioning of all).

## Checked
2026-11-01. Confirmed against the SRE Book "Load Balancing in the Datacenter" chapter: connection cost, 20 to 100
subset size and when to go larger, the random-subsetting imbalance, and the round-and-shuffle algorithm (the
Python above is an adaptation of the book's code). Removed: Rocksteadier and the gRPC A68 proposal, Envoy
`subset_config`, the 10% spread target, the StatefulSet remark and the reconnection-rate advice.
Method: documentation only; no commands were run.
