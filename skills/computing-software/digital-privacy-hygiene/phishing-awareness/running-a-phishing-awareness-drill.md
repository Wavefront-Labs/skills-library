---
id: computing-software.digital-privacy-hygiene.phishing-awareness.running-a-phishing-awareness-drill
name: running-a-phishing-awareness-drill
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, phishing-simulation, security-awareness-training, gophish, tabletop-exercise, click-rate, consent-based-testing, family-security-drill, blameless-followup]
level: practitioner
status: draft
description: "Run a consent-based phishing simulation for a family or small team: build a believable but harmless lure, measure outcomes without shaming anyone, and turn results into targeted coaching."
sources:
  - "https://getgophish.com/"
  - "https://www.ncsc.gov.uk/collection/phishing-scams"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a phishing awareness drill

**Goal:** measure how a household or small team actually responds to a realistic
lure — not how they *think* they'd respond — without deceiving anyone about the
exercise's existence, without real risk to any system, and in a way that produces
useful coaching instead of embarrassment and distrust.

## 1. Get consent for the program, not for each individual test
Tell everyone in advance that **unannounced simulated phishing tests will happen
periodically** as part of normal security practice — this is standard in
professional security-awareness programs (and often a compliance requirement in
regulated workplaces) precisely because advance warning of the *specific* test
defeats its purpose. What you don't do is run covert surveillance beyond the
test itself, or test people who never agreed to the program existing at all
(a spouse, a teenager, a colleague outside your authority) — for a family, this
usually just means a short conversation first: "I'm going to occasionally send
fake scam texts/emails to practice spotting them, is that alright?"

## 2. Build a lure that's realistic but genuinely harmless
- Use a **look-alike but clearly non-malicious domain you control** (not a
  typosquat of a real brand, which risks trademark/abuse complaints and can
  itself get flagged or blocked) — a free tool like **GoPhish** (self-hosted,
  open source) is built for exactly this and tracks opens/clicks/data entry
  without capturing or storing anything real.
- The landing page a click leads to should be an **immediate, friendly
  explanation** ("this was a test — here's what gave it away"), not a fake
  login form that actually captures a password, even in a drill. Capturing real
  credentials, even for training, creates a real secret you now have to protect
  and defeats the "harmless" premise.
- Match realistic pretexts to section 1 of
  `computing-software.digital-privacy-hygiene.phishing-awareness.spotting-and-handling-phishing`
  (urgency, a parcel fee, a shared document) rather than an obviously fake lure —
  the goal is a fair test, not an easy pass.

## 3. What to measure
- **Click rate**: opened the link.
- **Submission rate**: entered anything on a landing page (far more serious than
  a click alone, and the number that actually predicts real-world risk).
- **Report rate**: who recognised it and reported/flagged it, ideally without
  clicking at all — this is the number you actually want to grow over time, more
  than driving click rate to zero (a target of literally 0% clicks forever is
  unrealistic and usually means the lures stopped being realistic).
- Time to report, if you want a more advanced metric — faster organisational
  response to a real phish correlates with faster simulated reporting.

## 4. Follow-up — blameless, specific, immediate
- Anyone who clicked or submitted gets **immediate, private, specific** feedback:
  which red flag was present (section 1 of the companion skill), not a generic
  "be more careful." Shaming someone publicly for failing a drill reliably makes
  people hide future real incidents instead of reporting them — the opposite of
  the goal.
- Anyone who reported it correctly gets **positive reinforcement**, visibly —
  reporting is the behaviour you want reinforced, and it's cheap to praise.
- Track trend over repeated drills (quarterly is a reasonable cadence for a small
  team; twice a year is enough for a household) rather than treating one result
  as a verdict on any individual.

## 5. Scope and limits
- Don't test on systems or accounts outside your own authority — a drill against
  a workplace needs sign-off from whoever actually owns that risk (IT/security
  leadership), not just your own initiative, even with good intentions.
- A drill is a training measurement, not a substitute for the underlying
  controls (MFA, a password manager that won't autofill on a lookalike domain) —
  see `computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`
  and `computing-software.digital-privacy-hygiene.password-managers.vault-setup-sharing-and-recovery`.

## Gotchas
- A typosquat of a real brand (not a domain you own) can trigger abuse reports,
  blocklisting, or legal exposure — build the lure on your own harmless domain.
- Capturing real passwords "just for the drill" turns a training exercise into
  an actual security incident waiting to happen if that data isn't handled
  perfectly — don't collect anything real.
- Uncertain: workplace legal/compliance requirements for running simulated
  phishing on employees vary by jurisdiction and sector — get sign-off from
  whoever owns that risk before running one at work.

## Verify
- [ ] Everyone being tested agreed in advance that an ongoing, unannounced
      testing program exists (not to each specific test).
- [ ] The lure uses a domain you control; no real credentials are captured
      anywhere in the exercise.
- [ ] Click/submission/report rates are tracked over time, not just once.
- [ ] Follow-up for anyone who clicked is private, specific and blameless; anyone
      who reported correctly is positively reinforced.
