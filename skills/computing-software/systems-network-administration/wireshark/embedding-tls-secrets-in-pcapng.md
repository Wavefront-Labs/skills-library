---
id: computing-software.systems-network-administration.wireshark.embedding-tls-secrets-in-pcapng
name: embedding-tls-secrets-in-pcapng
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, inject-secrets, dsb, decryption-secrets-block, editcap, sslkeylogfile, tls-decryption, export-tls-session-keys]
level: practitioner
status: verified
description: "Embed TLS key logs into a pcapng Decryption Secrets Block with editcap --inject-secrets so decrypted captures can be shared, and strip them again before wider release."
sources:
  - https://www.wireshark.org/docs/man-pages/editcap.html
  - https://wiki.wireshark.org/TLS
  - https://www.ietf.org/archive/id/draft-ietf-opsawg-pcapng-02.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Embedding TLS secrets in pcapng (DSB)

Sending someone a capture plus a separate keylog file is error prone. pcapng has a
**Decryption Secrets Block** that carries the keys inside the file; Wireshark 3.0+ uses it automatically.

## Inject
```bash
# Keep only the keys for sessions present in this capture (avoid leaking unrelated sessions)
editcap --inject-secrets tls,keys.log in.pcapng with-keys.pcapng
```
Trim the keylog first: it may hold every TLS session of the browser for days. Wireshark can
export just the needed keys: File > Export TLS Session Keys (after loading the keylog), which
since 4.2 writes only secrets referenced by the packets (CLI: `tshark -r in.pcapng -o tls.keylog_file:keys.log
--export-tls-session-keys needed.log`; do not add `-q`, it skips dissection and the file comes out empty).
`editcap --inject-secrets` embeds the whole file it is given, so trim first.

Other secret types in editcap 4.4.1 (`--inject-secrets help`): `ssh`, `wg` (WireGuard), `opcua`. `--extract-secrets` (4.4+) writes the embedded secrets out instead.

## Use
Open `with-keys.pcapng`: TLS decrypts with no preference set. Capture File Properties lists
the DSB. tshark does the same (`tshark -r with-keys.pcapng -Y http2`).

## Strip before wider sharing
```bash
editcap --discard-all-secrets with-keys.pcapng no-keys.pcapng
```
Anyone with the DSB file can read all embedded sessions: treat it like the plaintext.

## Gotchas
- Only pcapng supports DSB; saving as pcap silently drops it.
- `mergecap` keeps DSBs from inputs; check the merged file if one input was sensitive.
- Key logs must match the session (client random); wrong file = silently no decryption.

## Verify
- [ ] Recipient opens the file and sees decrypted HTTP without configuring a keylog; public copies have no DSB.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 (editcap, tshark, capinfos, mergecap) with a loopback capture of TLS 1.3, TLS 1.2 ECDHE and TLS 1.2 RSA sessions and an 11-line combined keylog: `editcap --inject-secrets tls,keys.log in.pcapng with-keys.pcapng` gave a file whose `capinfos` reports "Number of decryption secrets in file: 1" and where `tshark -Y http` showed all three decrypted requests with no keylog set; `editcap --discard-all-secrets` then removed decryption (0 HTTP packets); `editcap --extract-secrets` writes a non-capture file; `tshark --export-tls-session-keys` exported 6 lines (0 with `-q`); `mergecap` of the DSB file with another kept the secrets block; `editcap -F pcap` dropped it (0 HTTP packets, no secrets).
- Source for the 4.2 export-only-referenced behaviour and DSB since 3.0: https://gitlab.com/wireshark/wireshark/-/wikis/TLS ; editcap type list from `editcap --inject-secrets help`.
