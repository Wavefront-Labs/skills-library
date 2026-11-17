---
id: computing-software.software-engineering.python.secrets-module-tokens-and-randomness
name: secrets-module-tokens-and-randomness
category: computing-software
field: software-engineering
product: python
tags: [python, py-security, secrets-module, secrets, token-urlsafe, csprng, os-urandom, random-vs-secrets, password-generation]
level: practitioner
status: docs-checked
description: "Generate tokens, passwords, API keys and nonces with the secrets module and os.urandom; never use random for security; compare secrets in constant time."
sources: ["https://docs.python.org/3/library/secrets.html", "https://docs.python.org/3/library/random.html#random.SystemRandom"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# secrets module: tokens and randomness

`random` is designed for modelling and simulation, not security, and is **never** appropriate for secrets. Use `secrets`, which provides the most secure source of randomness your operating system offers.

```python
import secrets, string

secrets.token_bytes(32)                 # 256-bit raw key material
secrets.token_hex(16)                   # 32 hex chars, e.g. session id
secrets.token_urlsafe(32)               # URL-safe text, about 1.3 chars per byte: reset links, API keys
secrets.randbelow(10**6)                # unbiased integer in [0, 10**6): OTP digits
f"{secrets.randbelow(10**6):06d}"       # 6-digit code, zero padded

alphabet = string.ascii_letters + string.digits
"".join(secrets.choice(alphabet) for _ in range(20))     # random password

secrets.compare_digest(a, b)            # constant-time comparison for tokens/MACs
secrets.SystemRandom().shuffle(items)   # shuffle with the OS RNG
```

## How much entropy
As of 2015 the docs say 32 bytes (256 bits) is believed sufficient for typical use. `DEFAULT_ENTROPY` is subject to change at any time, including in maintenance releases, so pass an explicit size.

## Lifecycle
- Give tokens expiry and single use; log token IDs, not values.
- Do not derive tokens from user data and a timestamp; generate them with `secrets`.

## Gotchas
- Modulo bias: `os.urandom(1)[0] % 10` is biased; use `randbelow`.
- `secrets.compare_digest` compares in constant time (see `hmac.compare_digest`).

## Verify
- [ ] A test asserts token length/charset and that two tokens differ.

## Checked

- 2026-11-03: checked against the CPython docs `library/secrets.rst`: purpose versus `random`, OS randomness source, `token_bytes`/`token_hex`/`token_urlsafe`, `randbelow`, `choice`, `compare_digest`, `SystemRandom`, 32-byte guidance, `DEFAULT_ENTROPY` may change.
- Removed: Mersenne Twister prediction claim, getrandom/BCryptGenRandom names, hashing of stored tokens, uuid and seeding remarks, fork and early-boot notes, ruff rule.

Method: documentation only; no commands were run.
