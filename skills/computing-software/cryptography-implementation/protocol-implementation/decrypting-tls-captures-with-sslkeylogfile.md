---
id: computing-software.cryptography-implementation.protocol-implementation.decrypting-tls-captures-with-sslkeylogfile
name: decrypting-tls-captures-with-sslkeylogfile
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, protocol-conformance, sslkeylogfile, wireshark, tls-debugging, nss-key-log, pcap, keylog-callback]
level: practitioner
status: docs-checked
description: "Decrypt TLS packet captures with SSLKEYLOGFILE: enabling key logs per client/library, loading them in Wireshark, and keeping key logging out of production."
sources: ["https://www.ietf.org/archive/id/draft-ietf-tls-keylogfile-02.html", "https://wiki.wireshark.org/TLS", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_keylog_callback/", "https://pkg.go.dev/crypto/tls#Config", "https://docs.openssl.org/3.0/man1/openssl-s_client/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decrypting TLS captures with SSLKEYLOGFILE

With forward-secret key exchange (all TLS 1.3, ECDHE in 1.2), having the
server's private key does not let Wireshark decrypt a capture. Instead, make
one endpoint log the per-session secrets in the NSS key log format and give
that file to Wireshark.

## Enable key logging

| Client/library | How |
|---|---|
| Firefox, Chrome, curl | set env `SSLKEYLOGFILE` to a writable path before starting (the underlying NSS, OpenSSL or BoringSSL library writes the secrets) |
| Safari, Edge | not supported: their TLS libraries (SChannel, SecureTransport) lack the mechanism (Wireshark wiki, 2019) |
| OpenSSL 3.4 and later apps | honour `SSLKEYLOGFILE` directly (see the Wireshark TLS wiki) |
| OpenSSL CLI | `openssl s_client -keylogfile <file> ...` |
| OpenSSL apps | `SSL_CTX_set_keylog_callback(ctx, cb)`; the callback receives a line in NSS format, log it followed by a newline |
| Go | `tls.Config{KeyLogWriter: w}`; the docs warn that this compromises security and is for debugging only |
| Java | no built-in; the Wireshark wiki points to the jSSLKeyLog agent |

The format covers TLS 1.2 and 1.3, plus DTLS and QUIC. A TLS 1.2 line uses the
label `CLIENT_RANDOM` for the master secret; TLS 1.3 uses labels such as
`CLIENT_TRAFFIC_SECRET_0`.

## Wireshark

Set Preferences > Protocols > TLS > (Pre)-Master-Secret log filename
(`tls.keylog_file`) to the key log, then open the capture.

`editcap --inject-secrets tls,<keys-file> in.pcap out-dsb.pcapng` embeds the
secrets in the capture so you can share one file (which then contains secrets).

## Safety

- The key log lets an attacker break confidentiality and integrity of every
  connection it includes, including previously stored traffic (IETF draft,
  Security Considerations). Control access to it, use only in development/test,
  delete afterwards, never commit.
- Production services should not log keys: audit manifests and debug configs
  for `SSLKEYLOGFILE`.
- For production debugging, prefer server-side structured TLS logs (version,
  cipher, alert codes) over decryption.

## Verify

- [ ] Wireshark shows decrypted application data for the session.
- [ ] Key log file deleted after use; no production process has SSLKEYLOGFILE set.

## Checked

2026-11-01. Confirmed against the IETF draft-ietf-tls-keylogfile-02 (format, labels, TLS 1.2/1.3/DTLS/QUIC, security
considerations), the Wireshark TLS wiki (browsers, curl, unsupported libraries, OpenSSL 3.4, jSSLKeyLog, `tls.keylog_file`,
editcap), OpenSSL 3.0 man pages (keylog callback, `s_client -keylogfile`) and pkg.go.dev crypto/tls (`KeyLogWriter`).
Removed: Python, Node and Java debug-flag rows, the `/proc` audit tip and the tshark command line (not confirmed).
Method: documentation only; no commands were run.
