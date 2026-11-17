---
id: computing-software.software-engineering.erlang.gen-tcp
name: gen-tcp
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-networking, gen-tcp]
level: advanced
status: docs-checked
description: "Erlang gen_tcp: listen, accept, packet framing, active once/N flow control, passive messages and controlling_process."
sources:
  - https://www.erlang.org/doc/apps/kernel/gen_tcp.html
  - https://www.erlang.org/doc/apps/kernel/inet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gen_tcp and active modes
**Goal:** build a TCP server with backpressure.

```erlang
{ok, L} = gen_tcp:listen(8080, [binary, {packet, 4}, {active, once}, {reuseaddr, true}]),
{ok, S} = gen_tcp:accept(L),
ok = gen_tcp:controlling_process(S, Handler),
%% in the owner process
receive
    {tcp, S, Data} -> inet:setopts(S, [{active, once}]), handle(Data);
    {tcp_closed, S} -> closed;
    {tcp_error, S, Reason} -> {error, Reason}
end.
```
- `{active, true}` (the default) sends everything received as messages and gives no flow control. `{active, false}` is passive: read with `gen_tcp:recv/2,3`. `{active, once}` delivers one message and needs `inet:setopts/2` again; `{active, N}` counts down and then sends `{tcp_passive, S}` as the socket turns passive.
- `{packet, 1|2|4}` prefixes each packet with a 1, 2 or 4 byte big-endian length header added on send and stripped on receive. `raw` or `0` does no packaging. `line` only affects receiving.
- Inbound data goes to the socket owner (the process that created it) unless `{active, false}`. Run `accept` in several acceptor processes and hand sockets to per-connection processes.

## Gotchas
- Forgetting `controlling_process/2` leaves messages going to the process that created the socket.
- `{reuseaddr, true}` allows reuse of the local address; reuse is disallowed by default.

## Self-check
Write an echo server and test with a TCP client; flood it and watch queue length.

## Checked

2026-11-03. Confirmed in the `gen_tcp` page ({tcp, ...}, {tcp_closed, ...}, {tcp_error, ...}, {tcp_passive, ...}, controlling_process) and `inet:setopts/2` (`active` modes, `packet` types, `reuseaddr`). Removed: the Ranch recommendation, the `eaddrinuse` claim, and the exact `line` framing description.
Method: documentation only; no commands were run.
