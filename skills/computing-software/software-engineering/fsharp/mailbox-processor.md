---
id: computing-software.software-engineering.fsharp.mailbox-processor
name: mailbox-processor
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, mailbox-processor, fsharp-async, agents, actor-model]
level: advanced
status: draft
description: "Build a message-loop agent with MailboxProcessor, Post and PostAndAsyncReply for serialised state."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MailboxProcessor
**Goal:** serialise access to state through a message queue.

```fsharp
type Msg =
    | Add of int
    | Get of AsyncReplyChannel<int>

let counter =
    MailboxProcessor.Start(fun inbox ->
        let rec loop total = async {
            let! msg = inbox.Receive()
            match msg with
            | Add n -> return! loop (total + n)
            | Get reply ->
                reply.Reply total
                return! loop total
        }
        loop 0)

counter.Post(Add 5)
let total = counter.PostAndReply Get                 // sync
let total2 = counter.PostAndAsyncReply Get |> Async.RunSynchronously
```
- State lives in the loop parameter; no locks needed.
- `Receive`, `TryReceive`, `Scan`, `Post`, `PostAndReply`, `PostAndAsyncReply`, `Error` event for unhandled exceptions.
- Messages queue unbounded; there is no built-in backpressure.

## Gotchas
- An exception inside the loop kills the agent silently unless you subscribe to `.Error`.
- For new code consider `System.Threading.Channels` or TPL Dataflow; MailboxProcessor remains supported (exact recommendation unconfirmed).

## Self-check
Post 1000 `Add 1` from parallel tasks and verify `Get` returns 1000.
