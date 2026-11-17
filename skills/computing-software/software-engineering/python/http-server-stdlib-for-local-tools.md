---
id: computing-software.software-engineering.python.http-server-stdlib-for-local-tools
name: http-server-stdlib-for-local-tools
category: computing-software
field: software-engineering
product: python
tags: [python, py-internet, http-server-stdlib, http-server, simplehttprequesthandler, threadinghttpserver, test-server, localhost]
level: practitioner
status: docs-checked
description: "Use http.server for local file serving, test doubles and tiny JSON endpoints: ThreadingHTTPServer, handlers, directory and bind options, and documented security limits."
sources: ["https://docs.python.org/3/library/http.server.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http.server for local tools

## Serve a directory
```
python -m http.server 8000 --bind 127.0.0.1 --directory ./site
```
The port defaults to 8000. By default the server binds to all interfaces; `--bind` (`-b`) takes an IPv4 or IPv6 address (IPv6 support added in 3.8). `--directory` (`-d`) is new in 3.7. `--protocol` (`-p`, new in 3.11) selects the HTTP version; the default is HTTP/1.0. Newer versions add `--tls-cert`/`--tls-key` (3.14) and `--content-type` (3.15).

## JSON endpoint / test double
```python
import json, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        payload = json.dumps({"echo": body}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
    def log_message(self, fmt, *args): pass       # silence per-request logging in tests

server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)   # port 0 = pick a free port
port = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
# ... run the client under test against http://127.0.0.1:{port} ...
server.shutdown(); server.server_close()
```
`SimpleHTTPRequestHandler` takes a `directory` argument (new in 3.7) naming the directory to serve; it defaults to the current directory.

## Not for production
The docs warn that `http.server` is not recommended for production because it only implements basic security checks. Its security section also says `SimpleHTTPRequestHandler` follows symbolic links (files outside the directory can be served) and that `send_header` and `send_response_only` do no input validation, so untrusted input can cause HTTP header injection.

## Gotchas
- `ThreadingHTTPServer` (3.7+) avoids one slow client blocking others; plain `HTTPServer` is single-threaded.
- `protocol_version` defaults to `'HTTP/1.0'`; if set to `'HTTP/1.1'` (persistent connections) the handler must send an accurate `Content-Length` header in every response.
- Symlinks are followed; do not serve untrusted trees.
- `ThreadingHTTPServer` handles requests with threads, which helps when browsers pre-open sockets that `HTTPServer` would wait on indefinitely.
- `serve_forever()` blocks; run it in a thread as above and stop it with `shutdown()` (see the `socketserver` docs for `shutdown`).

## Verify
- [ ] A client request shows the right status, headers and body.
- [ ] Tests run in parallel without port collisions (port 0).

## Checked

- 2026-11-03: checked against the CPython docs `library/http.server.rst` (production warning, `ThreadingHTTPServer` 3.7, `directory` 3.7, `protocol_version`, command-line options and versions, security considerations) and `library/socketserver.rst` (`serve_forever`, `shutdown`, `server_address`).
- Removed: the no-TLS-by-default, no-size-limit and no-authentication claims, the dotfile-exposure claim, the uvicorn/gunicorn/nginx advice, the CORS `end_headers` suggestion and the `curl` check.

Method: documentation only; no commands were run.
