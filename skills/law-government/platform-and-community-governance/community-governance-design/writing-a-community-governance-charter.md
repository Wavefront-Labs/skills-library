---
id: law-government.platform-and-community-governance.community-governance-design.writing-a-community-governance-charter
name: writing-a-community-governance-charter
category: law-government
field: platform-and-community-governance
product: community-governance-design
tags: [community-governance-design, platform-and-community-governance, community-governance, governance-charter, community-constitution, bylaws, code-of-conduct, community-council, steering-committee, elections, voting-mechanisms, consensus, lazy-consensus, rough-consensus, supermajority, quorum, ranked-choice-voting, term-limits, recall, charter-amendment, open-source-governance, foundation-governance, dao-governance, online-community, ostrom-principles, legitimacy, conflict-of-interest, transparency]
level: practitioner
status: draft
description: "Design how an online or open-source community governs itself: charter structure, bodies and powers, decision rules, elections, conflict of interest, enforcement of norms and amendment process."
sources: ["Elinor Ostrom, Governing the Commons (design principles for commons institutions)", "Public governance documents of open-source foundations and projects (e.g. Python PEP 13, Kubernetes steering charter)", "Robert's Rules of Order (deliberative procedure reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a community governance charter

**Goal:** a short, legitimate document that tells members who decides what, how, and
how those people are chosen and removed — so the community can make hard decisions and
survive conflict and leadership changes. Applies to forums, Discord/Reddit-style
communities, open-source projects, member associations and DAO-style groups. If the
community holds money or has a legal entity (association, foundation, company,
co-operative), the charter must sit inside that entity's legal constitution and local
corporate or charity law — get legal advice for that layer.

## 1. Start from the community's purpose and stage
- Write a two-sentence purpose and scope statement.
- Match weight to size: a 50-person community needs a one-page charter and an
  informal maintainer group; a project with thousands of contributors and money needs
  elected bodies, budgets and conflict-of-interest rules.
- Document how decisions are made **now** before inventing new ones; formalise what works.

## 2. Define bodies and powers
| Body | Typical powers | Typical size |
|---|---|---|
| Members / contributors | elect council, approve charter changes | all who meet a defined membership test |
| Council / steering committee | strategy, budget, disputes, delegating authority | 5-9 (odd for tie-breaks) |
| Working groups / teams | day-to-day decisions in their area | as needed |
| Moderation / conduct team | enforce the code of conduct | separate from council where possible |
Write powers as a list; anything unlisted stays with a named default (usually the council).
Define **membership** precisely (e.g. contributions in the last 12 months, paid dues, active account age) — it decides who votes.

## 3. Choose decision rules per decision type
| Decision | Rule |
|---|---|
| Routine | lazy consensus: proceed unless someone objects within N days (e.g. 72 hours) |
| Significant | rough consensus, or simple majority of the council with quorum |
| Constitutional / irreversible | supermajority (two-thirds is common) of members or council, with notice period |
Set quorum, notice periods, how votes are cast (public or secret), and tie-breaks.
Write a short **proposal process**: template, discussion period, decision, record.

## 4. Elections
- Eligible voters and candidates (with a cut-off date to stop late sign-up packing).
- Voting method: approval or ranked-choice voting work well for multi-seat councils;
  plurality is simplest but fragments.
- Staggered terms (e.g. 2 years, half elected each year) for continuity; consider term limits.
- Neutral election officers; published results and timelines.
- Limits on how many seats any one employer/organisation can hold, to prevent capture.
- Vacancy and **recall** procedures.

## 5. Integrity safeguards
- Conflict-of-interest declarations and recusal rules.
- Transparency: public minutes and decision log (except confidential conduct cases).
- Code of conduct with a separate enforcement process and appeal route (see
  law-government.platform-and-community-governance.volunteer-moderation-leadership.recruiting-and-leading-a-volunteer-moderator-team).
- Ostrom-style principles worth checking: rules fit local conditions, those affected can
  help change them, monitoring is accountable, sanctions are graduated, disputes have
  cheap local resolution.

## 6. Amendment and adoption
- Amendment procedure harder than ordinary decisions but achievable (e.g. two-thirds
  of votes cast with a 14-day notice and quorum).
- Adopt the first charter through the most legitimate process available (e.g. a
  ratification vote of active members); legitimacy at founding prevents later disputes.
- Review the charter on a set schedule (e.g. annually).

## Gotchas
- Founders keeping unwritten vetoes — fine early, corrosive later; write it down with a sunset.
- Platform-owner rules override community rules (a hosting platform's terms always win;
  say so).
- Token- or money-weighted voting concentrating control in a few holders.
- Quorum set so high that nothing ever passes.

## Verify
- [ ] Purpose, scope and membership definition written.
- [ ] Bodies, powers and residual authority listed.
- [ ] Decision rules, quorum and proposal process for each decision type.
- [ ] Election, vacancy, recall and conflict-of-interest rules in place.
- [ ] Amendment procedure defined and charter ratified by members.
