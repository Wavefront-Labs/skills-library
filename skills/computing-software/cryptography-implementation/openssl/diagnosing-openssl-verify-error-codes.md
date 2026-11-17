---
id: computing-software.cryptography-implementation.openssl.diagnosing-openssl-verify-error-codes
name: diagnosing-openssl-verify-error-codes
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, chain-verification, openssl-verify, verify-error-codes, x509-v-err, unable-to-get-local-issuer, certificate-has-expired, self-signed-in-chain, troubleshooting]
level: practitioner
status: docs-checked
description: "Map OpenSSL verify errors (2, 10, 18-21, 26, 62) to causes and fixes, read chain depth, and reproduce client TLS failures with s_client -verify_return_error."
sources: ["https://docs.openssl.org/master/man1/openssl-verify/#diagnostics", "https://docs.openssl.org/master/man3/X509_STORE_CTX_get_error/", "https://docs.openssl.org/master/man1/openssl-s_client/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing OpenSSL verify error codes

OpenSSL reports `error N at depth D lookup: <text>`. Depth 0 is the leaf,
depth 1 its issuer, and so on. The same codes appear in libssl applications
via `SSL_get_verify_result()` and in tools built on OpenSSL, sometimes only as text.

| Code | Text | Usual cause | Fix |
|---|---|---|---|
| 2 | unable to get issuer certificate | Issuer of a locally looked-up certificate not found; trusted list incomplete | Supply intermediate (`-untrusted`) or root |
| 10 | certificate has expired | Leaf or intermediate past notAfter (check depth) | Renew; replace old cached intermediates; check clock |
| 9 | certificate is not yet valid | notBefore in the future | Clock skew (NTP) or freshly issued backdated incorrectly |
| 18 | self-signed certificate | Leaf is self-signed and not trusted | Add to trust store (dev only) or use CA-issued cert |
| 19 | self-signed certificate in certificate chain | Chain built from untrusted certificates ends in a self-signed root that is not trusted | Install the (private) root |
| 20 | unable to get local issuer certificate | Issuer of an untrusted certificate cannot be found | Missing intermediate on the server, or root absent from store |
| 21 | unable to verify the first certificate | Chain holds a single certificate and no signature could be verified | Server sends leaf only - serve fullchain |
| 26 | unsuitable certificate purpose | EKU/keyUsage does not allow the role | Reissue with correct EKU (serverAuth/clientAuth) |
| 62 | hostname mismatch | Name not in SAN | Reissue with correct SANs; check SNI sent |
| 23 | certificate revoked | CRL/OCSP says revoked | Reissue |
| 3 / 12 | unable to get CRL / CRL has expired | `-crl_check` without fresh CRL | Fetch current CRL |

## Reproduce what a client sees

```bash
openssl s_client -connect host:443 -servername host -verify_return_error -verify 5 </dev/null
openssl s_client ... -CAfile corp-root.pem       # with a private root
openssl s_client ... -showcerts | openssl x509 -noout -dates -subject -issuer
```

Without `-verify_return_error`, s_client continues the handshake and prints
`Verify return code: 20 (...)` at the end - easy to overlook.

## Checklist when the code is unclear

1. Which depth fails? Inspect that certificate (`-showcerts`, `openssl x509 -text`).
2. Is the client's trust store the one you think (containers, Java cacerts, certifi)?
3. Is the system clock correct?
4. Does the server send the right chain for this SNI name?
5. Is something on the path substituting certificates (check the issuer)?

## Verify

- [ ] Root cause identified at the failing depth, not only by error text.
- [ ] Fix confirmed with `s_client -verify_return_error` returning code 0.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed the numeric codes and message texts against X509_STORE_CTX_get_error(3) and include/openssl/x509_vfy.h (2, 3, 9, 10, 12, 18, 19, 20, 21, 23, 26, 62), the `error N at D depth lookup` format and depth numbering in openssl-verify(1), and `s_client -verify_return_error` / `-verify depth`. Fixed the text for code 26 and the causes for 2, 19, 20 and 21; removed the unconfirmed proxy and tool-name claims.

Method: documentation only; no commands were run.
