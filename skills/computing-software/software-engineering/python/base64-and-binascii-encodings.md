---
id: computing-software.software-engineering.python.base64-and-binascii-encodings
name: base64-and-binascii-encodings
category: computing-software
field: software-engineering
product: python
tags: [python, py-archives-crypto, base64-binascii, base64, urlsafe-b64, base32, hexlify, binascii, jwt-padding]
level: practitioner
status: docs-checked
description: "Encode and decode base64, URL-safe base64, base32 and hex correctly: padding, validate=True, bytes vs str, JWT-style unpadded input and data-URI usage."
sources: ["https://docs.python.org/3/library/base64.html", "https://docs.python.org/3/library/binascii.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# base64 and binascii encodings

```python
import base64, binascii

raw = b"\xfb\xff\xfe hello"
base64.b64encode(raw)                   # b'+//+IGhlbGxv'  (bytes in, bytes out)
base64.b64encode(raw).decode("ascii")   # str for JSON
base64.urlsafe_b64encode(raw)           # uses '-' and '_' instead of '+' and '/'
base64.b64decode("+//+IGhlbGxv", validate=True)   # validate=True rejects non-alphabet characters
base64.b32encode(b"hi"); base64.b16encode(b"hi")  # Base32 / hex (upper-case)

# JWT / URL tokens omit '=' padding: restore before decoding (3.15 docs: urlsafe_b64decode no longer requires padding)
def b64url_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

data_uri = "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii")
base64.encodebytes(raw)                 # inserts newline every 76 chars (MIME style); usually NOT what you want
```

## Rules
- Base64 is encoding, not encryption or hashing.
- Pick the alphabet by destination: standard for MIME/XML, URL-safe for URLs, filenames, cookies, and JWT.
- Decode strictness: `b64decode` silently discards invalid characters by default; use `validate=True` for untrusted input and catch `binascii.Error`.
- Large payloads: `base64.encode(input, output)` and `decode(input, output)` work on file objects (MIME style, newline every 76 bytes).
- Ascii85 and Base85 are available as `a85encode` and `b85encode`.

## Gotchas
- `b64decode` accepts bytes-like objects or ASCII-only strings.
- Incorrect padding raises `binascii.Error`.
- Never log secrets even encoded; base64 is trivially reversible.

## Verify
- [ ] Round-trip property test: `b64decode(b64encode(x)) == x` for random bytes, lengths 0-10.
- [ ] A test decodes a padding-stripped JWT segment.

## Checked

- 2026-11-03: checked against the CPython docs `library/base64.rst` (main branch): `b64encode`, `b64decode` `validate` and `binascii.Error`, `urlsafe_b64encode`/`decode`, `b32encode`, `b16encode`, `encodebytes` (newline every 76 bytes), `encode`/`decode` file functions, `a85encode`, `b85encode`, ASCII-only string input, `padded` parameter new in 3.15.
- Removed: the ~33% inflation figure, `bytes.hex` advice, chunk-size advice, the `ValueError` and exact error text claims.

Method: documentation only; no commands were run.
