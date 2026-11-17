---
id: computing-software.it-support-helpdesk.servicenow.kcs-licensing-model
name: kcs-licensing-model
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, kcs-licensing, kcs, kcs-coach, knowledge-management, knowledge-roles, kcs-candidate]
level: advanced
status: draft
description: "Run the KCS licensing model: Candidate, Contributor and Publisher rights, coaches, AQI-based promotion criteria, and mapping licence levels to knowledge roles."
sources:
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/040/030"
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/040/040"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/knowledge-management/concept/knowledge-management-roles.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# kcs-licensing-model

KCS v6 (Performance Assessment and Leadership practices) grants knowledge rights by
demonstrated competency, not job title. Like a driving licence: you earn the right to
publish without review.

## Levels
| Licence | Can do | Typical criteria to earn |
|---|---|---|
| KCS Candidate | Create and modify articles visible internally only; articles stay Draft/Not validated until a coach or publisher reviews | KCS training done |
| KCS Contributor | Create and validate (approve) articles for internal use; reuse and fix others' articles | AQI average >= 90% over ~25 articles for 4 weeks; coach recommends |
| KCS Publisher | Publish articles to the external/self-service audience | Contributor + consistent quality, knows audience/legal rules |
| KCS Coach | Reviews, coaches, recommends licences; not a gatekeeper | Strong contributor + coaching skills; ratio about 1 coach to 5-10 agents |

Plus the Knowledge Domain Expert role: owns content health for an area (evolve loop).

## Implementing in ServiceNow
- Map licences to roles/user criteria on each knowledge base: Candidates can contribute
  (create) but articles go through approval workflow; Contributors are in "can contribute"
  plus the approval publish path is skipped for them (use a workflow condition on group
  membership, e.g. group `KCS Contributors`); Publishers get contribute rights on the
  external KB.
- Knowledge Management Advanced lets you configure the approval workflow per knowledge
  base (`Approval publish` vs `Instant publish`) and per user criteria.
- Track AQI with Knowledge quality checklists (article quality index) and a report per
  author.

## Running it
- Every agent should become a Contributor within about 3 months; if not, coaching is
  failing, not the agent.
- Licences can be revoked when AQI drops; say so up front.
- Don't make Publisher a reward for seniority; it is about audience judgement.
- Celebrate reuse and article fixes, not only article counts (counts drive duplicates).

## Gotchas
- Requiring review of every article forever creates a backlog and kills capture-in-the-
  moment.
- Coaches who rewrite articles themselves instead of coaching the author don't scale.

## Verify
Monthly report: licence level per agent, AQI per agent, time from Candidate to
Contributor, and share of articles published without review rising while AQI holds.
