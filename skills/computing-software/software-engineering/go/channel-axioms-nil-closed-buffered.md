---
id: computing-software.software-engineering.go.channel-axioms-nil-closed-buffered
name: channel-axioms-nil-closed-buffered
category: computing-software
field: software-engineering
product: go
tags: [go, go-concurrency-basics, go-channel-axioms, channels, nil-channel, closed-channel]
level: practitioner
status: docs-checked
description: "Predict channel behaviour: send and receive on nil, closed and buffered channels, close ownership, and select with nil channels."
sources:
  - https://go.dev/ref/spec#Channel_types
  - https://go.dev/ref/spec#Close
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Channel axioms

**Goal:** know exactly what each channel operation does so deadlocks and panics stop being surprises.

| Operation | nil chan | closed chan | open chan |
|---|---|---|---|
| send | blocks forever | **panic** | unbuffered: proceeds when a receiver is ready; buffered: proceeds when there is room |
| receive | blocks forever | after buffered values are drained, returns the zero value without blocking (`ok=false`) | blocks until a value arrives (buffered: until not empty) |
| close | **panic** | **panic** | closes |

```go
ch := make(chan int, 2)
ch <- 1; ch <- 2; close(ch)
for v := range ch { fmt.Println(v) }   // drains buffered values, then ends
v, ok := <-ch                          // 0, false

// disable a select case by nilling the channel
for a != nil || b != nil {
    select {
    case v, ok := <-a: if !ok { a = nil; continue }; use(v)
    case v, ok := <-b: if !ok { b = nil; continue }; use(v)
    }
}
```

Spec facts behind the table:
- A nil channel is never ready for communication, so a `select` with only nil channels and no `default` blocks forever; that is why nilling a channel disables its case.
- `range` over a channel yields values until the channel is closed; ranging over a nil channel blocks forever.
- `close(ch)` on a receive-only channel is a compile error. Because sending to or closing an already closed channel panics, give each channel exactly one closing owner: the sender (or a coordinator after all senders finish), never a receiver.
- Capacity zero or absent means unbuffered; communication then succeeds only when both sender and receiver are ready.

## Gotchas
- `for range` over a channel that is never closed never ends, which leaks the goroutine.
- A directional type (`<-chan T`) in signatures documents who may not close: the compiler rejects `close` on it.

## Verify
Write a test with a timeout `select` to assert that a send blocks when the buffer is full.

## Checked
Checked 2026-11-08 against the Go specification (Channel types, Close, Send statements, Receive operator, For statements with range clause, Select statements; one page read for those passages).
Removed as not in the spec: remarks on `len`/`cap` races, `sync.WaitGroup`/`Once` coordination, the mutex comparison, `-race`, and `testing/synctest`.
Method: documentation only; no commands were run.
