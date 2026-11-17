---
id: computing-software.cryptography-implementation.crypto-libraries.canonical-encoding-and-parsing-safety
name: canonical-encoding-and-parsing-safety
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, base64, hex-encoding, asn1, der, encoding-ambiguity, canonicalization, malleability, parser-safety, signature-encoding, url-safe-base64, padding]
level: advanced
status: verified
description: "Encoding/decoding crypto data safely: base64/hex variant mismatches, non-canonical ASN.1/DER parsing bugs, and why encoding ambiguity creates signature/hash malleability."
sources: ["https://www.rfc-editor.org/rfc/rfc4648", "https://www.rfc-editor.org/rfc/rfc7515", "https://nvd.nist.gov/vuln/detail/CVE-2022-3602", "https://nvd.nist.gov/vuln/detail/CVE-2022-3786", "https://github.com/openssl/openssl/blob/master/CHANGES.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Canonical encoding and parsing safety for cryptographic data

Cryptographic primitives operate on exact bytes. The bugs in this skill are
not in the primitives — they're in the encode/decode layer around them,
where "close enough" parsing silently breaks a security property the
primitive was providing.

## Base64/hex variant mismatches

RFC 4648 defines **two base64 alphabets**: standard
(`+`/`/`) and URL-safe (`-`/`_`), and padding with `=` is optional in some uses (JWS drops it).
Mixing them across a system boundary (a token
generated with URL-safe encoding, decoded by a library expecting standard
alphabet) fails loudly if you're lucky (Java 8 `getUrlDecoder()` rejects `+` with `Illegal base64 character 2b`) and silently
accepts two spellings if you're not (Node 24.22 `Buffer.from(s, "base64")` decodes both `-__-` and `+//+` to the same bytes; Python
`b64decode` without `validate=True` silently drops stray characters; Go's `StdEncoding` ignores newlines and accepts non-zero
trailing bits, so `"YQ=="` and `"YR=="` both decode to `a`, as in Python). Pick one variant per interface and
document it; when interoperating with an external system (JWT uses
base64url *without* padding, for instance — RFC 7515), match their exact
variant, don't assume.

Hex is unambiguous in alphabet but still has a case-sensitivity trap (`bytes.fromhex("AB") == bytes.fromhex("ab")`, but the
strings differ): constant-time comparison (see
`computing-software.cryptography-implementation.secure-implementation.constant-time-code-and-known-answer-tests`)
must happen on the decoded bytes, never on the hex/base64 *string* — comparing
encoded strings with `==` can be non-constant-time at the string level even
when the underlying byte array comparison function is safe, depending on
language (short-circuiting string comparison is extremely common).

## ASN.1/DER parsing — don't write your own

ASN.1 is the usual encoding for X.509 certificates and raw ECDSA signatures.
It's a flexible, context-dependent format, and hand-rolled or old parsers
have a long history of CVEs:
- **CVE-2022-3602/3786 ("X.509 punycode buffer overflow", OpenSSL 3.0.x):** NVD describes a buffer overrun in X.509 name
  constraint checking triggered by a crafted email address in a certificate (CVE-2022-3602: four attacker-controlled bytes
  overflowed on the stack; CVE-2022-3786: an arbitrary number of bytes containing the `.` character) — a parsing bug in
  security-critical certificate code, not a cryptographic flaw. It needed either a CA-signed malicious certificate or an
  application continuing after a failed path build (NVD text). NVD rates both HIGH.
- **BER vs DER leniency:** BER (Basic Encoding Rules) allows multiple valid
  encodings of the same value (e.g., indefinite-length encoding); DER
  (Distinguished Encoding Rules) mandates exactly one canonical encoding.
  Strict verifiers reject the alternatives: a P-256 ECDSA signature rewritten with a long-form SEQUENCE length (`30 81 44 ...`)
  or an indefinite length failed verification in pyca `cryptography`, `openssl dgst -verify`, Node `crypto.verify` and Go
  `ecdsa.VerifyASN1`, while the DER original verified in all four (run; Go 1.27.3, OpenSSL 3.2.3, Node 24.22). A parser that
  accepts BER where DER is specified (common in "lenient"
  libraries) opens exactly the kind of encoding-ambiguity bug this skill is
  about: two byte strings that decode to the "same" logical value but hash
  or compare differently, or — worse — a verifier and a signer disagreeing
  on what the "real" bytes were.
- **Rule:** always use your platform/library's X.509 and ASN.1 parser
  (OpenSSL, Java's `java.security.cert`, Go's `crypto/x509`, Python's
  `cryptography` package). Never hand-parse ASN.1 structures for anything
  security-relevant, and keep these libraries patched — this is one of the
  highest-CVE-density corners of any crypto stack precisely because parsing
  untrusted structured input is hard.

## Why encoding ambiguity breaks security properties, not just correctness

If two different byte sequences can represent the "same" value under a
lenient decoder, any security property that assumed **one canonical
representation per value** silently breaks:
- A signature over "the DER encoding of X" is only meaningful if encoder and
  verifier agree there's exactly one DER encoding of X — this is why DER
  (not BER) is mandated for signed structures.
- A cache key, dedup check, or allow-list comparison done on an *encoded*
  form instead of the *decoded, canonicalized* value can be bypassed by an
  attacker who finds an alternate encoding of a blocked value that the
  comparison doesn't recognize (a known class of WAF/filter bypass, same
  root cause).
- **General rule:** decode untrusted input to its canonical in-memory form
  first, perform all security checks and comparisons on that canonical
  form, and re-encode canonically if you need to emit it again. Never
  compare or make trust decisions on the raw encoded bytes of
  attacker-influenced input.

## Verify

- [ ] Exactly one base64/hex variant is used per interface boundary, matched
      to what the peer/spec (JWT, PEM, etc.) actually expects.
- [ ] Constant-time comparisons happen on decoded bytes, not on encoded
      strings.
- [ ] No hand-written ASN.1/DER parser anywhere in the codebase; certificate
      and signature parsing goes through a maintained library, kept patched.
- [ ] DER (not lenient BER) is enforced wherever a canonical encoding is
      required for a security decision (signatures, certs).
- [ ] Security-relevant comparisons (allow-lists, dedup, trust decisions)
      happen on canonicalized decoded values, not raw encoded input.

The CVE citations illustrate the bug class in a widely used library; check current advisories for your specific library/version before
relying on "patched" status.
