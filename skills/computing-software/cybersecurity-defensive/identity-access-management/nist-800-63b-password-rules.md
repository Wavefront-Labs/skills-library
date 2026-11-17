---
id: computing-software.cybersecurity-defensive.identity-access-management.nist-800-63b-password-rules
name: nist-800-63b-password-rules
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [password-policy, nist-800-63b, memorized-secrets, password-length, password-expiry, password-composition-rules, fine-grained-password-policy, passphrases]
level: practitioner
status: docs-checked
description: "Apply NIST SP 800-63B-4 password rules: length over complexity, no forced periodic changes, blocklist checks, rate limiting and salted hashing."
sources: ["https://pages.nist.gov/800-63-4/sp800-63b.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIST SP 800-63B password rules

**Goal:** a password policy that makes guessing and reuse attacks harder without driving users
to predictable patterns.

## The rules (800-63B-4, password verifiers)
- **Length**: passwords used as a single-factor mechanism must be at least 15 characters. Passwords
  used only as part of multi-factor authentication may be shorter, but at least 8 characters.
- **Maximum length**: verifiers should permit at least 64 characters.
- **Character set**: should accept all printing ASCII and the space character, and should accept
  Unicode (each code point counts as one character). If Unicode is accepted, apply NFC
  normalisation before hashing.
- **No composition rules**: verifiers must not require mixtures of character types.
- **No periodic forced changes**: must not require periodic change, but must force a change when
  there is evidence the authenticator is compromised.
- **Blocklist**: when a password is set or changed, compare the whole prospective password against
  a blocklist of commonly used, expected or compromised values. If it matches, require a different
  one and give the reason. Substrings and embedded words are not what is compared. An excessively
  large blocklist gives little extra benefit because online guessing is already throttled.
- **Guidance**: offer guidance for choosing a strong password, especially after a blocklist
  rejection, to discourage trivial modifications of listed passwords.
- **No hints or knowledge-based questions**: must not let a subscriber store a hint visible to an
  unauthenticated claimant, and must not prompt for KBA or security questions when choosing passwords.
- **Whole password**: request and verify the full password; never truncate.
- **Copy and paste**: the usability guidance says to support paste in password fields, including
  passphrases (helps password managers).
- **Rate limit**: limit consecutive failed attempts on one authenticator of one account to no more
  than 100 by disabling that authenticator (an upper bound; lower limits may be imposed). Optional
  techniques to reduce attacker-driven lockout: bot-detection challenge, increasing waits (for
  example 30 seconds up to an hour) and risk-based checks. After a successful sign-in the verifier
  should disregard earlier failures.
- **Storage**: salted and hashed; the salt must be at least 32 bits and chosen to avoid collisions
  between accounts, and a reference to the hashing scheme and cost factor should be stored.

## Gotchas
- Dropping expiry without adding a blocklist and rate limiting removes protection; apply the
  rules together.
- Audit regimes you are held to may still demand rotation or other rules; document the alignment
  or compensating controls.
- Long maximum lengths break some legacy applications with their own limits; find them first.

## Checked
Method: docs-checked 2026-11-09 against NIST SP 800-63B-4 (pages.nist.gov/800-63-4/sp800-63b.html), sections on password verifiers, rate limiting, salted storage and usability guidance, read from a downloaded copy.
Removed as unconfirmed: the Active Directory and Entra ID configuration sections (lengths, PSO values, lockout numbers, the Update-MgDomain command, Password Protection behaviour), the claim that Rev. 4 strengthened several items to "shall", the sample test passwords, and the Microsoft 365 and CIS sources, which were not read.
