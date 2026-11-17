---
id: computing-software.cryptography-implementation.crypto-libraries.big-endian-integers-and-fixed-length-key-encodings
name: big-endian-integers-and-fixed-length-key-encodings
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, integer-encoding, i2osp, big-endian, fixed-length-encoding, cross-language, ecdsa]
level: practitioner
status: verified
description: "Encode integers and keys consistently across languages: big-endian fixed-length scalars, leading-zero stripping bugs, two's-complement BigInteger output, and I2OSP."
sources: ["https://www.rfc-editor.org/rfc/rfc8017#section-4", "https://www.secg.org/sec1-v2.pdf", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigInteger.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Big-endian integers and fixed-length key encodings

## The rule
Crypto encodings use big-endian, fixed-length octet strings: I2OSP(x, len) in RFC 8017, field elements in SEC1.
A P-256 scalar or coordinate is always 32 bytes, even when the value has leading zeros.

## Classic bugs
- **Java `BigInteger.toByteArray()`** returns the minimal two's-complement big-endian form (Javadoc: at least one sign
  bit, `ceil((bitLength()+1)/8)` bytes): it adds a leading `0x00` when the top bit is set (33 bytes for a 256-bit value
  with its high bit set) and drops leading zeros (31 bytes). Left-pad or trim to the exact length: copy the low `len` bytes
  into a zero-filled array. Java 8 (run through `jjs`) gave 33 bytes for `2^255 + 1` and 32 for a 248-bit value with its top bit set. The same pad-or-trim logic in Python (no JDK 11+ here to compile a Java version):
  ```python
  def i2osp(x_bytes: bytes, n: int) -> bytes:   # x_bytes = BigInteger.toByteArray() output
      return x_bytes[-n:].rjust(n, bytes(1))     # trim a leading sign byte, pad short values
  assert i2osp(bytes(1) + bytes([255]) * 32, 32) == bytes([255]) * 32
  assert i2osp(bytes([18]) * 31, 32) == bytes(1) + bytes([18]) * 31
  ```
- **Python** `x.to_bytes((x.bit_length()+7)//8, "big")` strips zeros (a value with two leading zero bytes gave 30 bytes);
  use the fixed length: `x.to_bytes(32, "big")` (32 bytes, checked).
- **Go** `big.Int.Bytes()` strips zeros (2 bytes for `0x00001201`); use `FillBytes(make([]byte, 32))` (32 bytes, checked).
- **JS** BigInt hex conversion drops leading zeros (`0x00ffn.toString(16)` is `"ff"`); `padStart(64, "0")` (checked).
- ECDSA raw r||s signatures (JWS, WebCrypto) are fixed 2 x 32 bytes for P-256; DER uses minimal signed integers.
  In 5000 P-256 signatures `r` fitted in 31 bytes or fewer 0.5% of the time (about 1 in 256 per integer, so roughly 1 in
  128 signatures has a short `r` or `s`), which looks like flaky tests when a converter strips zeros.
- Little-endian exceptions: X25519/Ed25519 keys and scalars, ChaCha/Poly1305 internals.

## Verify
- [ ] Property test with values having leading zero bytes (e.g. force r < 2^248) across both implementations.
