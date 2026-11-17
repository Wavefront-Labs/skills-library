---
id: computing-software.systems-network-administration.wireshark.srtp-decryption
name: srtp-decryption
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, srtp, voip, sdes, dtls-srtp, rtp]
level: practitioner
status: verified
description: "Decrypt SRTP in Wireshark from SDES keys in SIP/SDP or DTLS-SRTP key logs, and recognise when encrypted media cannot be analysed for content."
sources:
  - https://www.rfc-editor.org/rfc/rfc3711
  - https://www.rfc-editor.org/rfc/rfc4568
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SRTP decryption

SRTP encrypts RTP payloads but leaves RTP headers (SSRC, sequence, timestamp) in clear. So jitter,
loss and sequence analysis work on encrypted streams; only audio playback needs keys. Wireshark 4.4.1 dissects SRTP
(it showed `SRTP PT=ITU-T G.711 PCMU, SSRC=..., Seq=...` for RTP/SAVP media announced in SDP) and shows the
`srtp.enc_payload`, `srtp.mki` and `srtp.auth_tag` fields, but it has no SRTP key preference and no cipher code in
its RTP dissector source: it does not decrypt SRTP itself. Decrypt with an external tool, then analyse the result.

## Key exchange methods
| Method | Where the key is | Decryptable? |
|--------|------------------|--------------|
| SDES (RFC 4568) | `a=crypto:1 AES_CM_128_HMAC_SHA1_80 inline:<base64>` in SDP | key is readable if SIP is cleartext or SIP-TLS decrypted |
| DTLS-SRTP (WebRTC) | derived from the DTLS handshake (`dtls.use_srtp.protection_profile` shows the offer) | Wireshark 4.4.1 has no SRTP key handling, so no |
| ZRTP | in-media DH | no (by design) |
| MIKEY | in SDP/SIP | rarely supported |

## SDES
Wireshark 4.4.1 parses `a=crypto` from SDP (the master key and suite are shown) and treats media on an `RTP/SAVP` m=
line as SRTP, but it does not use the key to decrypt. Check with:
```
sdp.crypto.crypto_suite
sdp.crypto.master_key
srtp.enc_payload
rtp.p_type
```
`sdp.crypto` and `srtp` alone are not valid filters in 4.4.1 ("is not a valid protocol or protocol field"). A decryptor
needs the base64 `inline:` value: 30 bytes for AES_CM_128 (16-byte master key plus 14-byte salt); the test SDP's key
printed as `master_key` 000102...0f.
If SIP is over TLS (5061), the SDP is only visible after you add TLS keys (key log or RSA for old servers) first (`sip.tls.port` defaults to 5061).

## DTLS-SRTP (WebRTC)
The DTLS handshake carries the `use_srtp` extension (`dtls.use_srtp.protection_profile`; Wireshark's SDP code lists the
`UDP/TLS/RTP/SAVP` profile as RFC 5764), but I found no SRTP key derivation in the 4.4.1 dissectors (no preferences, no
cipher calls in `packet-rtp.c`), so do not expect decrypted audio from a key log.

## Without keys
- RTP Stream Analysis still computes jitter, delta and lost packets on SRTP headers.
- Telephony > RTP > RTP Player cannot play encrypted audio.
- Enable the `rtp_udp` heuristic (`--enable-heuristic rtp_udp`) or Decode As RTP if no signalling was captured; without
  SDP, Wireshark shows the media as RTP, not SRTP.

## Gotchas
- Some SBCs re-key mid-call (re-INVITE with new crypto lines); capture the whole call.
- The suite name sets the authentication tag length (`AES_CM_128_HMAC_SHA1_80` or `_32`); a decryptor must use the one
  in the SDP.

## Verify
- [ ] RTP Stream Analysis shows the expected packet counts for the encrypted streams; decrypted audio comes from an external tool.

## Checked
Run with TShark 4.4.1 on a generated SIP INVITE/200 OK pair with SDP (`m=audio ... RTP/SAVP 0`, `a=crypto:1
AES_CM_128_HMAC_SHA1_80 inline:<base64 of 30 bytes>`) followed by RTP-shaped UDP packets: the media was labelled SRTP,
`sdp.crypto.crypto_suite`/`master_key`/`tag` printed, `rtp.p_type`, `rtp.ssrc`, `rtp.seq` printed; `-Y srtp` and `-Y
sdp.crypto` were rejected; `tshark -G currentprefs` has no SRTP preferences; the master RTP dissector source on GitHub
(`packet-rtp.c`) has SRTP context fields but no decrypt calls. `--enable-heuristic rtp_udp` made undeclared RTP appear
(0 to 5 packets). RFC 4568 suite names are as shown in SDP. ZRTP and MIKEY rows only name the RFC titles (RFC 6189 ZRTP: Media Path Key Agreement; RFC 3830 MIKEY).
