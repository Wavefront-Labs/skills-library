---
id: computing-software.software-engineering.clojure.core-async-channels-go-blocks-thread
name: core-async-channels-go-blocks-thread
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, core.async, channels, go, chan, put, take, buffers, thread, alt, csp, timeout, core-async-channels-go, clojure-core-async]
level: advanced
status: docs-checked
description: "Use core.async channels with buffers, go blocks for parking, thread for blocking work, >!, <!, put!, take!, close! and timeouts; avoid blocking in go."
sources: ["https://clojure.github.io/core.async/", "https://clojure.org/news/2013/06/28/clojure-clore-async-channels", "https://github.com/clojure/core.async/blob/master/src/main/clojure/clojure/core/async.clj"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# core.async channels and go blocks

**Goal:** coordinate concurrent processes with CSP-style channels.

Dependency (deps.edn): `org.clojure/core.async {:mvn/version "<current>"}` (check the latest release).

```clojure
(require '[clojure.core.async :as a :refer [chan go <! >! <!! >!! close! timeout thread]])
(def c (chan 10))                       ; buffered; (chan (a/sliding-buffer 1)), (a/dropping-buffer 1)
(go (>! c :hello))                      ; parking put inside go
(<!! c)                                 ; blocking take outside go
(go (println (<! c)))
(thread (<!! c))                        ; real thread for blocking calls; returns a channel with the result
(close! c)                              ; takes get nil after close
(<!! (timeout 100))
```
- Inside `go`, use `<!` `>!` (park) not `<!!` `>!!` (block): blocking inside go blocks a limited dispatch pool.
- `nil` cannot be put on a channel; `nil` from a take means closed.
- `put!`/`take!` take callbacks for non-go code.
- Channels have unbuffered rendezvous behaviour unless a buffer is given.
- `go` rewrites code to a state machine: it does not cross function boundaries (a `<!` in a called function or
  inside `fn` within a go body fails).

## Failure modes
- Deadlock by unbuffered puts with no taker.
- "No more than 1024 pending puts are allowed on a single channel": unbounded producers.
- Exceptions inside go blocks do not reach the code that started them; catch inside and send them on a channel.

## Self-check
Create a producer and consumer pair over a buffered channel and close it, then confirm the consumer exits on nil.

## Checked
2026-11-02. Confirmed: core.async source (async.clj docstrings) and the 2013 core.async announcement: chan with buffers (sliding, dropping), go with parking <! and >!, blocking <!! and >!!, thread, close!, timeout, put!/take! callbacks, nil cannot be put, takes get nil after close, go does not cross function boundaries, the 1024 pending-puts limit. Softened: the exception-propagation bullet.
Method: documentation only; no commands were run.
