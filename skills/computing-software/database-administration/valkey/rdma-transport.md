---
id: computing-software.database-administration.valkey.rdma-transport
name: rdma-transport
category: computing-software
field: database-administration
product: valkey
tags: [rdma, valkey-rdma, rdma-port, rdma-comp-vector, infiniband, module, transport]
level: advanced
status: docs-checked
description: "Valkey over RDMA: loading the valkey-rdma.so module, bind and port arguments, rdma-port and rdma-comp-vector tuning, protocol opcodes and current limitations."
sources:
  - https://valkey.io/topics/RDMA/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RDMA (remote direct memory access) is provided by a dynamically loaded module, `valkey-rdma.so`, and the page reports about 2 times higher QPS and lower latency than TCP/IP. It is Linux only, and you must already know how to configure RDMA on your hosts; the interface must support RDMA.

Run manually:
```
./src/valkey-server --protected-mode no --loadmodule src/valkey-rdma.so bind=192.168.122.100 port=6379
```
or put the `loadmodule` line in `valkey.conf`. Change it at runtime with `CONFIG SET rdma-port 6380`. RDMA and TCP can share a port by also passing `--port 6379`. From 9.0, `valkey-cli` and `valkey-benchmark` accept `--rdma` (`valkey-cli -h 192.168.122.100 --rdma`).

Tuning: `rdma-comp-vector` picks the RDMA completion vector; 0 and positive numbers are explicit, -1 (default) picks a random one per connection. Example 1: pin interrupt vectors 0-3 to CPUs 0-3, Valkey affinity to CPUs 4 and up, random vector; servers are isolated from kernel interrupts. Example 2: interrupt vector M, Valkey server M and completion vector M all on CPU M, fully isolating each server.

Protocol: reliable-connection queue pairs. Control messages are fixed 32-byte big-endian structs with opcodes `GetServerFeature` 0, `SetClientFeature` 1, `Keepalive` 2, `RegisterXferMemory` 3 (all required); new features are negotiated through the first two. Control uses `IBV_WR_SEND`; payload uses `IBV_WR_RDMA_WRITE_WITH_IMM` (required), the immediate value being the total length. 1024 WQEs are recommended.

Limitations: experimental (may change or vanish in any release), no TLS, no replication (use TCP or TLS), and too many active queue pairs can reduce performance.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/RDMA/ (page text read in full): Module-based, about 2 times QPS, Linux only, the loadmodule command and config-file form, CONFIG SET rdma-port, shared TCP port, --rdma from 9.0, rdma-comp-vector (-1 default) and both examples, RC queue pairs, 32-byte big-endian control messages, opcodes 0-3 all required, IBV_WR_SEND, IBV_WR_RDMA_WRITE_WITH_IMM, 1024 WQEs, limitations.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
