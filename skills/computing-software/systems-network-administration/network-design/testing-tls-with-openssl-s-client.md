---
id: computing-software.systems-network-administration.network-design.testing-tls-with-openssl-s-client
name: testing-tls-with-openssl-s-client
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-tools, openssl-s-client, tls, chain-validation, sni, starttls, cipher-testing]
level: practitioner
status: docs-checked
description: "Test TLS endpoints with openssl s_client: SNI, full chain and expiry, protocol and cipher probing, STARTTLS for SMTP/IMAP/LDAP, client certificates, and reading verify errors."
sources:
  - https://docs.openssl.org/3.0/man1/openssl-s_client/
  - https://docs.openssl.org/3.0/man1/openssl-x509/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing TLS with openssl s_client

## Basic connection with SNI
```
openssl s_client -connect app.example.net:443 -servername app.example.net </dev/null
```
`-servername name` sets the SNI extension in the ClientHello; if it is not given, SNI is populated from the `-connect`
name when that is a DNS name, so pass it explicitly when connecting by IP. Look at the certificate chain printout, the
verify return code, and the negotiated protocol and cipher.

## Expiry and names
```
openssl s_client -connect app.example.net:443 -servername app.example.net </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```
`openssl x509` supports `-subject`, `-issuer`, `-dates` and `-ext`.

## Full chain as sent
```
openssl s_client -connect app.example.net:443 -servername app.example.net -showcerts </dev/null
```
`-showcerts` prints the whole chain the server sent. A missing intermediate shows as a verification error on strict
clients (Java, curl, Python, IoT) even if browsers cope; fix the server's chain file.

## Probe protocols and ciphers
```
openssl s_client -connect host:443 -tls1_2
openssl s_client -connect host:443 -tls1_3
openssl s_client -connect host:443 -cipher 'ECDHE-RSA-AES128-GCM-SHA256' -tls1_2
```
`-tls1`, `-tls1_1`, `-tls1_2`, `-tls1_3` force a protocol version, and `-cipher` takes a cipher list (`-ciphersuites`
for TLS 1.3). A local OpenSSL build may not support old protocols; use a dedicated scanner for a full audit.

## STARTTLS services
```
openssl s_client -connect mail.example.net:25 -starttls smtp
openssl s_client -connect imap.example.net:143 -starttls imap
openssl s_client -connect dc01.example.net:389 -starttls ldap
```
Supported `-starttls` protocols in the OpenSSL 3.0 manual: smtp, pop3, imap, ftp, xmpp, xmpp-server, irc, postgres,
mysql, lmtp, nntp, sieve and ldap.

## Mutual TLS
```
openssl s_client -connect api.example.net:443 -cert client.crt -key client.key -CAfile ca.pem
```
`-cert` and `-key` supply the client certificate and key; `-CAfile` sets the trust anchors for verifying the server.

## Verify
- [ ] Verify return code 0 with the correct SAN and chain from a client that uses the system trust store, and weak
  protocols rejected.

## Checked
2026-10-28. Confirmed in the OpenSSL 3.0 s_client and x509 manual pages: `-servername` and SNI default, `-showcerts`,
`-tls1`..`-tls1_3`, `-cipher`, `-starttls` protocol list including ldap, `-cert`, `-key`, `-CAfile`, x509 `-subject`,
`-issuer`, `-dates`, `-ext`. Removed as unconfirmed: verify error numbers 20 and 21 and their messages, the
"Acceptable client certificate CA names" output line, the OpenSSL 1.1.1 and 3.x version statements, nmap and testssl.sh
recommendations.
Method: documentation only; no commands were run.
