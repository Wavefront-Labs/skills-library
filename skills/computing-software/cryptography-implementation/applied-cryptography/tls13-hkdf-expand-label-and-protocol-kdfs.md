---
id: computing-software.cryptography-implementation.applied-cryptography.tls13-hkdf-expand-label-and-protocol-kdfs
name: tls13-hkdf-expand-label-and-protocol-kdfs
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, hkdf-expand-label, tls-1-3, derive-secret, quic, sp-800-135, tls-prf, hkdf, key-schedule-debugging]
level: advanced
status: verified
description: "Compute TLS 1.3 HKDF-Expand-Label and Derive-Secret, QUIC packet keys, and recognise SP 800-135 protocol KDFs (TLS 1.2 PRF, SSH, IKE) when debugging."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-7.1", "https://www.rfc-editor.org/rfc/rfc9001#section-5", "https://csrc.nist.gov/pubs/sp/800/135/r1/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 HKDF-Expand-Label and protocol KDFs

## HKDF-Expand-Label (RFC 8446 7.1)
```
HKDF-Expand-Label(Secret, Label, Context, Length) =
    HKDF-Expand(Secret, HkdfLabel, Length)
struct {
    uint16 length = Length;
    opaque label<7..255> = "tls13 " + Label;     # 1-byte length prefix
    opaque context<0..255> = Context;            # 1-byte length prefix
} HkdfLabel;
Derive-Secret(Secret, Label, Messages) = HKDF-Expand-Label(Secret, Label, Transcript-Hash(Messages), Hash.length)
```
Traffic keys: `key = HKDF-Expand-Label(traffic_secret, "key", "", key_len)`, `iv = ...("iv", "", 12)`.

## Python reference
```python
import hmac, hashlib, struct
def expand(prk, info, L, h=hashlib.sha256):
    out, t, i = b"", b"", 1
    while len(out) < L:
        t = hmac.new(prk, t + info + bytes([i]), h).digest(); out += t; i += 1
    return out[:L]
def expand_label(secret, label, ctx, L):
    full = b"tls13 " + label
    info = struct.pack(">H", L) + bytes([len(full)]) + full + bytes([len(ctx)]) + ctx
    return expand(secret, info, L)
```
Checked: with the RFC 8448 simple-handshake early secret `33ad0a1c...f92a`, `expand_label(early, b"derived", sha256(b""), 32)`
gives `6f2615a1...11ba`, the RFC's "derived" value (49-byte info `00 20 0d 'tls13 derived' 20 <hash>`), and pyca `HKDFExpand`
with the same info agrees. For DTLS 1.3 pass `prefix=b"dtls13"` (RFC 9147: the label prefix SHALL be "dtls13", no trailing space).

## QUIC (RFC 9001 5)
Initial secrets: `HKDF-Extract(initial_salt, client_dst_connection_id)`, then labels `"client in"`, `"server in"`,
and per-packet `"quic key"`, `"quic iv"`, `"quic hp"` (header protection). Run: with initial_salt `38762cf7...0a` and
DCID `8394c8f03e515708` the code above reproduces RFC 9001 A.1 (client secret `c00cf151...7aea`, key `1f369613...a22d`,
iv `fa044b2f42a3fd3b46fb255c`, hp `9f50449e...edd2`). QUIC v2 (RFC 9369) uses initial_salt `0dede3de...d9` and labels
`"quicv2 key"`, `"quicv2 iv"`, `"quicv2 hp"`, `"quicv2 ku"`.

## SP 800-135 protocol KDFs
Application-specific KDFs in SP 800-135 Rev 1 (check its current status on CSRC): IKEv1/IKEv2, TLS 1.0-1.2 PRF (4.2), X9.42 and X9.63, SSH KDF (RFC 4253
7.2, letters A-F), SRTP, SNMP and TPM. FIPS modules implement them as separate services; do not reuse
them for new designs.

## Gotchas
- The label prefix is `"tls13 "` with a trailing space; DTLS 1.3 uses `"dtls13"` (no space, RFC 9147).
- Context for most labels is a transcript hash, not raw messages.
- Lengths are the derived length, not the hash length, in the HkdfLabel.

## Verify
- [ ] RFC 8448 simple 1-RTT handshake secrets reproduce byte for byte.
- [ ] RFC 9001 Appendix A initial keys reproduce.
