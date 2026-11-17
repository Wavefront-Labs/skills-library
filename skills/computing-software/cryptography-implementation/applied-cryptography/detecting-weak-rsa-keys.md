---
id: computing-software.cryptography-implementation.applied-cryptography.detecting-weak-rsa-keys
name: detecting-weak-rsa-keys
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, weak-rsa-keys, roca, cve-2017-15361, debian-weak-keys, cve-2008-0166, fermat-factorization, batch-gcd, badkeys, key-audit]
level: practitioner
status: docs-checked
description: "Scan certificates and keys for ROCA, Debian-weak, Fermat-factorable and shared-prime RSA keys using badkeys and shared-factor checks across a key corpus."
sources: ["https://badkeys.info/", "https://factorable.net/", "https://github.com/badkeys/badkeys", "https://badkeys.info/docs/roca.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting weak RSA keys

Valid-looking RSA keys can be factorable because of the generator that made them. The badkeys
service checks public keys for these known vulnerabilities:

| Class | Cause | Notes |
|---|---|---|
| ROCA (CVE-2017-15361) | flaw in the RSA key generation of Infineon chips, found in 2017 by CRoCS at Masaryk University | affected a wide variety of products; Estonia replaced a large number of eID cards |
| Debian OpenSSL (CVE-2008-0166) | historic Debian OpenSSL bug; badkeys found it can also impact ECDSA keys | check against a blocklist |
| Fermat attack (CVE-2022-26320) | RSA keys from printer firmware that Fermat's factorisation breaks trivially | |
| Common prime factor ("Mining Your Ps and Qs", 2012) | poor randomness: public keys sharing nontrivial common factors | factorable.net recovered RSA private keys for 0.50% of TLS hosts and 0.03% of SSH hosts this way; mostly headless embedded devices that generate keys on first boot |
| Small private exponent (Wiener), polynomial RSA keys, keypair/Gitkraken bug (CVE-2021-41117), sparse DSA keys, small ECDSA private keys | various | also in the badkeys list |
| Discouraged practices | DSA keys, small or unusual RSA exponent, small or unusual RSA key size | flagged separately |

## Running badkeys (README)
```
pip3 install badkeys
badkeys --update-bl            # download blocklist data before first use
badkeys test.crt my.key        # files are format-detected
badkeys -ts example.org        # scan TLS (-t) and SSH (-s) hosts
```
- Supports PEM public and private keys (PKCS #1 and #8), X.509 certificates, CSRs and SSH public
  keys. It prints output only for vulnerable keys unless you pass `-a`.
- Exit codes combine as a bitmask: 0 scanned and clean, 1 application error, 2 some input could
  not be scanned, 4 a vulnerable key was found (6 means both 2 and 4).
- Host scanning has limits (for example TLS scanning cannot see multiple certificates on one
  host); the README suggests collecting keys with other tools and scanning them locally.
- Uploading private keys to the web service is discouraged for production keys.

## Shared-factor check across a fleet
Collect every RSA modulus you own or accept and compute greatest common divisors across them
(factorable.net's approach). Any non-trivial common factor means both keys are broken. It
can only find shared primes within the set you collect.

## Response
- Treat a detected key as compromised: replace it and fix the generator (for example device
  firmware or the entropy source).

## Verify
- [ ] A badkeys run (checking the exit code bitmask) is part of key and certificate intake.
- [ ] A shared-factor check runs across the corpus after large enrolment waves.

## Checked
Method: docs-checked 2026-11-09 against badkeys.info (home page vulnerability list), badkeys.info/docs/roca.html, the badkeys GitHub README (install, usage, scanning, exit codes) and the factorable.net home page. Removed unconfirmed details: Debian key counts, device lists for ROCA, fastgcd tool name, openssl-vulnkey and the factorable extended paper and CRoCS paper (not read).
