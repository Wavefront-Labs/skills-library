---
id: computing-software.database-administration.redis.pipelining-for-throughput
name: pipelining-for-throughput
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, pipelining, throughput, latency, redis-cli-pipe, mass-insertion, round-trip]
level: practitioner
status: docs-checked
description: "Cut Redis round trips with pipelining: batch sizing, pipeline vs MULTI vs script, cluster considerations, redis-cli --pipe for bulk loading, and benchmarking."
sources:
  - https://redis.io/docs/latest/develop/using-commands/pipelining/
  - https://redis.io/docs/latest/develop/clients/patterns/bulk-loading/
  - https://redis.io/docs/latest/develop/clients/redis-py/transpipe/
  - https://redis.io/docs/latest/develop/using-commands/multi-key-operations/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipelining

**Goal:** stop paying one network round trip per command; get several times the throughput for bulk operations.

## Why
With 0.5 ms RTT, one client doing sequential commands caps at ~2000 ops/s regardless of Redis speed. Pipelining sends N commands, then reads N replies. It also saves socket I/O on the server (fewer `read()`/`write()` system calls): throughput grows almost linearly with pipeline length at first and reaches about 10 times the unpipelined baseline. The Redis docs' loopback example improved by a factor of five.

```python
pipe = r.pipeline(transaction=False)      # redis-py; the default transaction=True wraps the batch in MULTI/EXEC
for uid in user_ids:
    pipe.hget(f"user:{uid}", "plan")
plans = pipe.execute()
```
Other clients have equivalents; check your client's documentation.

## Batch size
The server queues all replies in memory while a pipeline is processed, so send reasonable batches: the Redis docs suggest about 10,000 commands, read the replies, then send the next 10,000. Speed is nearly the same and the extra memory is bounded. Smaller batches (hundreds to a few thousand) also work; measure with your payload size.

## Pipeline vs MULTI vs script
- Pipeline: network optimisation only; other clients' commands can interleave.
- MULTI/EXEC: atomic; usually sent as a pipeline too.
- Script/Function: atomic and can branch on values read earlier in the same call. Scripts are the right tool for read-compute-write, which pipelining cannot help with.
- `EVALSHA` inside a pipeline can fail with NOSCRIPT; `SCRIPT LOAD` first guarantees it will not.

## Cluster
In a standard open source cluster, keys in a pipeline that map to different slots are a problem for plain pipelines (the multi-key page lists pipelines as single-slot), so cluster-aware clients split batches per node or slot; check your client's cluster pipeline support. Hash-tag related keys to keep batches on one node.

## Mass insertion
```bash
# generate Redis protocol (RESP) and stream it
python gen_resp.py | redis-cli --pipe
```
`--pipe` (redis-cli 2.6+) sends data as fast as possible while reading replies, finishes with an `ECHO` of a random 20-byte string to know when the last reply arrived, and prints `errors: N, replies: M`. The Redis bulk-loading page prefers it to a client loop or `netcat` for loading many keys. `--pipe-timeout` (default 30 s) aborts if no reply arrives after all data is sent.

## Also: MGET/MSET/HMGET
Multi-key commands are cheaper than many pipelined single-key commands when keys are in one slot.

## Gotchas
- Errors are per command inside the replies list; check each result.
- Do not pipeline commands that depend on the previous reply's value; use a script.

## Verify
`redis-benchmark -t set -n 100000 -P 1` vs `-P 50` shows the throughput difference on your network (`-P` is the pipeline size, default 1); app-side batch latency drops accordingly.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): pipelining page, bulk loading page,
redis-py pipelines page, multi-key operations page, redis-benchmark page, redis-cli reference. Confirmed: RTT effect, reply
queuing and the 10k batch suggestion, up to 10x throughput, `--pipe` mechanism and output, `--pipe-timeout` default,
`-P`, `-t`, `-n` flags, redis-py `pipeline(transaction=False)`, EVALSHA/SCRIPT LOAD advice, pipelines single-slot in
a cluster. Fixed: "100-1000 commands per batch" is not the documented figure (the page says for instance 10k); removed
client-specific cluster pipeline names (redis-py RedisCluster, Lettuce, go-redis ClusterClient) and the ioredis,
go-redis and Jedis one-liners, which the documentation read here does not cover.
Method: documentation only; no commands were run.
