---
id: computing-software.software-engineering.ruby.ruby-socket-programming
name: ruby-socket-programming
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, socket-programming, networking]
level: advanced
status: draft
description: "Write TCP clients and servers in Ruby: TCPServer, IO.select, timeouts, framing, partial reads and graceful shutdown."
sources: ["https://docs.ruby-lang.org/en/master/Socket.html", "https://docs.ruby-lang.org/en/master/TCPServer.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TCP sockets

```ruby
require "socket"
server = TCPServer.new("127.0.0.1", 9000)   # bind loopback unless you mean to expose it
loop do
  client = server.accept                    # blocks
  Thread.new(client) do |c|
    while (line = c.gets("\n", 4096))       # limit line length!
      c.write("echo: #{line}")
    end
  rescue Errno::ECONNRESET, EOFError
  ensure c.close
  end
end

# client with timeout (Ruby 3.0+)
s = Socket.tcp("example.com", 80, connect_timeout: 3)
s.write("GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")
IO.select([s], nil, nil, 5) or raise "read timeout"
data = s.read_nonblock(65_536, exception: false)
```
Multiplex with `IO.select(readers, writers, errors, timeout)` or use an event library (`async`, `nio4r`) for many connections.

## Gotchas
- TCP is a byte stream: one `write` is not one `read`. Frame messages with a length prefix or delimiter (see skill on pack/unpack) and loop until you have the full message.
- `read(n)` blocks until n bytes or EOF; `readpartial` returns what is available.
- Set `SO_REUSEADDR` (TCPServer does by default) to restart quickly; handle `Errno::EADDRINUSE`.
- A client that connects and sends nothing ties up a thread forever; add read timeouts and caps on line and body size.
- Close sockets in `ensure`; trap `SIGTERM`, stop accepting, and drain connections for graceful shutdown.
- `TCP_NODELAY`: `s.setsockopt(Socket::IPPROTO_TCP, Socket::TCP_NODELAY, 1)` for small latency-sensitive writes.

Verify: run the server, connect with `nc 127.0.0.1 9000`, type lines, and confirm echo plus clean close on Ctrl-D.
