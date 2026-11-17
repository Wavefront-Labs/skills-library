---
id: computing-software.cryptography-implementation.applied-cryptography.finite-field-dh-safe-groups
name: finite-field-dh-safe-groups
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-agreement, ffdhe, rfc7919, diffie-hellman, logjam, safe-prime, dhparam, modp-groups, sp-800-56a]
level: advanced
status: docs-checked
description: "Use finite-field Diffie-Hellman safely when ECDH is not an option: RFC 7919 FFDHE named groups, safe primes, peer value range checks and avoiding custom dhparams."
sources: ["https://datatracker.ietf.org/doc/html/rfc7919"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finite-field Diffie-Hellman with safe groups

Prefer elliptic-curve Diffie-Hellman. Use finite-field DH (FFDH) only for interop with TLS 1.2 `DHE_*` suites and
legacy protocols.

## Use named groups, not generated parameters

- **RFC 7919 FFDHE** groups ffdhe2048, ffdhe3072, ffdhe4096, ffdhe6144 and ffdhe8192 (TLS `supported_groups` values
  256 to 260): the primes are all safe primes (p is prime and q = (p-1)/2 is also prime) and the generator is
  g = 2. A client names the groups it accepts, so both peers know the modulus is a safe prime.
- Do not accept or generate arbitrary custom primes: with an unknown group the peer cannot cheaply establish that
  the modulus is a safe prime. Copy a standard group instead of freshly generating one.
- For a custom group offered by a non-compatible server, RFC 7919 says a client must reject a prime shorter than
  768 bits and should reject one shorter than 1024 bits; set your own floor well above that.

## Peer value checks

RFC 7919 section 5.1: peers must validate each other's public value Y by ensuring 1 < Y < p-1. This rules out 0, 1
and p-1 and stops the remote peer forcing the local system into the 2-element subgroup. A server must also check
1 < dh_Yc < dh_p - 1 on the ClientKeyExchange and abort with a fatal `handshake_failure` alert if it fails. Many
hand-written DH codes skip the range check; a peer sending Y = 1 makes the shared secret 1.

## Verify

- [ ] Parameters are a named standard group, not a custom prime.
- [ ] No DH group below your policy's minimum size is accepted.
- [ ] Peer public values are range-checked (1 < Y < p-1).
- [ ] ECDHE is preferred over DHE in negotiation order.

## Checked
2026-11-01. Confirmed in RFC 7919 (named FFDHE groups and codepoints, safe primes, g = 2, section 5.1 peer key
check, ClientKeyExchange range check and alert, minimum prime guidance for clients). Removed: RFC 3526 groups,
Logjam and weakdh statements, SP 800-56A approval, strength and speed figures, and the nginx, OpenSSL and sshd
configuration snippets, none of which RFC 7919 states.
Method: documentation only; no commands were run.
