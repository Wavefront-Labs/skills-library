---
id: computing-software.digital-privacy-hygiene.password-hygiene.avoiding-predictable-password-patterns
name: avoiding-predictable-password-patterns
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, password-patterns, password-strength, password-length]
level: practitioner
status: draft
description: "Recognise the human password patterns crackers try first: keyboard walks, season-year, name-plus-symbol and leetspeak, and why random generation beats tweaks."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://hashcat.net/wiki/doku.php?id=rule_based_attack"
  - "https://github.com/dropbox/zxcvbn"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Avoiding predictable password patterns

**Goal:** understand why "complex-looking" human passwords fall in minutes, so you stop making them.

## Patterns cracking tools try first
| Pattern | Examples | How it's cracked |
|---|---|---|
| Keyboard walks | `qwerty123`, `1qaz2wsx`, `zxcvbnm,./` | Walk wordlists |
| Season/month + year | `Summer2026!`, `October26` | Mask attacks `?u?l?l?l?l?l?d?d?d?d?s` |
| Name/pet/team + digits + symbol | `Bella2019!` | Wordlist + rules (append digits/symbol) |
| Leetspeak | `P@ssw0rd`, `S3cur1ty` | Substitution rules in hashcat/John |
| Incrementing old password | `Spring2025!` > `Summer2025!` | Rules on breached previous password |
| Site name inside | `Amazon#Bella19` | Targeted rules once one is leaked |
| Phrases from songs/quotes | `tobeornottobe` | Phrase lists |

Attackers start from billions of breached passwords and apply rules; anything a human transforms is in range.

## What to do instead
- Generate: random 16-20+ characters for sites (password manager), diceware 6 words for things you type.
- Never derive passwords from a base with a site-specific tweak.
- Check candidates against breach lists (Pwned Passwords) and zxcvbn-style estimators.

## When a site forces rules
Generate randomly with the required classes; don't hand-edit.

## Gotchas
- Length requirements met by repetition (`aaaaaaaaaaaa1!`) score high on naive meters and fail instantly.
- NIST SP 800-63B-4 tells verifiers to block commonly used, expected or compromised values; many sites don't.
