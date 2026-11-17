---
id: computing-software.database-administration.valkey.pipelining
name: pipelining
category: computing-software
field: database-administration
product: valkey
tags: [pipelining, rtt, round-trip, batching, throughput, evalsha, script-load]
level: practitioner
status: docs-checked
description: "Valkey pipelining: batching commands to cut round-trip time and socket syscalls, 10k batch advice, reply queue memory, and pipelining versus scripting."
sources:
  - https://valkey.io/topics/pipelining/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Valkey uses a request/response protocol, so each command normally pays one round-trip time (RTT). At 250 ms RTT, even a server capable of 100k requests/s serves at most four per second per connection; loopback RTT is sub-millisecond but still adds up.

Pipelining sends many commands without waiting for replies, then reads all replies at once. It has worked in every version. Raw demo: `(printf "PING\r\nPING\r\nPING\r\n"; sleep 1) | nc localhost 6379` returns three `+PONG` for one RTT.

It is not only RTT: without pipelining each command costs `read()` and `write()` syscalls and user/kernel context switches, far more than the data work. With pipelining many commands arrive in one `read()` and replies leave in one `write()`, so throughput grows almost linearly with pipeline length up to about 10 times the baseline.

Memory caveat: the server queues replies in memory while the client pipelines. Send batches of a reasonable size, for example 10k commands, read the replies, then send the next batch. Speed stays almost the same and extra memory is bounded.

Benchmark on the page (Ruby, 10,000 `PING`s over loopback): 1.185 s without versus 0.251 s with pipelining, about five times faster, the smallest gain since RTT is already low.

Scripting: scripts run read-compute-write on the server, which pipelining cannot do because the write needs the read reply. `EVAL`/`EVALSHA` can also be pipelined; `SCRIPT LOAD` guarantees `EVALSHA` will not fail.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/pipelining/ (page text read in full): 250 ms RTT / four requests per second, nc PING example, read()/write() syscall explanation, up to 10 times baseline, 10k batch advice and reply queueing memory, Ruby figures 1.185238 s versus 0.250783 s, scripting versus pipelining, SCRIPT LOAD.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.

