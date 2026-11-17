---
id: computing-software.software-engineering.clojure.agents-send-future-promise-delay
name: agents-send-future-promise-delay
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, agents, send, send-off, await, future, promise, delay, deliver, pmap, thread-pools, agents-futures-promises]
level: practitioner
status: gated
description: "Run async work with agents (send/send-off), futures, promises, delays, pmap and know the thread pools, error handling and shutdown-agents requirement."
sources: ["https://clojure.org/reference/agents", "https://clojure.org/reference/refs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agents, futures, promises, delays

**Goal:** pick the right async primitive and avoid hung JVMs and lost errors.

```clojure
(def ag (agent 0))
(send ag + 5)             ; fixed-size pool, CPU-bound work
(send-off ag slow-io)     ; growing pool, blocking work
(await ag)  @ag  (agent-error ag)  (restart-agent ag 0)
(def f (future (compute)))  @f        ; blocks; (deref f 1000 ::timeout)
(def p (promise))  (deliver p 42)  @p
(def d (delay (expensive)))  @d        ; computed once, cached
(pmap f coll)                          ; parallel map over lazy seq, semi-lazy
```
- Agents process actions one at a time per agent, in send order; exceptions put the agent in a failed state
  until `restart-agent` (set `:error-mode :continue` with an `:error-handler` for resilience).
- `future` and `send-off` use a non-daemon cached thread pool: call `(shutdown-agents)` at the end of a
  program, or the JVM may wait about a minute before exiting.
- `pmap` has overhead; use only for coarse work. For CPU data parallelism see `clojure.core.reducers`
  (`fold`).
- Exceptions in futures surface at `deref` time as `ExecutionException`.

## Failure modes
- Blocking `send` (not `send-off`) starves the shared pool.
- Forgetting `shutdown-agents` in `-main` programs.

## Self-check
Create a failing `send`, observe `agent-error`, restart, and send again.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; agents page read; thread-pool sizing, :error-mode/:error-handler options, the JVM exit delay, reducers and ExecutionException are not stated on the fetched pages. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
