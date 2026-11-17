---
id: computing-software.cryptography-implementation.protocol-implementation.jwe-encryption-algorithms
name: jwe-encryption-algorithms
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, jwt, jose, jwe, rfc7516, rfc7518, ecdh-es, rsa-oaep-256, a256gcm, nested-jwt, compression-dos]
level: advanced
status: docs-checked
description: "Choose and validate JWE algorithms: ECDH-ES, RSA-OAEP-256, A256KW, dir with A256GCM; reject RSA1_5 and uncapped PBES2, limit zip, nest JWS for origin."
sources: ["https://datatracker.ietf.org/doc/html/rfc7516", "https://datatracker.ietf.org/doc/html/rfc7518#section-4", "https://datatracker.ietf.org/doc/html/rfc8725", "https://www.iana.org/assignments/jose/jose.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWE encryption algorithms

JWE (RFC 7516) encrypts a payload with a content encryption key (CEK) using
`enc`, and protects the CEK with `alg`. Both come from the token header, so
the recipient must allowlist them.

## Key management (`alg`)

| alg | Use | Notes |
|---|---|---|
| `ECDH-ES` / `ECDH-ES+A256KW` | encrypt to an EC public key | Preferred asymmetric option; validate the ephemeral key point: RFC 8725 reports that several JOSE libraries failed to validate ECDH-ES inputs, allowing invalid-curve key recovery |
| `RSA-OAEP-256` | encrypt to RSA keys | OAEP with SHA-256 and MGF1 with SHA-256 (IANA: Optional) |
| `RSA-OAEP` | legacy | RFC 7518 default parameters are SHA-1 with MGF1 SHA-1; prefer -256 |
| `RSA1_5` | **reject** | RSAES-PKCS1-v1_5; RFC 8725 says avoid all RSA-PKCS1 v1.5 encryption and prefer RSAES-OAEP |
| `A256KW`, `A256GCMKW` | shared symmetric wrapping key | |
| `dir` | CEK is the shared key directly | Simple; one key for all tokens |
| `PBES2-HS512+A256KW` | password-based | `p2c` (iteration count) is a header value the sender sets, so an attacker can make you do excessive work: reject, or cap it |

## Content encryption (`enc`)

`A256GCM` (or `A128GCM`), both Recommended in the IANA registry. `A128CBC-HS256` and `A256CBC-HS512` are the
AES-CBC with HMAC-SHA-2 options; the registry marks them Required, but GCM is simpler.

## Validation rules

- Allowlist exact `alg`+`enc` pairs per recipient key; reject everything else
  before doing any crypto.
- Bind the key to the algorithm (an RSA key is used only with RSA-OAEP-256).
- `zip: DEF` (DEFLATE compression): cap decompressed size or reject `zip` entirely (decompression bombs).
  RFC 8725 also says compression SHOULD NOT be done before encryption, because compressed data often reveals
  information about the plaintext.
- Use `kid` for key lookup only among configured keys.
- Decryption errors: one generic error.

## Nested JWT (sign then encrypt)

JWE alone does not authenticate the sender for asymmetric `alg`s: anyone
with the recipient's public key can encrypt. For tokens that need both
confidentiality and origin authenticity, sign (JWS) then encrypt (JWE, with `cty` set to describe the inner content, RFC 7516 4.1.12), and verify the
inner JWS after decrypting. RFC 8725 notes that some libraries do not validate the inner signature, requires
all outer and inner operations to be validated with application-supplied keys and algorithms, and requires an
explicit `typ` in the inner JWT when explicit typing is used.

## Verify

- [ ] Allowlists configured in the library call (not just documented).
- [ ] `RSA1_5`, uncapped `PBES2`, and unexpected `zip` rejected in tests.
- [ ] Sender authenticity provided by nested JWS where required.

## Checked
Date: 2026-10-31. Confirmed in the IANA JOSE registry (algorithm names, usage levels, `zip` DEF), RFC 7518 (RSA-OAEP
SHA-1 defaults, RSA-OAEP-256, PBES2 and `p2c`), RFC 7516 (`zip`, `cty`) and RFC 8725 (avoid RSA1_5, ECDH-ES invalid
curve finding, no compression before encryption, nested JWT validation). Removed: the P-256/X25519 curve list, the
2017 date, the Bleichenbacher attribution and the `jose` JavaScript snippet (library API not checked).
Method: documentation only; no commands were run.
