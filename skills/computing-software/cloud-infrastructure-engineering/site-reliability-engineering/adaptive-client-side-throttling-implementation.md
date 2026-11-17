---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.adaptive-client-side-throttling-implementation
name: adaptive-client-side-throttling-implementation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [adaptive-throttling-implementation, client-rejection-probability, client-side-throttling, handling-overload, backpressure]
level: advanced
status: docs-checked
description: "Implement the SRE Book's adaptive client-side throttling: track requests and accepts over two minutes and reject locally with probability max(0,(requests-K*accepts)/(requests+1))."
sources: ["https://sre.google/sre-book/handling-overload/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implementing adaptive client-side throttling

SRE Book: when a backend is rejecting most requests, the cost of rejecting is still significant. Clients
should throttle themselves. Each client keeps, over the last two minutes:
- `requests`: number of requests attempted by the application layer
- `accepts`: number accepted by the backend (not rejected for overload)

and rejects locally with probability:
```
p_reject = max(0, (requests - K * accepts) / (requests + 1))
```
The book generally prefers K = 2: the client self-regulates when requests reach 2 * accepts, so roughly half of the
backend's resources may go to rejected requests, but state changes propagate to clients sooner when the backend stops
rejecting. Lowering K (the book's example is 1.1, about one backend rejection per ten accepts) makes throttling more
aggressive; raising it makes it less aggressive. Locally rejected requests still count in `requests`, which the book calls
the preferred behaviour.

## Implementation (Python, with self-check)
```python
import random, time, collections

class AdaptiveThrottle:
    def __init__(self, k=2.0, window=120.0, buckets=120, clock=time.monotonic):
        self.k, self.window, self.clock = k, window, clock
        self.width = window / buckets
        self.req = collections.deque(); self.acc = collections.deque()  # (bucket_ts, count)
    def _add(self, dq, now):
        b = int(now / self.width)
        if dq and dq[-1][0] == b: dq[-1][1] += 1
        else: dq.append([b, 1])
    def _sum(self, dq, now):
        lo = int((now - self.window) / self.width)
        while dq and dq[0][0] <= lo: dq.popleft()
        return sum(c for _, c in dq)
    def allow(self):
        now = self.clock()
        r, a = self._sum(self.req, now), self._sum(self.acc, now)
        self._add(self.req, now)
        p = max(0.0, (r - self.k * a) / (r + 1))
        return random.random() >= p
    def record_accept(self):
        self._add(self.acc, self.clock())

if __name__ == "__main__":
    t = [0.0]; th = AdaptiveThrottle(clock=lambda: t[0])
    sent = 0; per_sec = {}
    for i in range(30000):            # client offers 100 req/s for 300 s
        t[0] += 0.01
        if th.allow():
            sent += 1
            sec = int(t[0])
            if per_sec.get(sec, 0) < 10:   # backend capacity: 10 accepts/s
                per_sec[sec] = per_sec.get(sec, 0) + 1; th.record_accept()
    rate = sent / 300
    assert 15 < rate < 30, rate        # converges near K * capacity = 20 req/s
    print("backend sees req/s:", round(rate, 1))
```
Usage: call `allow()` before sending; if False, fail the request locally with the same error as an
overload rejection. Call `record_accept()` on any response that was not an overload rejection
(errors unrelated to overload count as accepts).

## Gotchas
- Count only overload rejections (the book's trigger is "out of quota" style rejections) as non-accepts; counting
  unrelated errors throttles healthy traffic.
- Per-backend-service state, not global per process.
- Low-traffic clients have little data; the `+1` keeps p sane, but expect slower adaptation.
- Combine with criticality: throttle lower-criticality first (separate instances per criticality).

## Verify
- [ ] Self-check passes.
- [ ] Load test with backend capacity capped: the share of backend work spent on rejections stays bounded as K implies.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Handling Overload", section on client-side throttling: the two-minute
history, `requests` and `accepts`, self-regulation once requests reach K times accepts, K = 2 preferred and the 1.1
example, locally rejected requests still counted. The Python class is illustrative code with its own self-check, not a
quote from the book. Removed: the HTTP and gRPC status list and the (K-1)/K bound.
Method: documentation only; no commands were run.
