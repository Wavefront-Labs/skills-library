---
id: law-government.platform-and-community-governance.community-governance-design.drafting-a-community-charter-councils-elections-and-amendment-rules
name: drafting-a-community-charter-councils-elections-and-amendment-rules
category: law-government
field: platform-and-community-governance
product: community-governance-design
tags: [platform-and-community-governance, community-governance-design, community-charter, constitution, bylaws, governance-document, online-community, open-source-governance, wikipedia-governance, discord-server, subreddit, forum, dao-governance, council, steering-committee, elections, voting-mechanism, ranked-choice, approval-voting, quorum, supermajority, consensus, lazy-consensus, rfc-process, term-limits, recall, conflict-of-interest, code-of-conduct, amendment-process, benevolent-dictator, bdfl]
level: practitioner
status: draft
description: "Design how an online or open-source community governs itself: charter, decision rights, councils, elections and voting methods, quorum, recall, conduct enforcement and amendment."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drafting a community charter: councils, elections and amendment rules

**Goal:** a governance document that tells everyone who decides what, how, and how to
change it — written before the first crisis, not during it.

Applies to online communities (forums, subreddits, Discord servers, wikis), open-source
projects and member-run digital groups. Where the community sits on a company's
platform, the platform's terms override; where it's a legal entity (association,
foundation, cooperative, DAO wrapper), **corporate/association law of its jurisdiction
also applies** — get the legal entity's bylaws reviewed by a lawyer.

## 1. Start with decision rights
List the decisions that actually arise and assign each:
| Decision | Who decides | How |
|---|---|---|
| Day-to-day moderation | Moderators | Per code of conduct |
| Rule changes | Council | Proposal + comment period + vote |
| Removing a moderator | Council | Supermajority |
| Budget / money | Treasurer + council | Published budget |
| Charter amendment | Members | Supermajority referendum |
| Technical direction (OSS) | Maintainers / steering committee | RFC + lazy consensus |
Anything not assigned is the default to name explicitly (often the council).

## 2. Choose the governance model honestly
- **Founder-led / BDFL:** fast, common in early OSS; write down how succession works.
- **Meritocratic maintainers:** decision rights earned through contribution (e.g.
  committer status); define how people join and leave.
- **Elected council/steering committee:** for larger communities; balance of
  legitimacy and speed.
- **Direct democracy:** member votes on major items; needs participation thresholds.
Hybrids are normal. Mismatch between the written model and how power really works is the
commonest source of governance crises.

## 3. Councils and elections
- Size (odd number, 5–9 typical), **terms** (staggered, e.g. 2 years with half up each
  year), term limits, eligibility (account age, activity, contributor status),
  conflict-of-interest rules (no more than N seats from one employer — common in OSS
  foundations).
- **Electorate:** who can vote and how verified (sockpuppets kill legitimacy).
- **Voting method:** plurality is simplest but splits votes; **ranked-choice/STV** or
  **approval voting** handle multiple candidates better. Use a known tool and publish
  the method before nominations open.
- Election officer independent of candidates; published timetable; candidate
  statements; secret ballot; results with counts.
- **Vacancies, recall** (petition threshold + vote) and resignations.

## 4. Decision procedures
- **Quorum** for meetings and votes; what counts as a majority (of those voting vs. of
  seats); supermajorities (2/3 or 3/4) for removals and amendments.
- **Lazy consensus / RFC process:** proposal posted, fixed comment window (e.g. 7–14
  days), adopted unless a formal objection; objections go to a vote.
- Emergency powers: who can act immediately (e.g. lock a channel), how long, mandatory
  review afterwards.
- Record decisions publicly (minutes, decision log).

## 5. Conduct and disputes
Link the **code of conduct**, who enforces it, the steps (warning → timeout → ban), an
appeal route to a body other than the original decider, and how complaints about
moderators or council members are handled (recusal!).

## 6. Amendment
Higher bar than ordinary decisions: proposal, comment period, supermajority, and
perhaps a member ratification vote. Protect a few "entrenched" clauses (e.g. the
amendment rule itself) with an even higher bar.

## Gotchas
- Write for low participation: quorum rules that never meet paralyse the community.
- Undefined money handling causes the bitterest disputes; publish accounts.
- Copying a large foundation's charter into a 200-member community adds dead process.

## Verify
- [ ] Decision-rights table covers rules, people, money and amendments.
- [ ] Election method, electorate verification and timetable published in advance.
- [ ] Quorum and majority definitions are unambiguous.
- [ ] Appeals and complaints about office-holders have an independent route.
- [ ] Amendment process requires a supermajority and is itself entrenched.
