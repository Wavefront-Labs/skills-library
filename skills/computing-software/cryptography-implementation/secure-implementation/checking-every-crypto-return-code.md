---
id: computing-software.cryptography-implementation.secure-implementation.checking-every-crypto-return-code
name: checking-every-crypto-return-code
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, error-oracle, return-code-checks, fail-closed, openssl, cwe-252]
level: practitioner
status: docs-checked
description: "Check every crypto return value: OpenSSL's 1/0/negative verify convention, libsodium 0/-1, the CVE-2008-5077 lesson, and CWE-252."
sources: ["https://cwe.mitre.org/data/definitions/252.html", "https://docs.openssl.org/3.0/man3/EVP_DigestVerifyInit/", "https://docs.openssl.org/master/man3/ERR_get_error/", "https://www.openssl.org/news/secadv/20090107.txt", "https://doc.libsodium.org/public-key_cryptography/public-key_signatures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking every crypto return code

CWE-252 (unchecked return value) notes that if a function is used as a protection mechanism, an
unchecked return value can stop the code from seeing that the mechanism failed.

An unchecked or wrongly-tested return turns "signature invalid" into "signature valid". The
OpenSSL advisory of 7 January 2009 (CVE-2008-5077) describes several functions that incorrectly
checked the result of `EVP_VerifyFinal`, so a malformed signature was treated as good. It
affected DSA and ECDSA signature checks in SSL/TLS clients before 0.9.8j. The advisory states
that function returns 1 for success, 0 for failure and -1 for an error, and tells projects to
audit their handling of that code. The fix changed truthiness tests into explicit tests such as
`<= 0` for failure.

## Know the convention of each call

| API | Success | Failure |
|---|---|---|
| OpenSSL `EVP_DigestVerifyInit`, `EVP_DigestVerifyUpdate` | 1 | 0 |
| OpenSSL `EVP_DigestVerifyFinal`, `EVP_DigestVerify` | 1 | any other value; 0 means the signature did not verify, other values are more serious errors (and sometimes an invalid signature form) |
| libsodium `crypto_sign_verify_detached`, `crypto_sign_final_verify` | 0 | -1 |

Rule for verification: test for the documented success value explicitly (`== 1` for the OpenSSL
verify calls, `== 0` for libsodium). Never use a bare truthiness test on a verify result.

OpenSSL also documents that ignoring failure returns of `EVP_DigestVerifyInit()` can lead to
undefined behaviour in the later update, final or one-shot calls.

## Error queue

`ERR_get_error()` returns the earliest error code from the thread's error queue and removes the
entry; it can be called repeatedly until it returns 0 (no more errors). `ERR_peek_error()` reads
without removing.

## Fail closed

- Default the outcome variable to failure and set success only on the explicit success path.
- On any error in an authentication or decryption path, stop and return the generic failure
  rather than continuing with a partially initialised context.

## Verify

- [ ] Review or static analysis shows no verify call whose result is unused or tested by truthiness.
- [ ] Tests force each crypto call to fail and the code rejects.

## Checked

Method: docs-checked 2026-11-09 against CWE-252, OpenSSL 3.0 EVP_DigestVerifyInit man page (return values), OpenSSL master ERR_get_error man page, OpenSSL advisory 7 Jan 2009 (text and patch), libsodium public-key signatures page. Removed: the Apple goto-fail aside, table rows for X509_verify_cert, SSL I/O, CommonCrypto and PKCS#11, compiler attribute and linter recommendations (clang-tidy, CodeQL, errcheck, Rust must_use), RAND_bytes fallback advice, and the LD_PRELOAD fault-injection step, none of which the read sources state.
