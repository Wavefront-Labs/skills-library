---
id: computing-software.software-engineering.ruby.ruby-securerandom-digest
name: ruby-securerandom-digest
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, securerandom-digest, security]
level: practitioner
status: docs-checked
description: "Generate tokens with SecureRandom, hash with Digest, sign with OpenSSL::HMAC and compare secrets in constant time."
sources: ["https://docs.ruby-lang.org/en/master/Random/Formatter.html", "https://docs.ruby-lang.org/en/master/Digest.html", "https://docs.ruby-lang.org/en/master/OpenSSL/HMAC.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SecureRandom and Digest

```ruby
require "securerandom"; require "digest"; require "openssl"
SecureRandom.hex(16)          # 32 hex chars, 128 bits
SecureRandom.urlsafe_base64(32)
SecureRandom.uuid             # v4
SecureRandom.random_number(1_000_000)
Digest::SHA256.hexdigest("data")
Digest::SHA256.file("big.iso").hexdigest   # streams the file
mac = OpenSSL::HMAC.hexdigest("SHA256", key, payload)
OpenSSL::KDF.pbkdf2_hmac(pw, salt: salt, iterations: ITERATIONS, length: 32, hash: "sha256")  # ITERATIONS: a current, tuned count
```
Constant-time comparison: `OpenSSL.fixed_length_secure_compare(a, b)` for strings of equal length (added in openssl gem 2.2.0), or `OpenSSL.secure_compare(a, b)` for strings of possibly unequal length (same release). Plain `==` leaks timing.

## Gotchas
- `Kernel#rand`, `Random.rand` and `Random.new(seed)` are predictable; use SecureRandom for anything an attacker must not guess (tokens, reset links, session ids).
- A plain digest such as SHA-256 is not a password hash. Store passwords with a password-hashing KDF such as PBKDF2 (`OpenSSL::KDF.pbkdf2_hmac`) with a per-user salt and a current iteration count.
- Use `OpenSSL.secure_compare` for HMAC strings of unknown length, or check lengths before `fixed_length_secure_compare`.
- `SecureRandom.hex(n)` takes a length in bytes, so the string is `2n` characters.
- Reading a file with `File.read` to digest it loads it all in memory; use `Digest::SHA256.file`.

Verify: `SecureRandom.hex(16).size` is 32.

## Checked
2026-11-03. Confirmed against ruby/ruby `lib/random/formatter.rb` (hex, urlsafe_base64, uuid v4, random_bytes), `ext/digest/lib/digest.rb` (`Digest::SHA256.file`), `ext/openssl/lib/openssl.rb` and `ext/openssl/History.md` (secure_compare, fixed_length_secure_compare added in 2.2.0, OpenSSL::KDF.pbkdf2_hmac keywords). Fixed: the gem version for fixed_length_secure_compare was stated as 3.0+. Removed: Rack::Utils.secure_compare, the PBKDF2 iteration figure, the SHA-256 empty-string vector.
Method: documentation only; no commands were run.
