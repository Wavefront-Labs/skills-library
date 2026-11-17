---
id: computing-software.database-administration.valkey.bulk-loading-pipe-mode
name: bulk-loading-pipe-mode
category: computing-software
field: database-administration
product: valkey
tags: [mass-insertion, bulk-loading, valkey-cli, pipe-mode, resp, echo]
level: practitioner
status: docs-checked
description: "Mass-insert data into Valkey by generating RESP and feeding valkey-cli --pipe, including RESP command format and how pipe mode detects completion."
sources:
  - https://valkey.io/topics/mass-insertion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ordinary clients are poor for bulk loads: one command at a time pays RTT, and pipelining requires writing while concurrently reading replies, with non-blocking I/O many clients lack. Instead generate a file in raw RESP and feed it with the pipe mode of `valkey-cli`:
```
cat data.txt | valkey-cli --pipe
All data transferred. Waiting for the last reply...
Last reply received from server.
errors: 0, replies: 1000000
```
It prints only server errors to standard output. The older `(cat data.txt; sleep 10) | nc localhost 6379` is unreliable: netcat cannot tell when transfer ends or check for errors.

RESP format per command: `*<args>\r\n`, then for each argument `$<len>\r\n<arg>\r\n`. Example `SET key value` is `"*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n"`. Length is the byte size. The page gives a Ruby helper `gen_redis_proto` that builds this, and a loop of `SET Key#{n} Value#{n}` for 1000 keys piped via `ruby proto.rb | valkey-cli --pipe`, reporting `errors: 0, replies: 1000`.

Pipe mode internals: it sends data as fast as it can while reading and parsing replies. When stdin ends it sends an `ECHO` with a random 20-byte string; reaching a bulk reply equal to those 20 bytes means the final reply arrived, so it exits. Counting parsed replies yields the number of commands transferred without parsing the input protocol.

## Checked
2026-11-03. Confirmed against the Valkey Bulk loading page (valkey.io/topics/mass-insertion/): `valkey-cli --pipe` usage and sample output, the netcat caveat, the RESP command layout and `SET key value` encoding, the Ruby helper and 1000-key example, and the ECHO with a random 20-byte string completion check. Nothing removed.
Method: documentation only; no commands were run.
