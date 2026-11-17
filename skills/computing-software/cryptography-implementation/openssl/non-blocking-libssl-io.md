---
id: computing-software.cryptography-implementation.openssl.non-blocking-libssl-io
name: non-blocking-libssl-io
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, ssl-error-want-read, libssl, non-blocking-io, ssl-get-error, epoll, ssl-shutdown, openssl, event-loop]
level: advanced
status: docs-checked
description: "Drive libssl over non-blocking sockets: SSL_ERROR_WANT_READ/WANT_WRITE retries, partial writes, SSL_pending with edge-triggered epoll, EOF and shutdown handling."
sources: ["https://docs.openssl.org/3.0/man3/SSL_get_error/", "https://docs.openssl.org/3.0/man3/SSL_read/", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_mode/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-blocking libssl I/O

## The retry rule
After `SSL_read`, `SSL_write` or `SSL_do_handshake` returns <= 0 (or `SSL_shutdown` returns < 0), call `SSL_get_error()`:
| Result | Action |
|---|---|
| `SSL_ERROR_WANT_READ` | Wait for the socket to be readable, then repeat the **same call** |
| `SSL_ERROR_WANT_WRITE` | Wait for writable, then repeat the same call |
| `SSL_ERROR_ZERO_RETURN` | Peer sent close_notify; clean shutdown |
| `SSL_ERROR_SYSCALL` | Fatal I/O error (see errno); do not call `SSL_shutdown`. Before OpenSSL 3.0 an unexpected EOF also arrived here with errno 0 |
| `SSL_ERROR_SSL` | Protocol error; read the error queue (`ERR_get_error`) and abort |
A retry may again return WANT_READ or WANT_WRITE, with no fixed upper bound on iterations; wait on the direction
it asks for. After WANT_WRITE from `SSL_write`, do no other IO-triggering call before repeating the `SSL_write`.

```c
int n = SSL_read(ssl, buf, sizeof buf);
if (n <= 0) {
    switch (SSL_get_error(ssl, n)) {
    case SSL_ERROR_WANT_READ:  want_events(fd, EPOLLIN);  return AGAIN;
    case SSL_ERROR_WANT_WRITE: want_events(fd, EPOLLOUT); return AGAIN;
    case SSL_ERROR_ZERO_RETURN: return CLOSED;
    default: log_ssl_errors(); return FAIL;
    }
}
```

## Writes
- Repeat `SSL_write` with the same arguments, or set `SSL_MODE_ACCEPT_MOVING_WRITE_BUFFER` if the buffer
  address can change (the contents must stay the same).
- `SSL_MODE_ENABLE_PARTIAL_WRITE` lets `SSL_write` report success after a single record; the next call must send only the
  bytes left, as with `write()`.

## Edge-triggered epoll
OpenSSL may have decrypted application data buffered internally. After a successful read, loop while `SSL_pending(ssl) > 0`
(or until WANT_READ) before waiting for the next edge, or you stall with data in the buffer.

## EOF and shutdown
- OpenSSL 3 reports a TCP close without close_notify as `SSL_ERROR_SSL` with reason `SSL_R_UNEXPECTED_EOF_WHILE_READING`;
  `SSL_OP_IGNORE_UNEXPECTED_EOF` pretends a close_notify arrived (the error becomes `SSL_ERROR_ZERO_RETURN`) for protocols
  that delimit messages themselves. Do not ignore it where truncation matters.
- `SSL_shutdown` returns 0 when close_notify was sent but the peer's has not arrived: that is not an error, so do not
  call `SSL_get_error`; call `SSL_read` until it reports `SSL_ERROR_ZERO_RETURN` for the bidirectional shutdown. 1 means
  complete; < 0 means call `SSL_get_error`.

## Verify
- [ ] Test with a peer that sends 1-byte TCP segments and with large writes under backpressure.
- [ ] No busy loops: CPU stays idle while waiting.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 pages SSL_get_error (retry semantics, `SSL_ERROR_SYSCALL`, unexpected-EOF behaviour change), SSL_read (`SSL_pending`, retryable failures), SSL_CTX_set_mode (`SSL_MODE_ENABLE_PARTIAL_WRITE`, `SSL_MODE_ACCEPT_MOVING_WRITE_BUFFER`), SSL_shutdown (return values 0, 1, < 0; bidirectional shutdown; `SSL_OP_IGNORE_UNEXPECTED_EOF`) and SSL_CTX_set_options.
Corrected: `SSL_shutdown` returning 0 is not an error and `SSL_get_error` should not be called for it. Removed: the KeyUpdate/renegotiation claim and the "HTTP with Content-Length" example, which the pages do not state.
Method: documentation only; no commands were run.
