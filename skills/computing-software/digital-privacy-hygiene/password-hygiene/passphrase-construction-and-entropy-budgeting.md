---
id: computing-software.digital-privacy-hygiene.password-hygiene.passphrase-construction-and-entropy-budgeting
name: passphrase-construction-and-entropy-budgeting
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, entropy, diceware, passphrase, brute-force, guessing-resistance, bits-of-entropy, zxcvbn, password-strength-meters, offline-attack, hash-rate, argon2id, pbkdf2, memorable-password]
level: practitioner
status: draft
description: "Calculate real entropy for passphrases and passwords by hand, pick a word/character count that resists offline cracking, and read strength meters correctly."
sources:
  - "https://www.eff.org/dice"
  - "https://github.com/dropbox/zxcvbn"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Passphrase construction and entropy budgeting

**Goal:** decide how long a password or passphrase needs to be using arithmetic,
not a strength-meter's colour bar, so the choice actually survives an offline
cracking attempt against the kind of hash a breached site is likely to have used.

## 1. What entropy means here
Entropy in bits = log2(number of equally likely choices). A truly random
lowercase-only 8-character password has 8 × log2(26) ≈ 37.6 bits — far weaker than
it looks, because "8 characters" sounds long but the character set is small. A
6-word diceware passphrase from the EFF long wordlist (7,776 words, ~12.9 bits/word)
has 6 × 12.9 ≈ 77.5 bits — far stronger, because the *set of possible words* is much
larger than the set of possible single characters, even though there are fewer units.

## 2. Building a real entropy budget
- **Per-character random** (manager-generated, all classes, truly random): ~6.6
  bits/character (full 95-character keyboard set) to ~5.2 bits/character
  (mixed-case + digits only). A 20-character fully random password: ~105–130 bits.
- **Diceware words**: ~12.9 bits/word (EFF long list, 7,776 words) or ~10.3 bits/
  word (shorter 1,296-word list — use the long list). 5 words ≈ 64.5 bits, 6 words
  ≈ 77.5 bits, 7 words ≈ 90 bits.
- **Rule of thumb targets**: ≥ 60 bits for anything protected additionally by MFA
  and a sane rate-limited login; ≥ 80 bits for your password manager's master
  passphrase and anything with no rate limiting or offline-attackable (a file you
  encrypt yourself, a password-protected archive); add headroom because the attacker's
  hash rate, not your comfort, sets the real bar (section 3).

## 3. Why the offline hash matters more than the count
A password's practical strength depends on **what the attacker has to compute
against**, not just its entropy in isolation:
- A **fast, unsalted or weakly-hashed** credential store (old MD5/SHA1 breach dumps)
  lets an attacker try billions of guesses per second on commodity GPUs — only high
  entropy (80+ bits) meaningfully resists this.
- A properly built modern store (**Argon2id**, or bcrypt/scrypt/PBKDF2 with a high
  work factor) deliberately slows each guess to milliseconds, so even 50–60 bits can
  hold for a long time against a realistic attacker budget.
- You usually don't know which kind of hash a site used until after a breach — this
  is the actual argument for NIST SP 800-63B's "length over complexity" guidance
  (see `computing-software.digital-privacy-hygiene.password-hygiene.account-security-audit-and-breach-response`):
  pad the budget rather than assume the site protected you.

## 4. Building a memorable high-entropy passphrase by hand (no generator available)
1. Roll physical dice (5 rolls → one EFF long-list word) or use a dice-roll app you
   trust, 5–7 times.
2. Write the words with a separator (hyphens are fine; a separator doesn't add
   meaningful entropy against a targeted attacker but helps typing accuracy).
3. Do **not** add a "clever" substitution (`0` for `o`, a leading capital, a
   trailing `!`) expecting it to raise entropy — common substitution patterns are
   explicitly modeled by cracking tools (e.g. in Hashcat/John the Ripper rule sets)
   and add only a few bits at best, while making the passphrase harder to type and
   recall. Four or five truly random words beat four words plus leetspeak tricks.
4. Never pick words that are personally meaningful and guessable from your social
   media (pet names, birth years, street names) — diceware's security model depends
   on the words being randomly selected, not chosen for memorability.

## 5. Reading strength meters correctly
Meters like **zxcvbn** (used in many browsers and signup forms) estimate guessing
difficulty using dictionaries of real breached passwords, common patterns and
keyboard walks — they are far more realistic than a naive "has a symbol?" check,
but a green bar on one site's meter doesn't transfer to a guarantee elsewhere.
Treat a meter as a floor check, not your actual entropy calculation; do the
arithmetic above for anything high-value (vault master passphrase, full-disk
encryption passphrase).

## Gotchas
- A long passphrase made of a few common phrases ("to be or not to be") has far
  less real entropy than word-count arithmetic suggests — phrase-level dictionaries
  exist too.
- Entropy math assumes a uniformly random selection process; a human "randomly"
  picking words from memory is measurably less random than dice.
- Uncertain: effective modern GPU guess rates against well-salted Argon2id vary by
  configured memory/time cost and hardware generation — treat the 60/80-bit
  thresholds above as planning guidance, not a guarantee, and re-check current
  benchmarks periodically.

## Verify
- [ ] You can compute the bits-of-entropy for any password/passphrase scheme you
      propose, not just describe it as "strong."
- [ ] Vault master passphrase and full-disk encryption passphrase both clear ~80 bits.
- [ ] No personally-guessable words or "clever" substitutions used in place of real
      length/randomness.
- [ ] You know whether the account you're protecting is rate-limited/well-hashed or
      not, and budgeted accordingly.
