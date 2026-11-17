---
id: computing-software.software-engineering.ocaml.producer-consumer-with-mutex-and-condition
name: producer-consumer-with-mutex-and-condition
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, producer-consumer, blocking-queue, condition-wait, bounded-buffer]
level: advanced
status: docs-checked
description: "Implement a blocking queue using Mutex and Condition with while-loop waits, and shut down cleanly with a closed flag."
sources: ["https://github.com/ocaml-multicore/domainslib", "https://ocaml.org/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocking queue

```ocaml
type 'a t = { q : 'a Queue.t; m : Mutex.t; nonempty : Condition.t; mutable closed : bool }
let create () = { q = Queue.create (); m = Mutex.create (); nonempty = Condition.create (); closed = false }
let push t x = Mutex.protect t.m (fun () -> Queue.add x t.q; Condition.signal t.nonempty)
let pop t = Mutex.protect t.m (fun () ->
  while Queue.is_empty t.q && not t.closed do Condition.wait t.nonempty t.m done;
  Queue.take_opt t.q)                                    (* None after close and drain *)
let close t = Mutex.protect t.m (fun () -> t.closed <- true; Condition.broadcast t.nonempty)
```

## Notes
- Always wait in a `while` loop; wakeups can be spurious and another consumer may take the element.
- `Condition.wait` atomically releases the mutex and re-acquires it on wake.
- `Mutex.protect` (since 5.1) releases the mutex whether the function returns or raises.
- Use `broadcast` for shutdown so all waiting consumers exit.
- For bounded buffers add a second condition `nonfull`.

## Self-check
- [ ] All consumers terminate after `close` once the queue drains.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Mutex page (protect, since 5.1), the Condition page (wait atomically unlocks the mutex, can wake for no reason, signal/broadcast, a second condition for a bounded queue) and the Queue page (add, take_opt, is_empty).

Removed or corrected: the earlier-versions Fun.protect remark.

Method: documentation only; no commands were run.
