---
id: computing-software.software-engineering.crystal.channels
name: channels
category: computing-software
field: software-engineering
product: crystal
tags: [channels, concurrency-fibers, channel, buffered-channel, unbuffered, send, receive, close, channel-closed, producer-consumer, crystal]
level: practitioner
status: docs-checked
description: "Pass values between fibers with Channel(T), buffered and unbuffered, close, receive? and iteration patterns."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Channels

Goal: communicate by channel.

```crystal
ch = Channel(Int32).new(10)     # capacity 10; omit for unbuffered
spawn { 5.times { |i| ch.send(i) }; ch.close }
while (v = ch.receive?)
  puts v
end
```
- `send` blocks when the buffer is full (or no receiver for unbuffered); `receive` blocks when empty.
- `close` makes `receive` on a closed, empty channel raise `Channel::ClosedError`; `receive?` returns nil instead; `send` on a closed channel raises.
- Typed: `Channel(Nil)` as a done-signal; `Channel(Exception | Int32)` to ship errors.
- Fan-out: several fibers `receive` from one channel; fan-in: many senders, one receiver.

Gotchas:
- If every fiber is blocked on channels the program cannot make progress; add a `timeout` branch via `select` for bounded waits.
- Close from the sender side only, once.
- Capacity is not changeable later.

Verify: producer/consumer spec with a known sum.

## Checked

Date 2026-11-03. Confirmed Channel(T).new with capacity, send, receive, receive?, close, Channel::ClosedError, and the select actions in the Channel source. Removed the unverifiable Deadlock message text.

Method: documentation only; no commands were run.
