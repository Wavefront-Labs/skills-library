---
id: computing-software.systems-network-administration.wireshark.tls-sni-and-ja3-ja4-fingerprinting
name: tls-sni-and-ja3-ja4-fingerprinting
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tls-fingerprinting, sni, ja3, ja4, client-hello, threat-hunting, tshark]
level: practitioner
status: verified
description: "Identify TLS clients without decrypting: extract SNI, JA3/JA3S and JA4 fingerprints from Client and Server Hellos with Wireshark/tshark, and use them for inventory and hunting."
sources:
  - https://www.wireshark.org/docs/dfref/t/tls.html
  - https://github.com/FoxIO-LLC/ja4
  - https://github.com/salesforce/ja3
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNI and JA3/JA4 fingerprints

Encrypted traffic still exposes the Client Hello: server name (SNI), offered versions, cipher
suites, extensions and ALPN. Hashing those gives a fingerprint of the client software.

## SNI
```
tls.handshake.extensions_server_name
tls.handshake.extensions_server_name contains "dropbox"
tshark -r cap.pcapng -Y "tls.handshake.type == 1" -T fields -e ip.src -e tls.handshake.extensions_server_name | sort | uniq -c
```
Add it as a column: instant view of which services a host contacts.

## JA3 / JA3S
Wireshark 3.6+ computes them natively (the 3.4.0 source has no JA3 code, 3.6.0 does):
```
tls.handshake.ja3_full     # the raw string: version,ciphers,extensions,curves,point formats
tls.handshake.ja3          # MD5 of it
tls.handshake.ja3s         # server fingerprint from the Server Hello
```
JA3 is weakened by Chrome's extension order randomisation (introduced in 2023 per the JA4 README): the same browser yields many
JA3 hashes. Still useful for non-browser tools (malware, scripts, old clients).

## JA4
JA4 (FoxIO) sorts ciphers and extensions, so it is stable despite randomisation, and is human
readable, e.g. `t13d181100_85036bcba153_d41ae481755e` from the Python 3.14 test client (`t` TCP, `13` TLS 1.3,
`d` SNI present (`i` = IP/no SNI), `18` ciphers, `11` extensions, `00` no ALPN, then hashes); FoxIO's README lists Chrome as
`t13d1517h2_8daaf6152771_cb7bf5808d99`. Wireshark 4.2+ shows `tls.handshake.ja4` (and `tls.handshake.ja4_r`, the raw form); for older versions
use the JA4 Wireshark plugin or Zeek/Suricata packages. Wireshark 4.4.1 has no JA4S field (`tls.handshake.ja3s` exists).
The FoxIO suite also defines JA4S (server), JA4H (HTTP), JA4X (certificates).

## Using fingerprints
- Inventory: count distinct JA4 per host; a server that suddenly has a new client fingerprint (curl,
  Python requests, Go) deserves a look.
- Hunting: compare against published fingerprint lists (the JA4 repository describes a JA4+ database); check that a list is still maintained.
- Policy: some proxies and WAFs allow/deny by JA3/JA4.

## Gotchas
- Fingerprints identify libraries, not applications: every Go program has similar JA4.
- TLS inspection proxies replace the client fingerprint upstream with the proxy's own.
- ECH encrypts the inner SNI; you see the outer public name only.

## Verify
- [ ] tshark field extraction lists SNI and JA4 per client host, and known clients (a browser, curl)
  produce consistent values.

## Checked (2026-10-22)
- Ran tshark 4.4.1 over a loopback capture of Python 3.14 TLS 1.3, Python TLS 1.2 and OpenSSL 3.2.3 s_client clients: `tls.handshake.extensions_server_name`, `tls.handshake.ja3`, `ja3_full`, `ja4` returned values (for example `t13d181100_85036bcba153_d41ae481755e` for the Python TLS 1.3 client, with SNI `localhost`); `tls.handshake.ja4s` is rejected as an invalid field; `tshark -G fields` lists `ja3`, `ja3s`, `ja3s_full`, `ja4`, `ja4_r`.
- Version gates: fetched `packet-tls-utils.c` at tags wireshark-3.4.0 / 3.6.0 / 4.2.0 from GitHub; ja3 absent then present at 3.6.0, ja4 present at 4.2.0 (absent at 3.6.0).
- Fetched https://raw.githubusercontent.com/FoxIO-LLC/ja4/main/README.md: confirms the 2023 Chromium extension-order randomisation as the reason JA4 sorts extensions, the JA4+ family (JA4S, JA4H, JA4X ...), the Chrome example string and a Database section; the old example string in this skill did not match it and was replaced. The abuse.ch SSLBL site returned 503 so its mention was removed. The skill's `tshark ... | sort | uniq -c` SNI pipeline was run on the test capture.
