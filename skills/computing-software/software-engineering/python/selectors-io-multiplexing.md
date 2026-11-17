---
id: computing-software.software-engineering.python.selectors-io-multiplexing
name: selectors-io-multiplexing
category: computing-software
field: software-engineering
product: python
tags: [python, py-networking, selectors-io-multiplexing, selectors, epoll, kqueue, non-blocking-io, event-loop]
level: practitioner
status: docs-checked
description: "Serve many sockets from one thread using selectors.DefaultSelector: registration, non-blocking accept/recv/send, partial writes and when asyncio is the better tool."
sources: ["https://docs.python.org/3/library/selectors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# selectors I/O multiplexing

`selectors.DefaultSelector` is an alias to the most efficient implementation available on the platform (for example `EpollSelector` or `KqueueSelector`).

```python
import selectors, socket

sel = selectors.DefaultSelector()
srv = socket.create_server(("127.0.0.1", 9000)); srv.setblocking(False)
sel.register(srv, selectors.EVENT_READ, data="accept")
out = {}                                          # per-connection pending bytes

def accept(sock):
    conn, _ = sock.accept(); conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data="client")

def readable(conn):
    try: data = conn.recv(4096)
    except (BlockingIOError, InterruptedError): return
    except ConnectionError: data = b""
    if not data:
        sel.unregister(conn); out.pop(conn, None); conn.close(); return
    out[conn] = out.get(conn, b"") + data.upper()
    sel.modify(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, "client")

def writable(conn):
    sent = conn.send(out[conn])                    # may send less than asked
    out[conn] = out[conn][sent:]
    if not out[conn]:
        sel.modify(conn, selectors.EVENT_READ, "client")

while True:
    for key, mask in sel.select(timeout=1.0):
        if key.data == "accept": accept(key.fileobj)
        else:
            if mask & selectors.EVENT_READ: readable(key.fileobj)
            if mask & selectors.EVENT_WRITE and key.fileobj in out: writable(key.fileobj)
```

## Rules
- Only watch for `EVENT_WRITE` while you have pending data; otherwise the loop spins because sockets are almost always writable.
- Every handler must be non-blocking and short; do CPU work elsewhere.
- Use `data=` to carry per-connection state or a callback.
- On Windows sockets are supported but pipes are not; on Unix both are.

## Gotchas
- A file object must be unregistered before it is closed.
- `EVENT_READ` on a listening socket means `accept` won't block, not that data exists.
- `modify()` is equivalent to `unregister()` followed by `register()`.
- This module is a high-level layer over `select`; reach for asyncio when you also need timers, TLS, subprocesses and cancellation.

## Verify
- [ ] Load test with many idle plus a few active clients; CPU stays near 0 when idle.
- [ ] Kill a client mid-write: the server logs and keeps serving.

## Checked

- 2026-11-03: checked against the CPython docs `library/selectors.rst`: `DefaultSelector` as the most efficient implementation, `register`/`unregister`/`modify`, `EVENT_READ`/`EVENT_WRITE`, platform file-object support, unregister-before-close.
- Removed: the 512-handle figure, the epoll/select dead-fd behaviour, level-triggered remarks and the asyncio load-generator hint (not stated in the docs read).

Method: documentation only; no commands were run.
