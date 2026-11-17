---
id: computing-software.cryptography-implementation.crypto-libraries.python-secrets-module-and-compare-digest
name: python-secrets-module-and-compare-digest
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, python-secrets, python, secrets-module, compare-digest, csprng, tokens]
level: intro
status: verified
description: "Use Python's secrets module for tokens and hmac.compare_digest for comparisons: token_bytes, token_urlsafe sizing, choice for passwords, and replacing the random module."
sources: ["https://docs.python.org/3/library/secrets.html", "https://docs.python.org/3/library/hmac.html#hmac.compare_digest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python secrets module and compare_digest

## Tokens
```python
import secrets
secrets.token_bytes(32)        # raw key material
secrets.token_hex(16)          # 32 hex chars, 128 bits
secrets.token_urlsafe(32)      # ~43 chars, 256 bits, for URLs and reset links
secrets.randbelow(10**6)       # unbiased integer in [0, 10**6)
```
- Size by entropy: 128 bits minimum for unguessable tokens, 256 bits for long-lived keys.
- Default `token_*()` with no argument uses 32 bytes today (subject to change): `token_bytes()` is 32 bytes, `token_hex()` 64 chars, `token_urlsafe()` 43 chars (checked); pass sizes explicitly.

## Passwords and passphrases
```python
import string
alphabet = string.ascii_letters + string.digits
pw = "".join(secrets.choice(alphabet) for _ in range(20))
```

## Never use random for security
`random` is a Mersenne Twister: predictable after 624 outputs. Flag `random.random`, `random.choice`,
`random.randint`, `uuid.uuid1` in security contexts. `uuid.uuid4()` uses `os.urandom` and is acceptable as an
identifier but not a substitute for a sized token.

## Comparisons
```python
import hmac
if not hmac.compare_digest(received_sig, expected_sig):   # bytes or ASCII str
    raise PermissionError
```
- Constant time for equal-length inputs; lengths may leak (fine for fixed-size tags).
- `secrets.compare_digest` is an alias.
- Comparing non-ASCII `str` raises TypeError, and so does mixing `str` and `bytes`; encode first. Different lengths return `False`.

## Verify
- [ ] Bandit B311 (random) has no findings in auth code (checked: bandit reports `random.random`, `random.choice` and `random.randint` as B311 and does not flag `secrets.choice`); tests cover compare_digest paths.
