---
id: computing-software.database-administration.memcached.noreply-risks
name: noreply-risks
category: computing-software
field: database-administration
product: memcached
tags: [noreply, fire-and-forget, pipelining, quiet-mode, protocol]
level: practitioner
status: docs-checked
description: "Use noreply to skip responses but know malformed requests may still produce errors you must read, plus meta q semantics."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/protocols/meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The optional `noreply` parameter instructs the server not to send the reply. It is documented for the storage commands (set/add/replace/append/prepend/cas), delete, incr/decr and touch, and as the last parameter of flush_all, verbosity and cache_memlimit.

Risk (protocol.txt): if the request line is malformed, the server cannot parse the noreply option reliably. In this case it may send the error to the client, and not reading it on the client side will break things. Clients should construct only valid requests.

Meta equivalent is the `q` flag, which uses noreply semantics for return codes: it hides "nominal" responses (the `EN` miss for mg, the `HD` success for ms), still returns other codes such as `EX` for a failed CAS, and errors are always returned, including syntax errors (`CLIENT_ERROR`). End a quiet pipeline with `mn` (it responds `MN`) to learn that all previous commands have been processed.

## Checked

2026-11-04. Confirmed against protocol.txt (storage commands, deletion, incr/decr, touch, flush_all/verbosity/cache_memlimit, meta noreply notes) and the Meta page (Quiet mode semantics). Removed: the closing Verify line.

Method: documentation only; no commands were run.
