---
id: computing-software.systems-network-administration.linux.curl-verbose-and-openssl-s-client
name: curl-verbose-and-openssl-s-client
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, curl, curl-debug, curl-verbose, openssl, openssl-s-client, tls-debugging, sni, certificate-chain, http-debugging, resolve, troubleshooting, networking, sysadmin]
level: practitioner
status: verified
description: "Debug HTTP and TLS from the shell: curl -v/--resolve/-w timing, bypassing DNS and proxies, and openssl s_client for SNI, certificate chains, expiry, protocols and STARTTLS."
sources:
  - https://curl.se/docs/manpage.html
  - https://docs.openssl.org/3.0/man1/openssl-s_client/
  - https://everything.curl.dev/usingcurl/verbose/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# curl -v and openssl s_client

**Goal:** prove where an HTTPS request fails — DNS, TCP, TLS handshake, certificate, HTTP
— and hand the evidence to whoever owns that layer.

## 1. curl
```bash
curl -v https://app.example.com/health                # * lines = connection/TLS, > request, < response
curl -sS -o /dev/null -w '%{http_code} dns=%{time_namelookup} tcp=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' https://app.example.com/
curl -v --resolve app.example.com:443:10.0.10.80 https://app.example.com/   # hit one backend, keep SNI/Host correct
curl -v --connect-to app.example.com:443:lb2.internal:443 https://app.example.com/
curl -v -H 'Host: app.example.com' http://127.0.0.1/                      # plain HTTP vhost test
curl -v --noproxy '*' https://...       # ignore http(s)_proxy env vars
curl --cacert corp-ca.pem https://...   # test with a specific CA instead of -k
curl -I -L https://example.com          # follow redirects, headers only
curl --trace-ascii - https://...        # full byte dump including bodies
```
A curl built on Schannel (Windows) prints no certificate subject or expiry lines in `-v`; use `openssl s_client` for those. Do not leave `-k` in scripts: it hides exactly the error you are debugging.
Common errors: `(6) Could not resolve host` (DNS), `(7) Failed to connect` (refused/filtered),
`(28) timeout`, `(35) SSL connect error` (the SSL handshake failed), `(60) peer certificate cannot be authenticated with known CA certificates`.

## 2. openssl s_client
```bash
openssl s_client -connect app.example.com:443 -servername app.example.com -showcerts </dev/null
#  -showcerts prints the certificate list as the server sent it
openssl s_client -connect host:443 -servername host </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
openssl s_client -connect host:443 -tls1_2 </dev/null    # does it still accept TLS 1.2? (-tls1_3 likewise)
openssl s_client -connect mail.example.com:587 -starttls smtp </dev/null
openssl s_client -connect ldap.example.com:389 -starttls ldap </dev/null
openssl s_client -connect host:443 -CAfile corp-ca.pem -verify_return_error </dev/null
```
A server that requires SNI rejects `-noservername` (against example.com: "no peer certificate available" and alert 40 handshake failure). Since OpenSSL 1.1.1, s_client sends SNI by default using the name given to `-connect` when it is a DNS name; pass
`-servername` explicitly when connecting by IP address or testing another name, and `-noservername` to suppress SNI.

## 3. Reading failures
- A verify error about a missing issuer usually means the server did not send the intermediate certificate (`-showcerts` lists only what the server sent): fix the server's chain, not the clients.
- Expired or mismatched names: check `-dates` and the subject alternative names.
- Works in curl but not in another runtime: that runtime may use a different trust store.

## Verify
- [ ] `openssl s_client` verifies the chain without error and the certificate shows the expected SAN and expiry.
- [ ] `curl -sS -w '%{http_code}'` returns the expected status through the real name and via `--resolve` to each backend.

## Checked

Documentation check. Checked 2026-10-27 against the curl manpage (curl.se, current, which lists the exit codes and --resolve, --connect-to, --noproxy, --trace-ascii and the -w time variables) and the OpenSSL 3.0 openssl-s_client and openssl-x509 pages (docs.openssl.org): the `-w` variables `time_appconnect`, `time_starttransfer` and the others, `--resolve`, `--connect-to`, `--noproxy`, `--cacert`, `--trace-ascii`, curl exit codes 6, 7, 28, 35 and 60, s_client `-connect`, `-servername`, `-noservername`, `-showcerts`, `-tls1_2`/`-tls1_3`, `-starttls` with `smtp` and `ldap`, `-CAfile`, `-verify_return_error`, and `openssl x509 -ext`. Corrected the SNI advice (SNI is sent by default since OpenSSL 1.1.1) and the description of exit codes 35 and 60. Removed the numeric verify error numbers and trust-store paths, which no checked page states.
Run 2026-11-01 against example.com only (curl 8.21.0 Schannel, OpenSSL 3.2.3, Windows 11): `-v`, the `-w` one-liner (`200 dns=... total=...`), `--resolve`, `--connect-to`, `--noproxy '*'`, `-I -L`, `--trace-ascii -`, `-k` worked; a wrong `--cacert` gave exit 60 and a missing `--cacert` file was rejected; a closed local port gave exit 7, an unresolvable name exit 6 and `--max-time 0.01` exit 28. `-H 'Host: ...' http://127.0.0.1/` was accepted (connection refused: no local server). s_client: default SNI, `-servername`, `-showcerts`, `-tls1_2`, `-tls1_3`, `-CAfile` plus `-verify_return_error` with an unrelated CA ("unable to get local issuer certificate", exit 1) and the `openssl x509 -noout -subject -issuer -dates -ext subjectAltName` pipe all behaved as written. Exit 35 and `-starttls smtp|ldap` were not run (no suitable test server); they stay documentation-confirmed.
Method: documentation plus commands run.
