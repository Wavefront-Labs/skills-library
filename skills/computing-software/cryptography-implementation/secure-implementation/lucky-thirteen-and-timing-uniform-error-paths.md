---
id: computing-software.cryptography-implementation.secure-implementation.lucky-thirteen-and-timing-uniform-error-paths
name: lucky-thirteen-and-timing-uniform-error-paths
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, lucky13, timing-attack, mac-then-encrypt, cbc-padding-oracle, encrypt-then-mac, rfc-7366, uniform-error-responses, side-channel]
level: advanced
status: docs-checked
description: "Understand Lucky Thirteen-style timing leaks in MAC-then-encrypt CBC, write timing-uniform padding and MAC checks, and prefer AEAD or encrypt-then-MAC designs."
sources: ["https://www.isg.rhul.ac.uk/tls/Lucky13.html", "https://www.rfc-editor.org/rfc/rfc7366", "https://www.imperialviolet.org/2013/02/04/luckythirteen.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lucky Thirteen and timing-uniform error paths

## The attack
AlFardan and Paterson (2013) showed that all TLS and DTLS ciphersuites with CBC-mode encryption are potentially
vulnerable, including implementations that follow the RFC advice on padding oracles. The MAC covers 13 bytes of
header (5 bytes of TLS header plus 8 bytes of sequence number), and for chosen message lengths with HMAC-SHA1 a
record with at least two correct padding bytes is processed one hash compression evaluation faster than other
records. Timing the arrival of the error reveals padding validity, a padding oracle even when all errors look
identical. For TLS it needs many sessions repeating the same plaintext; for DTLS it works in a single session.

## Lessons for any design
1. Identical error messages are not enough; the **time** to produce them must not depend on secret-derived values.
2. MAC-then-encrypt with CBC is very hard to make constant time: random delays do not help because they average
   out, and Adam Langley's write-up shows even a careful patch leaked through a variable-time `DIV` instruction.
3. Authenticate ciphertext before touching padding: encrypt-then-MAC (RFC 7366 for TLS and DTLS) or AEAD makes the
   padding check unreachable for forged data.

## If you must process legacy MtE-CBC data
- Check padding in constant time: access memory as if the padding were the maximum length (capped by the public
  record length) and accumulate an error mask.
- Compute the MAC with the same number of hash blocks for any padding length, selecting the real result with masks,
  and extract the MAC from the record with constant memory accesses.
- Return a single error after the full computation.
- Rate-limit and alert on decryption failures (the TLS attack needs many sessions).

## Modern equivalents to watch
- Decompression or parsing before authentication (any format that decrypts, parses, then verifies).
- Different handling of "bad tag" vs "bad format after decryption" in streaming code.

## Verify
- [ ] No code path parses or unpads data before authentication succeeds.
- [ ] Legacy CBC handling passes a timing test for valid vs invalid padding.

## Checked
2026-11-01. Confirmed: attack scope, 13-byte header, one-compression timing difference, random-delay ineffectiveness,
AEAD recommendation (isg.rhul.ac.uk Lucky13 page); constant-time padding, MAC and DIV details (ImperialViolet
Lucky Thirteen post); encrypt-then-MAC for TLS and DTLS (RFC 7366 abstract). Removed: OpenSSL line-count claim,
256-byte scan, dudect.
Method: documentation only; no commands were run.
