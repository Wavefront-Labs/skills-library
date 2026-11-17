---
id: computing-software.systems-network-administration.wireshark.application-keylog-for-tls-decryption
name: application-keylog-for-tls-decryption
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tls-decryption, application-keylog, sslkeylogfile, java-agent]
level: practitioner
status: verified
description: "Produce TLS key logs from curl, Python, Java, Go and Node so Wireshark can decrypt their traffic, including agents for apps without SSLKEYLOGFILE support."
sources:
  - https://wiki.wireshark.org/TLS
  - https://docs.python.org/3/library/ssl.html#ssl.SSLContext.keylog_filename
  - https://github.com/neykov/extract-tls-secrets
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Key logging from applications

Wireshark decrypts TLS 1.2/1.3 given the NSS key log (`CLIENT_RANDOM`, `CLIENT_TRAFFIC_SECRET_0`...).
Browsers honour `SSLKEYLOGFILE`; other clients vary.

| Client | How |
|--------|-----|
| curl (only TLS backends that support it, e.g. OpenSSL builds) | `SSLKEYLOGFILE=$HOME/keys.log curl https://...`; the Windows curl 8.10.1 build with Schannel wrote no file |
| Python `ssl` (and requests, which uses it) | `SSLKEYLOGFILE` honoured by `ssl.create_default_context()` (Python 3.8+ per the docs; checked on 3.14), or `ctx.keylog_filename = "keys.log"` |
| Node.js | `node --tls-keylog=keys.log app.js` |
| Go | `tls.Config{KeyLogWriter: f}` in code; no env var by default |
| Java | no built-in support; the Wireshark TLS wiki points to the `extract-tls-secrets` and jSSLKeyLog Java agents (not run here) |
| .NET, nginx, other servers/runtimes | check that runtime's own documentation for a key-log hook |
| OpenSSL s_client | `openssl s_client -keylogfile keys.log -connect host:443` |

## Using the log
Edit > Preferences > Protocols > TLS > (Pre)-Master-Secret log filename = `keys.log`. Or:
```
tshark -r app.pcapng -o tls.keylog_file:keys.log -Y http2
editcap --inject-secrets tls,keys.log app.pcapng app-dsb.pcapng     # embed for sharing
```

## Gotchas
- Start capture before the TLS session starts; resumed sessions need the original secrets.
- Key logs decrypt everything in that file; protect and delete them, never enable in production
  permanently.

## Verify
- [ ] The packet list shows decrypted protocols (HTTP, HTTP/2) and TLS records have a Decrypted TLS tab.

## Checked (2026-10-22)
- Ran all of these on Windows with Wireshark 4.4.1 against a loopback TLS server (Python 3.14 ssl, dumpcap + Npcap): `openssl s_client -keylogfile` (OpenSSL 3.2.3), Python `ctx.keylog_filename`, `SSLKEYLOGFILE` read by `ssl.create_default_context()` (`keylog_filename` printed the env value), `node --tls-keylog=...` (Node 20.20.2), Go `tls.Config{KeyLogWriter: f}` all produced key log files; `tshark -r app.pcapng -o tls.keylog_file:nodek.log -Y http` then decrypted the session (GET and 200 shown); `editcap --inject-secrets tls,keys.log` (lists tls, ssh, wg, opcua types) produced a DSB that decrypted with no preference.
- curl 8.10.1 (Schannel) with `SSLKEYLOGFILE` set wrote no file; libcurl's env docs say support depends on the SSL backend (https://raw.githubusercontent.com/curl/curl/master/docs/libcurl/libcurl-env.md).
- Java agents and the SSLKEYLOGFILE/NSS-library explanation read in the Wireshark TLS wiki https://gitlab.com/wireshark/wireshark/-/wikis/TLS. Removed unverified claims (.NET, nginx, live reread, QUIC).
