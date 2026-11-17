---
id: computing-software.cryptography-implementation.openssl.s-client-sni-and-chain-inspection
name: s-client-sni-and-chain-inspection
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, s-client, tls-testing, showcerts, sni, chain-verification, verify-return-code]
level: practitioner
status: docs-checked
description: "Use openssl s_client to check SNI routing and the served chain: -servername, -showcerts, chain order, verify return codes 20/19/10/62 and hostname checks."
sources: ["https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man1/openssl-verification-options/", "https://docs.openssl.org/master/man3/X509_STORE_CTX_get_error/", "https://github.com/openssl/openssl/blob/master/apps/s_client.c"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SNI and chain inspection with s_client

## The baseline command
```
openssl s_client -connect host.example.com:443 -servername host.example.com \
  -showcerts -verify_return_error -verify_hostname host.example.com </dev/null
```
- `-servername` sets SNI (the name is sent as given, even an IP address). When omitted, s_client populates SNI from the name
  given to `-connect` if it has DNS-name form (and uses `localhost` if `-connect` is absent); otherwise you may see the
  default vhost's certificate.
- `-noservername` suppresses the SNI extension, showing what a client that sends none gets.
- `-connect 203.0.113.10:443 -servername host.example.com` tests one backend or a new load
  balancer before DNS moves.
- `</dev/null` closes stdin so the command exits after the handshake.

## Read the chain section
```
Certificate chain
 0 s:CN=host.example.com
   i:O=Example CA, CN=Example Issuing CA
 1 s:O=Example CA, CN=Example Issuing CA
   i:O=Example CA, CN=Example Root CA
```
Each `i:` should equal the next line's `s:`. The root normally isn't sent. Problems to spot:
- Only `0` present: the server sent no intermediate; clients that do not fetch missing intermediates themselves will fail.
- Wrong order or an unrelated old intermediate: verification depends on how the client builds the path.
- `-showcerts` prints each PEM; save and inspect with `openssl x509`.

## Verify return codes
At the end: `Verify return code: 0 (ok)`. Common failures:
| Code | Meaning | Usual cause |
|---|---|---|
| 20 | unable to get local issuer certificate | missing intermediate, or private CA not in `-CAfile` |
| 21 | unable to verify the first certificate | the chain holds a single certificate and no signature could be verified |
| 19 | self-signed certificate in certificate chain | private root not trusted |
| 18 | self-signed certificate | leaf is self-signed |
| 10 | certificate has expired | expired leaf or intermediate |
| 62 | hostname mismatch | name not in SAN (needs `-verify_hostname`) |
Without `-verify_return_error`, s_client reports the error and completes the handshake anyway.

## Variants worth knowing
```
openssl s_client -connect host:443 -servername host -CAfile private-root.pem   # private PKI
openssl s_client -connect host:443 -servername host -status                    # OCSP staple
openssl s_client -connect host:443 -servername host -alpn h2,http/1.1           # ALPN result
openssl s_client -connect host:443 -servername host -brief                      # one-screen summary
openssl s_client -connect host:443 -proxy proxy.internal:3128 -servername host  # via HTTP CONNECT
```
For mTLS servers, `Acceptable client certificate CA names` lists the CAs the server will accept.

## Compare with what clients use
s_client uses the OpenSSL default trust locations (`openssl version -d` shows `OPENSSLDIR`). Other clients may use
their own trust stores, so a code 0 here does not prove another client works; test with that client's own trust store too.

## Verify
- [ ] Return code 0 with `-verify_return_error -verify_hostname` for every public hostname.
- [ ] Chain lines link up from leaf to the last intermediate; no root, no stray certs.
- [ ] With and without SNI the expected certificates are served.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-s_client(1): `-servername` and the SNI default, `-noservername`, `-proxy host:port` (HTTP CONNECT), `-brief`, `-showcerts`, `-status`, `-alpn`, `-verify_return_error`; the strings `Verify return code: N (text)` and `Acceptable client certificate CA names` in apps/s_client.c and apps/lib/s_cb.c; and the verify error numbers and texts against X509_STORE_CTX_get_error(3) and x509_vfy.h. Removed the version-specific capture, the named public CA example and the list of failing client libraries.

Method: documentation only; no commands were run.
