---
id: computing-software.systems-network-administration.wireshark.tls-rsa-private-key-decryption
name: tls-rsa-private-key-decryption
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tls-decryption, rsa-key-decryption, rsa-keys-list, tls]
level: practitioner
status: verified
description: "Decrypt TLS with an RSA private key in Wireshark, recognise when it cannot work (ECDHE, TLS 1.3, resumption) and switch to key log files."
sources:
  - https://wiki.wireshark.org/TLS
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RSA private key decryption

With RSA key exchange, the client encrypts the pre-master secret with the server's public key, so the
server's private key decrypts the session. This works only for:
- TLS 1.2 and earlier, AND
- cipher suites with RSA key exchange (`TLS_RSA_WITH_*`), not `ECDHE_*`/`DHE_*`, AND
- full handshakes captured (not session resumption without the original handshake).

Modern servers negotiate ECDHE (forward secrecy) and TLS 1.3, where the private key cannot decrypt.

## Configure
Edit > Preferences > RSA Keys > Add new keyfile (PEM private key, or PKCS#12 `.pfx`/`.p12` with password); the
key must be the server certificate's key, not a client or CA key. Older dialog: Protocols > TLS > RSA keys list
(deprecated in favour of the RSA Keys dialog).
```
tshark -r in.pcapng -o "uat:rsa_keys:\"server.key\",\"\"" -Y http
```

## Check the cipher suite first
```
tls.handshake.type == 2
tls.handshake.ciphersuite == 0x009c        # TLS_RSA_WITH_AES_128_GCM_SHA256: decryptable
```
If the Server Hello shows `TLS_ECDHE_RSA_*` or TLS 1.3, stop and use `SSLKEYLOGFILE` from the client
or a key-log-capable server (nginx/OpenSSL keylog, Java agent).

## Debugging
Protocols > TLS > Debug file (`-o tls.debug_file:dbg.txt` in tshark) writes the decryption log. With a working RSA key
it contains `ssl_decrypt_pre_master_secret`; for ECDHE or TLS 1.3 sessions it ends in `Cannot find master secret`
or `Cannot find ... TRAFFIC_SECRET, decryption impossible` (no "not RSA" message exists).

## Gotchas
- Keys in an HSM cannot be exported to a file; Wireshark can use an HSM through *Add new provider...* (PKCS#11 DLL/.so
  plus vendor configuration), otherwise use a key-logging endpoint or a decrypting tap.
- Private keys in analyst workstations are a serious exposure; delete after use and prefer key logs
  (one session's secrets, not the server identity).

## Verify
- [ ] The packet list shows HTTP (or the inner protocol) and the TLS layer has a "Decrypted TLS" tab.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 against a loopback capture (dumpcap, Npcap) of Python TLS 1.2 `AES128-GCM-SHA256`, TLS 1.2 ECDHE and TLS 1.3 sessions: `-o "uat:rsa_keys:\"srv.key\",\"\""` decrypted only the RSA-kx session (HTTP shown), none without the key; cipher 0x009c was the chosen suite, 0xc030 (ECDHE) and 0x1302 were not decryptable.
- tls.debug_file text taken from the real log (message names above).
- RSA-key scope (server key only, PEM/PKCS#12, no resumption, HSM provider) from the Wireshark TLS wiki: https://gitlab.com/wireshark/wireshark/-/wikis/TLS
- Note: a default modern client (Python 3.14 ssl) does not offer RSA key exchange at all; the test client had to restrict ciphers to `AES128-GCM-SHA256`.
