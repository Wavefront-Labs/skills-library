---
id: computing-software.cryptography-implementation.openssl.tls12-cipher-list-strings
name: tls12-cipher-list-strings
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, cipher-strings, cipher-list, openssl-ciphers, tls-1-2, ecdhe, aead-only, mozilla-intermediate, nginx-ssl-ciphers]
level: practitioner
status: docs-checked
description: "Write and test OpenSSL TLS 1.2 cipher list strings: syntax (!, -, +, @SECLEVEL), expanding with openssl ciphers -v, ECDHE+AEAD-only policies, and server preference."
sources: ["https://docs.openssl.org/master/man1/openssl-ciphers/", "https://docs.openssl.org/master/man3/SSL_CTX_set_options/", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.2 cipher list strings

For TLS 1.2 and below, OpenSSL (and software that passes the string through, such as nginx `ssl_ciphers`, which takes
the format understood by OpenSSL) takes a cipher list string. TLS 1.3 suites are configured
separately (see TLS 1.3 ciphersuites skill).

## Syntax

- Names: `ECDHE-ECDSA-AES128-GCM-SHA256`; keywords: `ECDHE`, `AESGCM`, `CHACHA20`, `aRSA`, `kRSA`, `CBC`, `HIGH`, `ALL`.
- `A+B` = logical and (`ECDHE+AESGCM`).
- `!X` removes permanently; `-X` removes but may be re-added; `+X` moves to end.
- `@STRENGTH` sorts by key length; `@SECLEVEL=n` sets security level inline.
- `DEFAULT` = the build's default list (normally `ALL:!COMPLEMENTOFDEFAULT:!eNULL`); as a prefix it cannot be combined
  with other strings using `+` (`DEFAULT+AES` is invalid).

## Recommended policy: ECDHE + AEAD only

```
ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305
```

This list contains only ephemeral ECDH key exchange with AEAD ciphers, which gives forward secrecy. Add
`DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384` only if a client you must support needs it, with a 2048+ bit
DH group.

Excluded on purpose: `TLS_RSA_*` key exchange (no forward secrecy), CBC suites, 3DES, RC4, NULL, EXPORT and
anonymous (`aNULL`) suites.

## Test what a string expands to

```bash
openssl ciphers -v 'ECDHE+AESGCM:ECDHE+CHACHA20:!aNULL'
openssl ciphers -s -v -tls1_2 'HIGH:!aNULL:!kRSA:!CBC'   # -s: only supported by this build/seclevel
openssl ciphers -stdname -v 'DEFAULT'                    # IANA names alongside OpenSSL names
```

IANA names (`TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256`) differ from OpenSSL names;
`-stdname` shows the standard name next to each suite and `-convert` maps a standard name to the OpenSSL name.

## Server preference

Set server-side ordering so clients cannot pick the weakest offered suite:
`SSL_OP_SERVER_PREFERENCE` (the older name `SSL_OP_CIPHER_SERVER_PREFERENCE` still works but is discouraged),
nginx `ssl_prefer_server_ciphers on` (its default is `off`). When the option is not set the server follows the
client's preferences.

## Verify

- [ ] `openssl ciphers -v '<string>'` lists only ECDHE (or vetted DHE) AEAD suites.
- [ ] A TLS 1.2 handshake with each suite you intend to allow succeeds, and one with each excluded suite fails
      (`s_client -tls1_2 -cipher <suite>`).
- [ ] No `TLS_RSA_`, CBC, 3DES or RC4 suites offered.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-ciphers(1): string syntax (`+` as logical and, `!`, `-`, `+` prefixes, `@STRENGTH`, `@SECLEVEL=n`, `DEFAULT` prefix rule and its default expansion), keywords ECDHE, AESGCM, CHACHA20, aRSA/kRSA, CBC, HIGH, ALL, and the options `-s`, `-v`, `-stdname`, `-convert`; SSL_CTX_set_options(3) for `SSL_OP_SERVER_PREFERENCE` and its older name; nginx's ngx_http_ssl_module documentation for `ssl_ciphers` (OpenSSL format) and `ssl_prefer_server_ciphers` (default off). Removed the Mozilla recommendation, named attacks, Java and Go claims and the testssl.sh step, which were not checked.

Method: documentation only; no commands were run.
