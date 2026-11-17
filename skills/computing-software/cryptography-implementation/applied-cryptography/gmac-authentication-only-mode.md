---
id: computing-software.cryptography-implementation.applied-cryptography.gmac-authentication-only-mode
name: gmac-authentication-only-mode
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, gmac, gcm, sp-800-38d, mac, authentication-only]
level: advanced
status: docs-checked
description: "Use GMAC (GCM with empty plaintext, SP 800-38D) for authentication-only data: unique IV requirement, tag length, and when HMAC or CMAC is the safer choice."
sources: ["https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GMAC authentication-only mode

GMAC is GCM applied only to authenticated data: the plaintext is empty and all input is AAD. SP 800-38D says
statements about GCM also apply to GMAC, so it inherits GCM's fragility.

## Rules
- The IV must be unique per key, exactly as for GCM. SP 800-38D: if IVs repeat for a given key, an adversary is
  likely to determine the hash subkey from the outputs and can then construct forgeries. This is the main
  difference from HMAC/CMAC, which are deterministic and need no IV.
- SP 800-38D recommends restricting support to 96-bit IVs. For random IVs, the total number of invocations under
  one key is limited (to 2^32 in the standard's random-IV construction); a counter-based deterministic construction
  avoids that limit.
- Use the full 128-bit tag where you can. Tags of 64 or 32 bits are only for applications that meet the guidance in
  SP 800-38D Appendix C (requirements for short tags).
- Send the IV with the tag; the verifier recomputes and compares in constant time.

## Using a GCM API
Call GCM encryption with empty plaintext and the message as AAD; the tag is the GMAC.

## When to choose something else
- No reliable unique-IV source, or keys shared across many senders: use HMAC-SHA-256 or AES-CMAC.
- Need a deterministic MAC (lookup keys, idempotency tokens): HMAC.

## Verify
- [ ] IV generation reviewed for uniqueness (counter, or random IVs within the standard's invocation limit).
- [ ] A GCM test vector with empty plaintext reproduces.

## Checked
2026-11-01. Confirmed in SP 800-38D (GMAC as GCM on non-encrypted data, statements apply to GMAC; IV uniqueness
and the hash-subkey/forgery consequence; 96-bit IV recommendation; 2^32 random-IV invocation bound; short tags and
Appendix C). Removed: the OpenSSL command and parameter names, and the MACsec/IPsec usage claim.
Method: documentation only; no commands were run.
