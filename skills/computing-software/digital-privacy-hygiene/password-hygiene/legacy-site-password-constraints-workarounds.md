---
id: computing-software.digital-privacy-hygiene.password-hygiene.legacy-site-password-constraints-workarounds
name: legacy-site-password-constraints-workarounds
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, length-caps, character-restrictions, forced-rotation, security-questions, banking-password-limits, legacy-systems, password-truncation, special-character-blocklist, pin-only-login]
level: practitioner
status: draft
description: "Get the strongest password a site will actually accept when it caps length, blocks characters, forces rotation, or still uses security questions — and know when it's silently truncating."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Legacy site password constraints and workarounds

**Goal:** many sites — especially banks, government portals and older enterprise
systems — still enforce rules NIST SP 800-63B has explicitly moved away from
(short length caps, forced character sets, periodic rotation, security questions).
Get the actual strongest credential the site will accept, and know which of its
quirks are a real security problem versus just annoying.

## 1. Length caps and silent truncation
- Some systems advertise a max (e.g. "up to 20 characters") — generate exactly
  that length with your manager rather than guessing short.
- The dangerous variant is **silent truncation**: a site accepts a 40-character
  password at signup, truncates it to the first N characters server-side without
  telling you, and still logs you in with the full string on some platforms (if the
  client itself truncates before sending) but not others. Test it directly: after
  setting a long password, try logging in with a deliberately *shortened* version
  of it (first 20 chars only, say). If that also works, the password is truncated
  server-side and your effective entropy is only the first N characters — save
  that shorter string in your manager as the real password, not the long one you
  typed, so you don't lock yourself out guessing which prefix was kept.

## 2. Character set restrictions
- A site that **blocks spaces, blocks certain symbols, or requires a very small
  allowed set** ("letters and numbers only") shrinks the effective character
  space. Compensate with length: generate the maximum allowed length using only
  the allowed classes — a 24-character alphanumeric-only password still clears a
  reasonable entropy bar (section on entropy budgeting:
  `computing-software.digital-privacy-hygiene.password-hygiene.passphrase-construction-and-entropy-budgeting`)
  even without symbols.
- A requirement for **at least one of each class** (upper, lower, digit, symbol)
  is usually satisfied automatically by a manager's generator — just confirm the
  generated password isn't rejected for an unsupported symbol the site secretly
  blocks (quotes, backslash and angle brackets are common silent rejects); if a
  save fails, regenerate rather than hand-editing down to something weaker.

## 3. Forced periodic rotation
- NIST 800-63B now recommends **against** mandatory rotation on a schedule (it
  pushes people toward predictable incremental changes — `Summer2024!` →
  `Summer2025!` — which are easier to guess than no rotation at all), but many
  organisational and banking systems still enforce 60/90-day rotation by policy,
  often for compliance reasons unrelated to current guidance.
- If forced to rotate: generate a fully new random password each time rather than
  incrementing the old one, and save it in the manager immediately — don't reuse
  a password from the site's remembered history, which most rotation policies
  block anyway (and which is also why incrementing a number at the end often fails
  the "too similar to previous" check).

## 4. Security questions
- Treat every security question as **a second password field**, not a factual
  answer: generate a long random string with the manager and store it as a custom
  field against that login, exactly like a password. Real answers to "mother's
  maiden name" or "first pet" are frequently discoverable via social media or
  public records (this is the core criticism NIST's current guidance levels at
  security questions, recommending against them entirely where an alternative
  factor exists).
- Where a site requires a security question as a prerequisite for *registering*
  stronger MFA, treat filling it with a random manager-generated string as a
  stepping stone to getting MFA on, not as the long-term protection.

## 5. PIN-only or 4-digit login (some banking apps)
A banking app that only accepts a 4–6 digit PIN at the app level is usually layered
on top of a much stronger credential elsewhere (device biometric gate, backend
password, out-of-band verification) — the short PIN is a convenience factor for an
already-authenticated device, not the whole defense. Confirm the underlying
account password (used for web login or account recovery) is still a full-strength
manager-generated credential; don't let a short app PIN make you think the account
itself is only as strong as 4 digits.

## Gotchas
- Assuming a long password "worked" at signup is not the same as confirming it
  wasn't truncated — test with a shortened variant if the site's behaviour is
  unclear.
- Forced rotation without a manager turns into predictable incrementing in
  practice — if you can't avoid the policy, at least avoid that pattern.
- Uncertain: which specific major banks/government portals currently truncate or
  cap length changes over time without notice — re-verify per site rather than
  assuming last year's test still holds.

## Verify
- [ ] For any site with an unusual length/character limit, you've generated a
      password at its actual maximum, in the manager, not a hand-shortened guess.
- [ ] You've tested for silent truncation on anything that accepted a long password
      without clearly stating a max.
- [ ] Any security-question answers are random manager-generated strings, not real
      facts.
- [ ] Forced rotations produce a brand-new random password each time, saved
      immediately, never an incremented variant.
