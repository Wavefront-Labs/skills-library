---
id: computing-software.software-engineering.python.socket-programming-basics
name: socket-programming-basics
category: computing-software
field: software-engineering
product: python
tags: [python, py-networking, socket-programming, socket, tcp, udp, sendall, recv, create-connection, so-reuseaddr]
level: practitioner
status: docs-checked
description: "Write correct blocking TCP and UDP code with the socket module: create_connection, sendall, recv loops, framing, timeouts, SO_REUSEADDR and IPv6-ready servers."
sources: ["https://docs.python.org/3/library/socket.html", "https://docs.python.org/3/howto/sockets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Socket programming basics

```python
import socket, struct

# Client: resolves names, tries every address (IPv4/IPv6), applies a connect timeout
with socket.create_connection(("example.com", 80), timeout=5) as s:
    s.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")  # sendall, not send
    chunks = []
    while chunk := s.recv(4096):          # b"" means the peer closed
        chunks.append(chunk)

# Server: dual-stack listener
with socket.create_server(("", 9000), family=socket.AF_INET6, dualstack_ipv6=True, backlog=128) as srv:
    conn, addr = srv.accept()
    with conn:
        data = conn.recv(1024)

def recv_exact(sock, n):                   # TCP has no message boundaries
    buf = bytearray()
    while len(buf) < n:
        part = sock.recv(n - len(buf))
        if not part: raise ConnectionError("closed early")
        buf += part
    return bytes(buf)

def send_msg(sock, payload: bytes):        # length-prefix framing
    sock.sendall(struct.pack("!I", len(payload)) + payload)
def recv_msg(sock):
    (n,) = struct.unpack("!I", recv_exact(sock, 4))
    return recv_exact(sock, n)
```
`create_server` sets `SO_REUSEADDR` on POSIX for you. UDP: `socket.socket(AF_INET, SOCK_DGRAM)`, `sendto`/`recvfrom`; datagrams are lossy and unordered.

## Gotchas
- `send()` may send part of the data; `sendall()` loops. `recv(n)` returns *up to* n bytes.
- Always set timeouts (`settimeout`); the default is blocking forever. A `socket.timeout` is an alias of `TimeoutError` since 3.10.
- Validate the framed length before allocating (cap at a maximum) to avoid memory DoS.
- `gethostbyname` does not support IPv6; the docs say to use `getaddrinfo` for IPv4/v6 dual stack.
- Close sockets on error paths (use `with`).

## Verify
- [ ] Loopback echo test using `socketpair()` or a server on port 0 (`srv.getsockname()[1]`).
- [ ] Test a truncated message and an oversize length prefix.

## Checked
Date: 2026-11-03. Confirmed against the socket module docs: `create_connection`, `create_server` (SO_REUSEADDR on POSIX, `dualstack_ipv6`), `sendall`, `settimeout` default of None, `socket.timeout` as alias of `TimeoutError` since 3.10, `socketpair`, `gethostbyname` IPv6 limitation. Removed as unconfirmed: bind-address advice, selectors/threads advice, `shutdown(SHUT_WR)` half-close. The frame helpers are illustrative code built on the confirmed calls.
Method: documentation only; no commands were run.
