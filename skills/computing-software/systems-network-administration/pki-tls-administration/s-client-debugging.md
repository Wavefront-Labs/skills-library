---
id: computing-software.systems-network-administration.pki-tls-administration.s-client-debugging
name: s-client-debugging
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [s-client-debugging, pki-openssl, openssl, s_client, sni, ocsp, alpn, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Use openssl s_client to see the served certificates, test verification, SNI, STARTTLS, OCSP status requests and ALPN, with the documented options."
sources:
  - https://docs.openssl.org/master/man1/openssl-s_client/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with openssl s_client
Goal: see exactly what the server sends.
```
openssl s_client -connect host:443 -servername host -showcerts </dev/null
openssl s_client -connect host:443 -servername host -tls1_3
openssl s_client -connect host:443 -servername host -verify_return_error -CAfile ca.pem -verify_hostname host </dev/null
openssl s_client -connect host:25 -starttls smtp -brief </dev/null
openssl s_client -connect host:443 -status -alpn h2 </dev/null
```
- `-showcerts` lists the certificates exactly as the server sent them, in order; it is not a verified chain.
- `-servername name` sets SNI. Without it, SNI is taken from the `-connect` name if that looks like a DNS name (default since OpenSSL 1.1.1). `-noservername` suppresses SNI, which lets you see what a server with no SNI returns.
- `-verify depth` turns on verification but the handshake continues after errors so all chain problems are visible. `-verify_return_error` makes verification errors abort the handshake. s_client is a test tool and by default accepts any chain the peer sends; non-test applications must not behave like that.
- `-CAfile`, `-CApath`, `-CAstore` set trust anchors; `-verify_hostname`, `-verify_ip`, `-verify_email` check the name; `-partial_chain`, `-purpose` and the other verification options are shared with `openssl verify`.
- `-status` sends a certificate status request (OCSP stapling) and prints the server's response; `-ocsp_check_leaf` and `-ocsp_check_all` require status checking.
- `-alpn list` advertises protocols, most desirable first (comma-separated, for example `h2,http/1.1`).
- `-starttls` supports: smtp, pop3, imap, ftp, xmpp, xmpp-server, irc, postgres, mysql, lmtp, nntp, sieve, ldap.
- `-proxy host:port` connects through an HTTP CONNECT proxy; for client-certificate tests add `-cert` and `-key`, but a certificate is not sent unless the server requests one.
- `-tls1`, `-tls1_1`, `-tls1_2`, `-tls1_3` and `-no_tls1_3` etc. pin or exclude versions; `-cipher` and `-ciphersuites` set TLS 1.2 and 1.3 suites.
- `-msg` shows protocol messages, `-trace` a verbose trace, `-debug` raw bytes, `-brief` a short summary of connection parameters, `-quiet` suppresses non-error output, `-prexit` prints session information even if the connection fails, `-reconnect` reconnects 5 times with the same session ID to test session caching.
Gotcha: `-ign_eof` (implied by `-quiet`) stops s_client shutting the connection at end of input; `-no_ign_eof` restores the shutdown.
Verify:
- [ ] The listed certificates match the intended chain.
- [ ] Verification with the intended CA file succeeds, with `-verify_return_error` set.

## Checked
Confirmed 2026-11-08 against the openssl-s_client manual: every option named above. Removed (the page does not describe them): output section labels such as "Verify return code", "SSL-Session" and the mTLS flow, grep filters, and the claim that a missing -servername "misleads" with the default certificate (the manual only describes the SNI default).
Method: docs-only read of cited pages, 2026-11-08
