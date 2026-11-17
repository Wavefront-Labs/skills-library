---
id: computing-software.database-administration.valkey.valkey-benchmark-usage
name: valkey-benchmark-usage
category: computing-software
field: database-administration
product: valkey
tags: [valkey-benchmark, benchmark, throughput, pipeline, rand-int, cluster-benchmark, load-testing]
level: practitioner
status: docs-checked
description: "valkey-benchmark usage: -c -n -d -r -P -t -q options, __rand_int__ and __data__ placeholders, cluster mode with {tag}, TLS flags, and example runs."
sources:
  - https://valkey.io/topics/benchmark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`valkey-benchmark [OPTIONS] [--] [COMMAND ARGS...]` simulates many clients. Default tests run unless you pick `-t set,get` or give a custom command; separate several commands with a quoted `';'`, and prefix a command with N to repeat it.

Placeholders: `__rand_int__` (12-digit zero-padded integer from `-r` range, fresh per execution), `__data__` (payload of `-d` bytes), `{tag}` (routes to the right cluster node; required in keys with `--cluster`).

Key options and defaults: `-h` 127.0.0.1, `-p` 6379, `-c` 50 clients (at least the node count in cluster mode), `-n` 100000 requests, `-d` 3 bytes, `-P` pipeline depth (default 1), `-r` key space (without it every command uses one key), `-k` keepalive 1, `-q` quiet, `--csv`, `-l` loop forever, `-I` idle connections, `--threads`, `-3` RESP3, `--rps` rate limit, `--dbnum`, `-u valkey://user:pass@host:port/db` (`valkeys` for TLS), `--user` with `-a`. Cluster: `--cluster`, and `--rfr no|yes|all` sends reads to primaries, replicas or all (use only for read tests). Also `--enable-tracking`, `--tls` with `--cacert`, `--cert`, `--key`, `--sni`, `--insecure`, `--rdma`, `--mptcp`.

Examples:
- `valkey-benchmark -c 20 -P 10 --threads 2 -q`
- `valkey-benchmark -t set -n 1000000 -r 100000000` to load about a million keys.
- `valkey-benchmark -t set,lpush -n 100000 -q` printing e.g. `SET: 74239.05 requests per second`.
- `valkey-benchmark -r 10000 -n 10000 lpush mylist __rand_int__`.
- `valkey-benchmark -- multi ';' set key:__rand_int__ __data__ ';' incr counter ';' exec`.

Pipelining effect: `-n 1000000 -t set,get -P 16 -q` gave 403063 SET and 508388 GET requests/s.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/benchmark/ (page text read in full): Usage line, -t and custom commands, ';' quoting and N-prefix repeat, __rand_int__ (12 digits), __data__, {tag}, option defaults (-h, -p, -c 50, -n 100000, -d 3, -P 1, -k 1), -r single-key default, -u valkeys scheme, --rfr modes, TLS/RDMA/MPTCP flags, all example commands, pipelining figures.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
