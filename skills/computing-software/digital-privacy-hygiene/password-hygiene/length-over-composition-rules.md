---
id: computing-software.digital-privacy-hygiene.password-hygiene.length-over-composition-rules
name: length-over-composition-rules
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, password-length, password-strength, unique-passwords, nist-800-63b, composition-rules, passphrase, minimum-length]
level: intro
status: docs-checked
description: "Apply NIST 800-63B-4's password rules for people: length (15+ for single-factor) beats symbols, no forced complexity, no periodic changes, and why P@ssw0rd1! is weak."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Length over composition rules

**Goal:** replace folk rules ("one capital, one number, one symbol, change it every 90
days") with what actually resists guessing.

## What NIST SP 800-63B-4 says (verifier requirements, section 3.1.1)
- Passwords used as the only factor must be at least **15 characters**; passwords used only inside multi-factor
  authentication may be shorter but must be at least 8. Verifiers should permit at least 64 characters.
- **No other composition rules** (such as forced mixtures of character types).
- **No periodic forced changes**; a change is forced on evidence of compromise.
- New passwords are checked against a **blocklist** of commonly used, expected or compromised values (whole password,
  not substrings), with a reason given on rejection.
- Printing ASCII, the space character and Unicode should be accepted; security questions and accessible hints are
  not allowed.
- Password managers and autofill must be allowed, and paste should be permitted.
- Appendix A: additional length and complexity requirements increase frustration and cause counterproductive
  workarounds; blocklists, hashed storage, machine-generated passwords and rate limiting work better.

## Why length wins
Guessing tools run wordlists with rulesets rather than every character combination: the OWASP guidance on brute force
describes attackers starting with dictionary words or slightly modified dictionary words because most people use
those. A "complex" password built from a word plus substitutions (`Password` -> `P@ssw0rd1!`) sits in that space.
Prefer length from unpredictable material over substitutions.

## Personal practice
- Password manager generated: as long as the site allows (a long random value).
- Things you must type or remember (vault, device login, disk encryption): a multi-word random passphrase (see
  `computing-software.digital-privacy-hygiene.password-hygiene.passphrase-construction-and-entropy-budgeting`).
- Sites with silly rules: let the generator satisfy them, then make it longer.

## Verify
- [ ] No memorised password is under 15 characters or built from a word + substitutions.

## Checked
Confirmed 2026-11-08 against NIST SP 800-63B-4 section 3.1.1 and Appendix A, and the OWASP brute-force page
(dictionary and modified dictionary attacks). The CISA page cited before returned HTTP 403 to the fetcher, so it was
dropped from sources and no claim relies on it. Removed: the "20+ random characters" and "5-7 word diceware" figures, which the readable pages do
not state.
Method: docs-only read of cited pages, 2026-11-08
