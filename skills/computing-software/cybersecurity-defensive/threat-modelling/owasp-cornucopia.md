---
id: computing-software.cybersecurity-defensive.threat-modelling.owasp-cornucopia
name: owasp-cornucopia
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [cornucopia, owasp-cornucopia, threat-modelling-game, elevation-of-privilege, gamified-threat-modelling]
level: practitioner
status: docs-checked
description: "Run an OWASP Cornucopia card session with developers: deck suits, dealing, scoring, and turning the threats players find into tracked requirements."
sources: ["https://owasp.org/www-project-cornucopia/", "https://cornucopia.owasp.org/", "https://github.com/adamshostack/eop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OWASP Cornucopia sessions

Cornucopia is a card game that gets developers to find threats in their own design. The project provides decks for website
apps and mobile apps (printable, online cards and an online game), and its related-standards list includes ASVS and
MASVS. Follow the rules and suit list printed with the edition you use.
Elevation of Privilege (EoP), created by Adam Shostack at Microsoft, is a similar card game.

## Running a session (timeboxed)
1. **Prep**: a current DFD or architecture sketch on the wall; 4-6 players who build the system plus a
   facilitator and a scribe; printed deck or the online version. Remove a suit only if everyone agrees the
   area is absent.
2. **Deal** all cards. Play in tricks: a player leads, others follow suit if they can.
3. When playing a card, the player either **explains how that threat applies to this system** (scores a
   point) or plays it without a claim. Use the scoring rules that come with your deck.
4. The scribe records every claimed threat: card id, component, how it would happen, and agreed status
   (already mitigated / needs work / not applicable with reason).
5. Stop at the timebox even with cards left; points are motivation, not the deliverable.

## After the game
- Convert "needs work" threats into backlog items with the card's referenced requirement (for example ASVS) as acceptance criteria.
- Mitigated claims need a pointer to where (code, config, test) so they can be re-checked.
- Repeat with only the suits relevant to a change (e.g. authentication when adding SSO).

## Gotchas
- Without a diagram players argue about the system instead of threats.
- Facilitator limits debate to about three minutes per card and parks disputes.
- The cards encode generic web threats; you still need a structured pass (STRIDE per element) for
  architecture-specific risks such as trust boundaries between services.

## Verify
Session output is a list of threats with owners and ticket links, and the ASVS IDs cited appear in the team's
test or review checklist.

## Checked
2026-10-28. Confirmed on owasp.org/projects/cornucopia, cornucopia.owasp.org and the EoP repo: card decks for website and mobile apps, printable, online cards and online game, ASVS and MASVS in related standards, a wild card, EoP created at Microsoft by Adam Shostack. Removed: the named suit list, trump-suit rule, CAPEC reference claim, STRIDE-suit remark and the 60-90 minute figure.
Method: documentation only; no commands were run.
