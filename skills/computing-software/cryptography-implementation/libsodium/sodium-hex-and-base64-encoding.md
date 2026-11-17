---
id: computing-software.cryptography-implementation.libsodium.sodium-hex-and-base64-encoding
name: sodium-hex-and-base64-encoding
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, sodium-helpers, sodium-bin2base64, sodium-bin2hex, sodium-base642bin, constant-time-encoding, url-safe-base64]
level: practitioner
status: docs-checked
description: "Encode keys and ciphertexts with libsodium's constant-time sodium_bin2hex/bin2base64 and decoders: the four base64 variants, buffer sizing macros, and ignore/strict parsing."
sources: ["https://doc.libsodium.org/helpers", "https://github.com/jedisct1/libsodium.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hex and base64 encoding in libsodium

`sodium_bin2hex` and `sodium_hex2bin` are documented to evaluate in constant time for a given size, which matters when the data is a secret key. The docs make no such statement for the base64 functions, so check before encoding secrets with them.

## Hex

```c
char hex[crypto_secretbox_KEYBYTES * 2 + 1];
sodium_bin2hex(hex, sizeof hex, key, sizeof key);
size_t binlen; const char *end;
if (sodium_hex2bin(key, sizeof key, hex, strlen(hex), ":", &binlen, &end) != 0
    || binlen != sizeof key) { /* reject */ }
```

`ignore` (here `":"`) lists characters to skip, e.g. for `aa:bb:cc`. Pass
NULL for strict parsing. Always check `binlen` equals the expected key size.

## Base64: pick a variant explicitly

| Variant constant | Alphabet | Padding |
|---|---|---|
| `sodium_base64_VARIANT_ORIGINAL` | `+/` | `=` |
| `sodium_base64_VARIANT_ORIGINAL_NO_PADDING` | `+/` | none |
| `sodium_base64_VARIANT_URLSAFE` | `-_` | `=` |
| `sodium_base64_VARIANT_URLSAFE_NO_PADDING` | `-_` | none (JWT-style) |

```c
size_t b64max = sodium_base64_ENCODED_LEN(sizeof ct, sodium_base64_VARIANT_URLSAFE_NO_PADDING);
char *b64 = malloc(b64max);
sodium_bin2base64(b64, b64max, ct, sizeof ct, sodium_base64_VARIANT_URLSAFE_NO_PADDING);
if (sodium_base642bin(buf, buflen, b64, strlen(b64), NULL, &binlen, NULL,
                      sodium_base64_VARIANT_URLSAFE_NO_PADDING) != 0) { /* invalid */ }
```

- The variant must match on both sides; agree it in the protocol spec. `sodium_base642bin` accepts an `ignore` set (typically whitespace and newlines) and returns -1 when more than `bin_maxlen` bytes would be needed or the string cannot be fully parsed and no `b64_end` pointer was given.
- `sodium_base64_ENCODED_LEN` includes the trailing NUL.
- libsodium.js: `sodium.to_base64(bytes, sodium.base64_variants.URLSAFE_NO_PADDING)`
  (its default is `URLSAFE_NO_PADDING`, per the libsodium.js README); the `sodium_base64_VARIANT_*` macros have no associated symbols, so bindings define their own.

## Verify

- [ ] Every decode checks the return value and decoded length.
- [ ] Variant documented and identical on all sides (test with a value containing bytes 0xfb/0xff, which produce `+/` vs `-_`).
- [ ] Secret material uses libsodium's constant-time hex helpers where timing matters.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: sodium_bin2hex minimum buffer of bin_len*2+1 and constant time, sodium_hex2bin ignore set and NULL for strict parsing and return values, the four base64 variant constants, sodium_base64_ENCODED_LEN including the trailing NUL, sodium_base642bin signature and return values, libsodium.js default variant. The base64 alphabet and padding columns follow the standard definitions of the four variant names. Removed claims that the base64 functions are constant time, that the decoder rejects other variants, and the Node default.

Method: documentation only; no commands were run.
