---
id: computing-software.software-engineering.clojure.timeouts-retries-and-backpressure-patterns
name: timeouts-retries-and-backpressure-patterns
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, timeouts, retry, backoff, backpressure, circuit-breaker, core.async, deref-timeout, resilience, rate-limiting, timeouts-retry-backpressure]
level: advanced
status: draft
description: "Add timeouts with deref and core.async, retry with exponential backoff and jitter, and apply backpressure using bounded channels or queues to keep services stable."
sources: ["https://clojure.github.io/core.async/", "https://clojure.github.io/clojure/clojure.core-api.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timeouts, retries, backpressure

**Goal:** make concurrent or remote work fail predictably.

```clojure
(deref (future (slow)) 2000 ::timeout)                       ; returns ::timeout, but the work keeps running
(let [f (future (slow))] (or (deref f 2000 nil) (do (future-cancel f) :cancelled)))
(go (let [[v p] (alts! [work-ch (timeout 2000)])] (if (= p work-ch) v :timeout)))

(defn retry [n f]
  (loop [i 0]
    (let [r (try {:ok (f)} (catch Exception e {:err e}))]
      (cond (:ok r) (:ok r)
            (>= i n) (throw (:err r))
            :else (do (Thread/sleep (long (+ (* 100 (Math/pow 2 i)) (rand-int 100)))) (recur (inc i)))))))
```
- Timeouts do not stop the work; cancel futures, close channels or interrupt threads.
- Retry only idempotent operations and only on retryable errors (timeouts, 5xx); cap attempts, use exponential
  backoff with jitter.
- Backpressure: bounded `chan` buffers (`(chan 100)`) and `>!` that parks when full; avoid unbounded queues;
  drop or sample with `dropping-buffer` / `sliding-buffer` when losing data is acceptable.
- Rate limiting: a token-bucket via an atom/timestamp or a library (for example Resilience4j via interop).
- Circuit breakers stop calls to failing dependencies; libraries or Resilience4j interop provide them.
- Propagate deadlines downstream; log timeouts with correlation ids.

## Failure modes
- Retry storms multiplying load on an already failing service.
- Infinite waits from `@promise` or `<!!` without timeout.

## Self-check
Wrap a flaky function in `retry` and verify attempt count and growing delays in logs.
