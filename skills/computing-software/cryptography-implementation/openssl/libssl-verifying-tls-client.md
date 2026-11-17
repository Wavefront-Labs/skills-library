---
id: computing-software.cryptography-implementation.openssl.libssl-verifying-tls-client
name: libssl-verifying-tls-client
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, libssl, ssl-ctx, libssl-client, ssl-set1-host, ssl-verify-peer, sni, tls-client, openssl-3, c-api]
level: advanced
status: docs-checked
description: "Write a TLS client in C with OpenSSL 3 libssl that actually verifies the server: default trust store, SSL_VERIFY_PEER, SSL_set1_host, SNI, minimum version, and error checks."
sources: ["https://docs.openssl.org/3.2/man7/ossl-guide-tls-client-block/", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_verify/", "https://docs.openssl.org/3.0/man3/SSL_set1_host/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A verifying TLS client with libssl

OpenSSL's defaults do **not** verify the server certificate or hostname; a
client that only calls `SSL_connect` accepts any certificate. This is the
minimum correct setup (follows `ossl-guide-tls-client-block`).

```c
SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
if (!ctx) goto err;
SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);            /* 1. verify chain */
if (!SSL_CTX_set_default_verify_paths(ctx)) goto err;      /* 2. system trust store */
if (!SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION)) goto err;

SSL *ssl = SSL_new(ctx);
BIO *bio = BIO_new_connect("example.com:443");            /* or your own socket + SSL_set_fd */
if (!bio || BIO_do_connect(bio) <= 0) goto err;
SSL_set_bio(ssl, bio, bio);
if (!SSL_set_tlsext_host_name(ssl, "example.com")) goto err;  /* 3. SNI */
if (!SSL_set1_host(ssl, "example.com")) goto err;            /* 4. hostname check */
if (SSL_connect(ssl) < 1) {
    if (SSL_get_verify_result(ssl) != X509_V_OK)
        fprintf(stderr, "verify: %s\n",
                X509_verify_cert_error_string(SSL_get_verify_result(ssl)));
    ERR_print_errors_fp(stderr); goto err;
}
/* SSL_write_ex / SSL_read_ex ... then SSL_shutdown(ssl) */
```

## The four things people miss

1. `SSL_VERIFY_PEER` on the client: without it, verification runs but failures
   are ignored (result is only in `SSL_get_verify_result`).
2. A trust store: verification only succeeds if a trusted store is configured.
   `SSL_CTX_set_default_verify_paths` selects the default store; if your platform has none,
   load a bundle with `SSL_CTX_load_verify_locations(ctx, "ca-bundle.pem", NULL)`.
3. Hostname: `SSL_set1_host` makes the check include the name. Without it any
   certificate is acceptable unless the application checks the name itself.
4. SNI: needed for virtual-hosted servers to present the right certificate;
   SNI is not verification, and verification is not SNI. Do both.

For IP addresses use `X509_VERIFY_PARAM_set1_ip_asc(SSL_get0_param(ssl), "192.0.2.1")`.

## Reading and errors

Use `SSL_read_ex`/`SSL_write_ex`; on failure `SSL_get_error()` tells you
`SSL_ERROR_WANT_READ` (retry, non-blocking), `SSL_ERROR_ZERO_RETURN` (clean
close), or `SSL_ERROR_SSL` (fatal, check the error queue). Treat EOF without
close_notify as a possible truncation attack if your protocol lacks its own
length framing (OpenSSL 3 reports it as an error unless
`SSL_OP_IGNORE_UNEXPECTED_EOF` is set).

## Verify

- [ ] Connecting to a test server with a wrong hostname, an expired certificate and a self-signed certificate fails.
- [ ] Connecting to a correct host succeeds on every target OS (trust store present).
- [ ] Every libssl call's return value is checked.

## Checked

2026-10-31. Confirmed against the OpenSSL docs: ossl-guide-tls-client-block (`SSL_VERIFY_PEER`, `SSL_CTX_set_default_verify_paths`, `SSL_CTX_set_min_proto_version(TLS1_2_VERSION)`, `SSL_set_tlsext_host_name`, `SSL_set1_host`, `SSL_get_verify_result`/`X509_verify_cert_error_string`), SSL_CTX_set_verify (default `SSL_VERIFY_NONE`; in client mode failures only end the handshake with `SSL_VERIFY_PEER`), SSL_set1_host, X509_VERIFY_PARAM_set_flags (`X509_VERIFY_PARAM_set1_ip_asc`), SSL_get_error and SSL_CTX_set_options (`SSL_OP_IGNORE_UNEXPECTED_EOF`).
Removed: the `org.openssl.winstore` store, the `SSL_set1_host` version note, the claim about OPENSSLDIR contents on Windows/macOS, and the named badssl.com test hosts (external sites, not documented).
Method: documentation only; no commands were run.
