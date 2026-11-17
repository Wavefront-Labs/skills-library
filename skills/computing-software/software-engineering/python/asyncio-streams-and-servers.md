---
id: computing-software.software-engineering.python.asyncio-streams-and-servers
name: asyncio-streams-and-servers
category: computing-software
field: software-engineering
product: python
tags: [python, py-asyncio-adv, asyncio-streams-servers, start-server, open-connection, streamreader, streamwriter, tcp]
level: practitioner
status: docs-checked
description: "Build asyncio TCP clients and servers with open_connection/start_server, framing with readuntil and readexactly, drain backpressure and the stream limit."
sources: ["https://docs.python.org/3/library/asyncio-stream.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# asyncio streams and servers

```python
import asyncio

async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info("peername")
    try:
        while line := await reader.readline():
            writer.write(line.upper())
            await writer.drain()              # flow control: waits when the write buffer is above its high watermark
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle, "127.0.0.1", 8888)
    async with server:
        await server.serve_forever()

async def client():
    r, w = await asyncio.open_connection("127.0.0.1", 8888)
    w.write(b"hello\n")
    await w.drain()
    print(await r.readline())
    w.close()
    await w.wait_closed()
```

## Framing (TCP is a byte stream)
- Text protocols: `readline()` or `readuntil(separator=b'\n')`; the separator may also be a tuple of separators.
- Binary: length prefix, then `readexactly(n)`, which raises `IncompleteReadError` if EOF arrives first (`IncompleteReadError.partial` holds the data read so far).
- `readuntil()` raises `IncompleteReadError` on EOF before the separator, and `LimitOverrunError` when data exceeds the stream limit (the data stays in the buffer and can be read again).
- `limit` on `open_connection` and `start_server` sets the `StreamReader` buffer limit; the default is 65536 bytes (64 KiB).

## TLS
- `start_server(..., ssl=ssl_context)` and `open_connection(host, port, ssl=ctx)` take an `ssl` argument; `StreamWriter.start_tls(sslcontext, ...)` upgrades an existing connection. Its `ssl_handshake_timeout` defaults to 60.0 s and `ssl_shutdown_timeout` to 30.0 s. See the TLS skill for context set-up.

## Gotchas
- `write()` should be used along with `await drain()`; `close()` along with `await wait_closed()` (not mandatory, but recommended).
- When the write buffer is below the high watermark `drain()` returns immediately without yielding to the event loop, so a loop of `write()` plus `await drain()` can starve other tasks (the docs describe a workaround).
- `start_server` defaults to `backlog=100`; `sock=` transfers socket ownership to the server.

## Verify
- [ ] A test starts the server on port 0, reads the chosen port from the server's sockets, sends a message and expects the reply.
- [ ] A client that sends half a line then disconnects makes the handler exit cleanly (`readline` returns what it has at EOF).

## Checked
Date: 2026-11-03. Confirmed against the asyncio streams documentation: signatures and defaults of `open_connection`/`start_server`, `limit`, `readexactly`, `readuntil` errors, `drain` semantics, `close`/`wait_closed`, `start_tls` timeouts, `get_extra_info`. Removed as unconfirmed: `asyncio.wait_for` timeouts, task exception logging, `wait_closed` 3.12 behaviour, slowloris and semaphore advice, `asyncio.Protocol` recommendation, `ConnectionResetError` handling.
Method: documentation only; no commands were run.
