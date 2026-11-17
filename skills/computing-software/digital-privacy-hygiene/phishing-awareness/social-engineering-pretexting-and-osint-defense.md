---
id: computing-software.digital-privacy-hygiene.phishing-awareness.social-engineering-pretexting-and-osint-defense
name: social-engineering-pretexting-and-osint-defense
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, social-engineering, pretexting, osint, help-desk-fraud, tailgating, physical-pretext, caller-id-spoofing, sim-swap-pretext, insider-reconnaissance, credential-reset-fraud]
level: practitioner
status: draft
description: "Recognise and defend against in-person, phone and help-desk social engineering and the OSINT reconnaissance that sets it up, not just email phishing."
sources:
  - "https://www.ncsc.gov.uk/collection/phishing-scams"
  - "https://www.cisa.gov/topics/cyber-threats-and-advisories/social-engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Social engineering, pretexting and OSINT defense

**Goal:** recognise the social engineering that happens outside a phishing email
entirely — a phone call to a help desk, a stranger at a door, a "survey" that's
really reconnaissance — and know what information you're leaking in public that
makes those attacks easier.

## 1. OSINT reconnaissance — what gets harvested before the approach
Attackers (and legitimate penetration testers running the same playbook) build a
**pretext** from information that's already public:
- **LinkedIn/job postings**: org charts, who reports to whom, internal tool
  names, a recent new-hire ("the new person won't know who's who yet").
- **Social media**: travel plans ("out of office" posts telling an attacker
  exactly when to call impersonating you), pet names and other
  security-question-adjacent facts, a employer badge photo showing a badge
  design that can be replicated.
- **Out-of-office auto-replies**: often reveal exactly who to contact in your
  absence — useful to a legitimate colleague and to an attacker equally.
- **Data broker/people-search sites**: home address, phone number, relatives'
  names — see `computing-software.digital-privacy-hygiene.privacy-configuration.account-privacy-and-tracking-review`
  section 6 for opting out.
The defense here is largely upstream: minimise what's public, and assume anyone
calling or emailing with specific personal details may have gotten them from a
public source, not from genuine insider knowledge.

## 2. Help-desk and support-line pretexting
A common and effective attack: call a company's **own help desk**, claim to be
an employee locked out, and talk the agent into resetting a password or MFA
method — bypassing every technical control by targeting the human process
instead. This has been used in several major breaches (attackers impersonating
employees to IT support to get MFA reset or re-enrolled on an attacker-controlled
device).
- As the person being called: never accept an unsolicited call claiming to be
  IT/support asking you to install something, read back a code, or approve an
  MFA push you didn't request — hang up and call the official support line
  yourself.
- As an organisation/help-desk operator (or just the standard to expect from one
  you trust): a password/MFA reset should require verification through a
  channel independent of the call itself — a callback to a number already on
  file, video verification, or a manager co-sign — never just "answer these
  questions" using facts an attacker could have gathered per section 1.

## 3. In-person pretexting and tailgating
- **Tailgating**: following an authorised person through a secured door,
  often while carrying something (boxes, a tray of coffee) that makes holding
  the door seem like simple courtesy. Defense is procedural, not technical:
  badge everyone in individually, and it's socially fine to ask "who are you
  here to see?" of someone you don't recognise.
- **Pretext visits**: someone claiming to be a courier, inspector, or IT
  contractor to gain physical access or get someone to plug in a device/USB
  drive. Verify unexpected visitors through the company/service they claim to
  represent, independently, before granting access — the same "verify out of
  band" principle as
  `computing-software.digital-privacy-hygiene.phishing-awareness.business-email-compromise-and-invoice-fraud-defense`.
- Never plug in an unknown USB drive, even one "found" in a parking lot or
  handed over by a visitor — a classic drop-attack vector.

## 4. Caller ID spoofing and SIM-swap pretexts
- **Caller ID can be trivially spoofed** to show a bank's real number or a
  known contact — a call *appearing* to come from a trusted number proves
  nothing; verify by calling back on a number you already had, not the one
  that just called you.
- A SIM-swap or port-out attack is itself often preceded by a pretexting call to
  a mobile carrier using OSINT-gathered personal details to pass "identity
  verification" — see the carrier port-out PIN guidance in
  `computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`
  section 5 as the actual technical defense.

## 5. The general tell across every channel
Pretexting works by **borrowing legitimacy** (a real name, a real logo, a
plausible org chart) and pairing it with **urgency or authority** to short-circuit
verification. The countermeasure is the same regardless of channel: verify
through contact information you already had, not anything the approach itself
supplied, and treat "there's no time to check" as itself the signal to check.

## Gotchas
- An attacker who's done real OSINT homework can sound far more convincing than
  the generic "obviously fake" examples used in training — specificity is not
  the same as legitimacy.
- Being professionally polite to an in-person pretext is normal; actually
  granting access or information without verification is the failure point,
  not the politeness itself.
- Uncertain: how much of a given organisation's internal structure is
  discoverable varies hugely by how public-facing its employees' social media
  presence is — a periodic personal OSINT self-check (search your own name,
  check what a LinkedIn profile reveals) is worth doing but has no fixed
  completeness guarantee.

## Verify
- [ ] You know what a search of your own name/employer reveals about your role,
      schedule and reporting line.
- [ ] You would not act on an unsolicited call, even from a number that looks
      right, without an independent callback.
- [ ] You ask unfamiliar people at a secured door who they're there to see,
      rather than assuming legitimacy from appearance alone.
- [ ] You know your own (or your organisation's) actual password/MFA reset
      verification process well enough to recognise if someone tried to bypass it.
