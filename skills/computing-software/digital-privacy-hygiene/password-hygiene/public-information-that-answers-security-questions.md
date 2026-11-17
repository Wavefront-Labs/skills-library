---
id: computing-software.digital-privacy-hygiene.password-hygiene.public-information-that-answers-security-questions
name: public-information-that-answers-security-questions
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, security-question-osint, security-questions, knowledge-based-authentication]
level: practitioner
status: draft
description: "Audit which security question answers are public via social media, people-search sites and records, then replace them with random answers."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://ssd.eff.org/module/creating-strong-passwords"
  - "https://www.ftc.gov/business-guidance/blog/2016/03/time-rethink-mandatory-password-changes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Public information that answers security questions

**Goal:** see your security questions the way an account-recovery attacker does, and close the gaps.

## What's findable
| Question | Where attackers find it |
|---|---|
| Mother's maiden name | Obituaries, genealogy sites, Facebook relatives |
| City of birth | People-search sites, LinkedIn, birth announcements |
| High school / mascot | LinkedIn, Facebook, class reunion pages |
| First pet / car | Instagram posts, "share your first car" memes and quizzes |
| Street you grew up on | Voter records, people-search address history |
| Favourite team/food | Public posts |

Social media "get to know me" quizzes harvest exactly these.

## Audit
1. List accounts that still use security questions (bank, carrier, older email, utilities, government).
2. Search your name + relatives on people-search sites and your own social profiles for the answers.
3. Assume every true answer is public.

## Fix
- Replace answers with random strings or random words, stored per account in the password manager.
- Where a phone agent reads the answer, use pronounceable random words ("purple anchor seventeen").
- Remove KBA where the site lets you use MFA instead.
- Limit old posts and profile fields that reveal family, schools, pets.

## Gotchas
- Some sites restrict answer length or characters; generate within the rules.
- Credit bureau and government KBA quizzes draw on credit history, not your answers; freezes and IP PINs help there.
