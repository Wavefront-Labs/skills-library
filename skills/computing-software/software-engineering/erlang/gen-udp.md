---
id: computing-software.software-engineering.erlang.gen-udp
name: gen-udp
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-networking, gen-udp]
level: practitioner
status: docs-checked
description: "Erlang gen_udp: open, send, active receive messages, passive recv and common socket options (recbuf, sndbuf, broadcast, ip, inet6)."
sources:
  - https://www.erlang.org/doc/apps/kernel/gen_udp.html
  - https://www.erlang.org/doc/apps/kernel/inet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gen_udp datagrams
**Goal:** send and receive UDP datagrams.

```erlang
{ok, S} = gen_udp:open(9999, [binary, {active, true}]),
ok = gen_udp:send(S, {127,0,0,1}, 9999, <<"ping">>),
receive {udp, S, IP, Port, Data} -> {IP, Port, Data} after 1000 -> timeout end.
gen_udp:close(S).
```
- In an active mode the controlling process gets `{udp, Socket, PeerIP, PeerPort, Packet}` (a variant with an extra `AncData` field appears only if `recvtos`, `recvtclass` or `recvttl` is active). `recv/2,3` reads in passive mode. A socket in `{active, N}` mode sends `{udp_passive, Socket}` when the count reaches 0.
- Options of interest: `{recbuf, N}`, `{sndbuf, N}`, `{broadcast, true}` (permission to send broadcasts), `{ip, Address}` (which local address to use), `inet6`. The default receive buffer is `{recbuf, 9216}`.
- For UDP, `inet:setopts/2` advises that the user-level `{buffer, Size}` should not be larger than the MTU of the network path.

## Gotchas
- `{active, true}` has no flow control; use `{active, N}` or `{active, once}` as described under `inet:setopts/2`.

## Self-check
Send to your own port and verify the tuple received.

## Checked

2026-11-03. Confirmed in the `gen_udp` page (message shapes, `udp_passive`, `recbuf` default, `ip`, `inet6`, `recbuf`, `sndbuf`, `broadcast`) and `inet:setopts/2` (`active`, `buffer` and MTU). Removed: the "about 1400 bytes" figure and the unsupported delivery-guarantee statement.
Method: documentation only; no commands were run.
