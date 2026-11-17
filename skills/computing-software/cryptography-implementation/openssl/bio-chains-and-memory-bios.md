---
id: computing-software.cryptography-implementation.openssl.bio-chains-and-memory-bios
name: bio-chains-and-memory-bios
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, bio-mem, openssl-bio, libssl, bio-pair, c]
level: advanced
status: docs-checked
description: "Use OpenSSL BIOs in C: memory BIOs for in-memory PEM, filter chains (base64, cipher, md), BIO pairs for TLS over custom transports, and freeing chains."
sources: ["https://docs.openssl.org/3.0/man3/BIO_s_mem/", "https://docs.openssl.org/3.0/man3/BIO_f_base64/", "https://docs.openssl.org/3.0/man3/BIO_new_bio_pair/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIO chains and memory BIOs

## Load PEM from memory
```c
BIO *b = BIO_new_mem_buf(pem, (int)pem_len);     /* read-only view, no copy */
EVP_PKEY *k = PEM_read_bio_PrivateKey(b, NULL, NULL, NULL);
BIO_free(b);
```
For output, `BIO_new(BIO_s_mem())`, write, then `BIO_get_mem_data(b, &ptr)` (the pointer is informative; no ownership transfers).

## Filter chains
```c
BIO *b64 = BIO_new(BIO_f_base64());
BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
BIO *out = BIO_push(b64, BIO_new_fp(stdout, BIO_NOCLOSE));
BIO_write(out, data, len);
BIO_flush(out);                       /* required: base64 and cipher BIOs buffer */
BIO_free_all(out);                    /* frees the whole chain */
```
For authenticated encryption use the EVP AEAD calls directly rather than a cipher BIO.

## TLS over custom transport
Use a BIO pair or two memory BIOs: `SSL_set_bio(ssl, rbio, wbio)`, feed received bytes into `rbio`, send whatever
appears in `wbio`. Handle `SSL_ERROR_WANT_READ` by reading more from the transport. (The BIO_new_bio_pair page could
not be read, so pair behaviour is not covered here.)

## Pitfalls
- `BIO_new_mem_buf` with length -1 uses `strlen`; binary DER data must pass the length.
- Forgetting `BIO_flush` truncates base64/cipher output.
- `SSL_set_bio` transfers ownership; do not free those BIOs yourself.
- Check return values: a 0 or -1 return from `BIO_read`/`BIO_write` is not necessarily an error; use
  `BIO_should_retry`. An empty memory BIO returns EOF (0) unless `BIO_set_mem_eof_return` is set.

## Verify
- [ ] Run under ASan/Valgrind: no leaks after `BIO_free_all`, binary input round-trips.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 pages BIO_s_mem (`BIO_new_mem_buf` is read only, not copied, length -1 uses `strlen`; `BIO_get_mem_data`; empty-BIO EOF and `BIO_set_mem_eof_return`), BIO_f_base64 (`BIO_FLAGS_BASE64_NO_NL`, `BIO_flush` finishes the final block, `BIO_push`, `BIO_free_all`), BIO_read (0 or -1 may only mean retry; `BIO_should_retry`) and SSL_set_bio (ownership of rbio and wbio passes to the SSL object).
Removed: the NUL-termination remark and the "cipher BIO is CBC/CTR only" claim (not on the pages read). The BIO_new_bio_pair page returned an empty stub, so no pair behaviour is claimed.
Method: documentation only; no commands were run.
