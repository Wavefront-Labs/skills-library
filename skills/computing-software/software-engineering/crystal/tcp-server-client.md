---
id: computing-software.software-engineering.crystal.tcp-server-client
name: tcp-server-client
category: computing-software
field: software-engineering
product: crystal
tags: [tcp-server-client, sockets, tcp, tcpserver, tcpsocket, socket, accept, connect, read-timeout, line-protocol, echo-server, crystal]
level: practitioner
status: docs-checked
description: "Write a fiber-per-connection TCP server, connect clients with timeouts, and handle line protocols and closed sockets."
sources:
  - https://crystal-lang.org/api/latest/TCPServer.html
  - https://crystal-lang.org/api/latest/TCPSocket.html
  - https://crystal-lang.org/api/latest/Socket.html
  - https://crystal-lang.org/api/latest/IO/TimeoutError.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCPServer and TCPSocket

Goal: do TCP IO.

```crystal
require "socket"
server = TCPServer.new("127.0.0.1", 9000)
while client = server.accept?
  spawn do
    while line = client.gets
      client.puts line
    end
    client.close
  end
end
```
- Client: `TCPSocket.new("host", 9000, connect_timeout: 3)` (`dns_timeout` and `connect_timeout` are in seconds, integers or floats), `s.puts "x"`, `s.gets`, `s.read_timeout = 5.seconds` (`Time::Span | Nil`; a number of seconds is also accepted), `s.tcp_nodelay = true`, `s.keepalive = true`. `TCPSocket.open(host, port) { |s| ... }` closes the socket when the block returns.
- `accept?` returns the client `TCPSocket`, or nil if the server was closed (for example by another fiber), which is what ends the loop; `accept` instead raises `IO::Error` if the server is closed.
- `remote_address` and `local_address` return `Socket::IPAddress`. `TCPServer.new(host, port, backlog = SOMAXCONN, dns_timeout = nil, reuse_port = false)`; port 0 asks the kernel for a free port.
- Errors: a failed connect raises `IO::TimeoutError` or `Socket::ConnectError`; a read that exceeds `read_timeout` raises `IO::TimeoutError`, a subclass of `IO::Error`.

Gotchas:
- `gets` has overloads taking `limit` (`gets(limit : Int, chomp = false)`), so a line protocol can cap the line length.
- Bind `0.0.0.0` only intentionally; the default example binds loopback.

Verify: connect with `nc` and see echo.

## Checked

Checked 2026-11-08 against the API pages for TCPServer, TCPSocket, Socket and IO::TimeoutError (Crystal 1.22.2 docs). Removed: `Socket::Addrinfo.resolve`, the broken-pipe wording for `IO::Error` and the close-in-ensure advice, which the pages do not state.

Method: docs-only read of cited pages, 2026-11-08
