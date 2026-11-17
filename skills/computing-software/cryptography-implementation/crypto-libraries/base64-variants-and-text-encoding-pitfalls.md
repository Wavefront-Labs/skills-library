---
id: computing-software.cryptography-implementation.crypto-libraries.base64-variants-and-text-encoding-pitfalls
name: base64-variants-and-text-encoding-pitfalls
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, interoperability, base64-variants, base64url, hex, utf-8, encoding]
level: practitioner
status: verified
description: "Avoid encoding bugs around crypto: standard vs url-safe base64, padding, strict decoding, hex case, UTF-8 vs Latin-1 strings, and hashing text that must be canonical."
sources: ["https://www.rfc-editor.org/rfc/rfc4648", "https://www.rfc-editor.org/rfc/rfc7515#appendix-C", "https://doc.libsodium.org/helpers", "https://openjdk.org/jeps/400"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Base64 and text encoding pitfalls

## Base64 variants (RFC 4648)
| Variant | Alphabet 62/63 | Padding | Used by |
|---|---|---|---|
| standard | `+` `/` | `=` | PEM, MIME, most "base64" APIs |
| url-safe | `-` `_` | often omitted | JWT/JWS/JWK, Fernet (keeps `=`), URLs |
| MIME | standard + line breaks every 76 | `=` | email (PEM proper wraps at 64; RFC 4648 section 3.1) |

API map:
- Python: `base64.b64encode` / `urlsafe_b64encode` (keeps `=`; strip for JOSE).
  `b64decode(s, validate=True)` - without `validate`, non-alphabet chars are silently dropped (`b64decode("YW!Jj")` gave
  `b'abc'`; with `validate=True` it raises `binascii.Error: Only base64 data is allowed`). Missing padding raises
  `Incorrect padding`; extra `=` (`"YQ==="`) is accepted. All checked on Python 3.14.
- JavaScript: `Buffer.from(s, "base64url")`; in Node 24.22 `Buffer.from(s, "base64")` also decodes the URL-safe alphabet (same
  bytes for `-__-` and `+//+`), so it is lenient. `Uint8Array.fromBase64` is `undefined` in Node 24.22 (check your
  runtime before using it in a browser or Node). `atob` is standard-only (`atob("-__-")` throws `InvalidCharacterError`) and
  returns a binary string, not bytes.
- Java: `Base64.getDecoder()` / `getUrlDecoder()` / `getMimeDecoder()`; `.withoutPadding()` on encoders (all run on Java 8 through the `jjs` Nashorn shell, no JDK 11+ here: `getDecoder()` threw `Illegal base64 character 21` for `YW!Jj`, accepted `YQ` without padding, and `getUrlDecoder()` rejected `+` (`Illegal base64 character 2b`); `getMimeDecoder()` silently dropped the bad character and returned `abc`; `getMimeEncoder()` inserts `\r\n` line breaks).
- Go: `base64.StdEncoding`, `URLEncoding`, `RawURLEncoding` (no padding), `RawStdEncoding` (all four run). `StdEncoding`
  ignores newlines and accepts non-zero trailing bits (`"YR=="` decodes to `a`); `.Strict()` rejects them. `RawStdEncoding`
  rejects input that has `=` padding.
- libsodium: `sodium_bin2base64` with `sodium_base64_VARIANT_ORIGINAL`, `_ORIGINAL_NO_PADDING`, `_URLSAFE`,
  `_URLSAFE_NO_PADDING` (names from doc.libsodium.org/helpers).

## Strictness
- Decoders differ on: missing padding, extra padding, whitespace, non-zero trailing bits.
  A lenient decoder means two strings map to the same bytes (`"YQ=="` and `"YR=="` both decode to `a` in Python and Go) - a problem if you compare the
  *encoded* form (cache keys, deduplication, signature checks on the text).
- Compare tokens, MACs and hashes after decoding, in constant time, never as base64 strings.
- For JOSE: base64url, no padding, reject padding and whitespace (RFC 7515).

## Hex
Lowercase vs uppercase hex of the same digest are different strings. Normalise or compare bytes.
`bytes.fromhex` (`fromhex() arg must contain an even number of hexadecimal digits`) and Go `hex.DecodeString`
(`odd length hex string`) reject odd lengths; hand-rolled parsers often do not. `bytes.fromhex("AB") == bytes.fromhex("ab")`
but `"AB" != "ab"`.

## Text to bytes
- Always encode text explicitly as UTF-8 before hashing, HMACing or encrypting
  (`s.encode("utf-8")`, `new TextEncoder().encode(s)`, `getBytes(StandardCharsets.UTF_8)`).
  Java `getBytes()` with no argument uses the platform default (UTF-8 by default since JDK 18, JEP 400; not before: Java 8 here reported `windows-1252`).
- Unicode normalisation: the character e-acute can be one or two code points (in Python `"\u00e9" != "e\u0301"`, and the two are equal after
  `unicodedata.normalize("NFC", ...)`, checked). Normalise (NFC) passwords and
  identifiers before hashing, or the same visible string fails to verify (RFC 8265 PRECIS for passwords).
- Never store ciphertext or keys in a text column via a "string" conversion (`new String(bytes)`);
  invalid UTF-8 sequences are replaced (Java 8: `new String(new byte[]{-1,-2}, "UTF-8")` gave two U+FFFD characters) and data is lost. Encode first.

## Verify
- [ ] Every encode/decode pair names the variant explicitly.
- [ ] Decoders run in strict mode; tests feed padding, whitespace and invalid characters.
- [ ] Hash/MAC inputs built from text use explicit UTF-8 and documented normalisation.
