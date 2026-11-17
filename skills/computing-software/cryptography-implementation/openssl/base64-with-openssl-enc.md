---
id: computing-software.cryptography-implementation.openssl.base64-with-openssl-enc
name: base64-with-openssl-enc
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, openssl-base64, base64, openssl-enc, encoding]
level: intro
status: verified
description: "Encode and decode Base64 with openssl enc -a and base64: the -A single-line flag, 64-column wrapping, decoding failures on long lines, and URL-safe variants."
sources: ["https://docs.openssl.org/3.0/man1/openssl-enc/", "https://www.rfc-editor.org/rfc/rfc4648"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Base64 with openssl enc

```sh
openssl base64 -in file.bin -out file.b64          # same as: openssl enc -base64 / -a
openssl base64 -d -in file.b64 -out file.bin
openssl base64 -A -in file.bin                      # single line, no newlines
echo -n 'hello' | openssl base64                    # aGVsbG8=
```

## Line handling (the classic bug)
- Encoding wraps at 64 characters per line.
- Decoding without `-A` is line-oriented: input that does **not end with a newline** (for example `echo -n`, `base64 -w0`
  output or a JWT segment) silently decodes to **zero bytes**, however short it is. Tested on OpenSSL 3.2.3: the same
  data followed by a newline decoded correctly for lines up to at least 668 characters, but a 1336-character line came
  back truncated (232 of 1000 bytes), so very long single lines are also unsafe. Use `-A` when decoding single-line input.
- With `openssl enc -aes-256-cbc -a`, ciphertext saved as one line needs `-A` to decrypt (without it the tool reports
  "error reading input file").

## URL-safe Base64
OpenSSL has no base64url mode. Convert:
```sh
openssl base64 -A -in f | tr '+/' '-_' | tr -d '='
```
Decoding base64url: reverse the `tr`, then re-pad to a multiple of 4 with `=`.

## Alternatives
- GNU `base64 -w0` / `base64 -d`; macOS `base64 -i f`; both differ in flags.
- In code, use the language's base64 library rather than shelling out.

## Checked
Run with OpenSSL 3.2.3 on 2026-10-18: `openssl base64` output wraps at 64 characters per line; `-d -A` round-trips a one-line encoding byte for byte; `echo -n hello | openssl base64` gives `aGVsbG8=`; the `tr` pipeline gives URL-safe unpadded output; decoding behaviour without `-A` is as described in the line-handling section (measured, not from documentation; earlier drafts of this skill said 76 characters, which was wrong).

## Verify
- [ ] Round-trip test: `cmp file.bin <(openssl base64 -A -in file.bin | openssl base64 -d -A)`.
