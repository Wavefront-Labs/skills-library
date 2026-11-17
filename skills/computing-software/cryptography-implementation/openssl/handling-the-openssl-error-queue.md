---
id: computing-software.cryptography-implementation.openssl.handling-the-openssl-error-queue
name: handling-the-openssl-error-queue
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, libssl, err-get-error, error-queue, ssl-get-error, return-codes, err-clear-error, thread-local, c-api]
level: advanced
status: docs-checked
description: "Handle OpenSSL errors correctly: the per-thread error queue, ERR_get_error vs ERR_print_errors, clearing before SSL_* calls so SSL_get_error is right, and return-code conventions."
sources: ["https://docs.openssl.org/3.0/man3/ERR_get_error/", "https://docs.openssl.org/3.0/man3/SSL_get_error/", "https://docs.openssl.org/3.0/man3/ERR_error_string/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling the OpenSSL error queue

OpenSSL reports details through a **thread-local error queue**, not return
values. Code that ignores it gets mysterious failures: stale errors from an
earlier call make `SSL_get_error` misreport, and real causes are never logged.

## Return code conventions vary

| Function family | Success | Failure |
|---|---|---|
| Most `EVP_*`, `SSL_CTX_*` setters | 1 | 0 (sometimes negative) |
| `SSL_connect/accept/read/write` | > 0 | <= 0, then call `SSL_get_error` |
| `BIO_new_mem_buf` and similar constructors | pointer | NULL |
| `EVP_PKEY_verify` | 1 valid | 0 invalid signature, < 0 error |
| `EVP_DigestVerifyFinal` | 1 valid | any other value is failure: 0 is a bad signature, others a more serious error |

Check verify functions with `== 1`, never `if (ret)` - a negative error value is truthy and would accept a bad signature.

## Reading the queue

```c
static void log_ossl_errors(const char *where) {
    unsigned long e; char buf[256];
    while ((e = ERR_get_error()) != 0) {
        ERR_error_string_n(e, buf, sizeof buf);
        fprintf(stderr, "%s: %s\n", where, buf);
    }
}
```

`ERR_print_errors_fp(stderr)` does the same in one call. OpenSSL 3 adds
`ERR_get_error_all(&file, &line, &func, &data, &flags)` for richer context.
Draining (get) removes entries; `ERR_peek_error` leaves them.

## The SSL_get_error rule

`SSL_get_error(ssl, ret)` inspects the queue. If an unrelated earlier failure
left entries, it "will not work reliably" (its man page: the thread's error
queue must be empty before the I/O operation). So:

```c
ERR_clear_error();                 /* before every SSL_read/write/connect/accept/shutdown */
int r = SSL_read_ex(ssl, buf, len, &n) ? 1 : 0;
if (!r) switch (SSL_get_error(ssl, r)) {
  case SSL_ERROR_WANT_READ: case SSL_ERROR_WANT_WRITE: /* retry when ready */ break;
  case SSL_ERROR_ZERO_RETURN: /* peer sent close_notify */ break;
  case SSL_ERROR_SYSCALL: /* fatal I/O error: check errno, no SSL_shutdown */ break;
  default: log_ossl_errors("SSL_read"); /* fatal: tear down */
}
```

## Threads and event loops

The queue is per thread. In async runtimes where one request can hop threads,
drain the queue immediately after each call in the same thread, or errors get
attributed to another request.

## Do not leak details to peers

Log full OpenSSL errors server-side; return generic messages to clients.
Detailed decrypt/verify errors can become oracles.

## Verify

- [ ] Every libcrypto/libssl call checks its return per the table above.
- [ ] `ERR_clear_error()` precedes SSL I/O calls; errors are drained after failures.
- [ ] Verify results compared with `== 1`.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 pages ERR_get_error (`ERR_get_error` removes, `ERR_peek_error` does not, `ERR_get_error_all`), ERR_error_string (`ERR_error_string_n`), ERR_print_errors (`ERR_print_errors_fp`), ERR_clear_error, SSL_get_error (thread-local queue must be empty before the I/O call; `SSL_ERROR_SYSCALL` semantics; `SSL_R_UNEXPECTED_EOF_WHILE_READING`), EVP_DigestVerifyInit and EVP_PKEY_verify (return values).
Corrected: since OpenSSL 3.0 an unexpected EOF is `SSL_ERROR_SSL`, not `SSL_ERROR_SYSCALL`. Removed: the specific claim that stale entries turn `SSL_ERROR_WANT_READ` into `SSL_ERROR_SSL`, and the `d2i_*`/`PEM_read_*` row (not in the pages).
Method: documentation only; no commands were run.
