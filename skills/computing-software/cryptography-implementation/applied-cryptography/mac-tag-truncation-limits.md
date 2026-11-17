---
id: computing-software.cryptography-implementation.applied-cryptography.mac-tag-truncation-limits
name: mac-tag-truncation-limits
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, message-authentication-code, mac-truncation, hmac, truncated-tags, forgery-probability, sp-800-107]
level: advanced
status: docs-checked
description: "Decide how short a MAC tag may be: forgery odds per attempt, the RFC 2104 and RFC 4868 truncation guidance, budgeting verification attempts, and safe truncation rules."
sources: ["https://www.rfc-editor.org/rfc/rfc2104#section-5", "https://www.rfc-editor.org/rfc/rfc4868"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAC tag truncation limits

Truncating a MAC tag to t bits gives an attacker a `2^-t` chance per forged
attempt. That is the whole security story for a good MAC, so the question
is how many attempts the attacker gets.

## Minimums from the sources

- RFC 2104 section 5 recommends that the output length t be not less than half
  the length of the hash output (to match the birthday attack bound) and not
  less than 80 bits. Truncation takes the t leftmost bits of the normal HMAC
  result.
- RFC 4868 defines HMAC-SHA-256-128, HMAC-SHA-384-192 and HMAC-SHA-512-256 for
  IPsec: a truncation to half the hash output, alongside untruncated variants.
- For any other MAC or mode (CMAC, GMAC, AEAD tags) take the minimum from that
  algorithm's own specification and do not assume the HMAC rule transfers.

## Choosing t

1. Estimate the attacker's online verification budget N over the key's
   lifetime (requests per second x lifetime, or the cap you enforce).
2. Require `N x 2^-t` well below your risk tolerance.
3. Example: 2^20 attempts per day for 2 years is about 2^30; t = 64 gives
   2^-34 total, t = 32 is unacceptable.

Offline-verifiable tags (anything the attacker can check without you, such
as a MAC used as a password-reset token lookup) must not be truncated much
because N is unbounded.

## Implementation rules

- Truncate by taking the leftmost t bits; verifier recomputes the full tag
  and compares the truncated prefix in constant time.
- Fix t in the protocol; never read the tag length from the message.
- Rate-limit and alert on verification failures, and rotate keys when a
  failure threshold is crossed.

## Verify

- [ ] Tag length is a constant documented with the N x 2^-t calculation.
- [ ] Verification failures are counted and limited per key.

## Checked
2026-11-01. Confirmed in RFC 2104 section 5 (half the hash output, at least 80 bits, leftmost t bits) and RFC 4868
(truncated HMAC-SHA-2 variants, half-length truncation for IPsec). Removed: SP 800-107 and SP 800-38B minimums,
the HMAC-SHA1-96 and GCM statements, and a numeric risk target, none of which these pages state.
Method: documentation only; no commands were run.
