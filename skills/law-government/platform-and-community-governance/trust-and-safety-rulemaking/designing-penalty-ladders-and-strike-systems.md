---
id: law-government.platform-and-community-governance.trust-and-safety-rulemaking.designing-penalty-ladders-and-strike-systems
name: designing-penalty-ladders-and-strike-systems
category: law-government
field: platform-and-community-governance
product: trust-and-safety-rulemaking
tags: [trust-and-safety-rulemaking, platform-and-community-governance, trust-and-safety, enforcement-system, penalty-ladder, strike-system, strikes, graduated-enforcement, proportionality, warnings, feature-limits, temporary-suspension, account-suspension, permanent-ban, zero-tolerance, strike-expiry, recidivism, ban-evasion, abuse-vectors, coordinated-inauthentic-behaviour, spam, enforcement-playbook, policy-to-enforcement-mapping, severity-matrix, account-level-enforcement, statement-of-reasons, dsa-article-23, misuse-suspension, repeat-infringer-policy]
level: advanced
status: draft
description: "Turn platform policies into an enforcement system: severity matrix, actions menu, strike counting and expiry, zero-tolerance categories, ban evasion, abuse-vector playbooks and measurement."
sources: ["EU Digital Services Act (Regulation (EU) 2022/2065), Articles 17 and 23 on statements of reasons and measures against misuse", "US DMCA section 512(i) repeat-infringer policy requirement", "Published platform strike-system documentation (e.g. major video and social platforms)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing penalty ladders and strike systems

**Goal:** an enforcement system where the consequence fits the violation and the
person's history, repeat abusers are removed, first-time or accidental violators
learn and stay, and every action is explainable. Applies to any user-generated-content
or marketplace platform. Some regimes constrain design: the EU DSA requires statements of
reasons for restrictions and sets conditions for suspending frequent misusers; US DMCA
safe harbour requires a repeat-infringer policy; other rules vary by market.

## 1. Map policy to enforcement
For every policy, list the violation types and assign a **severity**:
| Severity | Examples | Default response |
|---|---|---|
| Critical (zero tolerance) | child sexual exploitation, terrorist content, credible violent threats, selling illegal weapons | immediate permanent removal of account; preserve evidence; legal reporting |
| High | targeted harassment, doxxing, non-consensual intimate imagery, scams | content removal + strike + feature limit or temporary suspension |
| Medium | hate speech without threat, graphic content without warning | content removal + strike |
| Low | spam-like behaviour, minor guideline breaches | warning, label or reduced reach |

## 2. Build the actions menu
Content-level: label, interstitial/blur, age-gate, demote/reduce reach, remove.
Account-level: warning, education prompt, feature limits (no posting, no live, no
messaging new users, no monetisation), temporary suspension (e.g. 1, 7, 30 days),
permanent suspension. Network-level: device or payment-instrument blocks for ban evasion
where lawful.

## 3. Design the strike ladder
- Strikes accrue per confirmed violation (not per report).
- Example ladder (illustrative): 1st strike — warning + education; 2nd — 24-hour posting
  limit; 3rd — 7-day suspension; 4th — 30-day suspension; 5th — permanent suspension.
  High-severity violations can skip steps.
- **Expiry:** strikes lapse after a period (commonly 90 days to 1 year) of good behaviour,
  so old mistakes don't follow users forever.
- **Batching:** a burst of old violations found at once should usually count as one strike,
  not five.
- Separate ladders for distinct regimes if needed (e.g. copyright strikes under a
  repeat-infringer policy vs community-guideline strikes).
- Every action produces a user notice with the policy breached, the content, the action,
  the duration and how to appeal.

## 4. Abuse-vector playbooks
For attacks that don't fit item-by-item review — spam waves, coordinated inauthentic
behaviour, raids/brigading, fake-review rings, account takeovers — write playbooks:
signals and thresholds, who declares an incident, bulk actions allowed, collateral-damage
checks (don't ban the victims of a hijack), and communication plan.

## 5. Ban evasion
Define it as its own violation; specify the evidence standard (e.g. multiple independent
signals — device, payment, behavioural pattern) and the action. Be careful with shared
devices and networks (families, schools, internet cafes).

## 6. Measure and tune
- Recidivism by step: what share of users reoffend after each action? If warnings
  work for most first-timers, keep them.
- Appeal overturn rate by violation type — high rates mean definitions or enforcement are off.
- Distribution of actions across languages and regions to catch disparate impact.
- Time from first violation to ban for serious repeat abusers.

## Gotchas
- Permanent bans for low-severity first offences — high appeals, bad press, little safety gain.
- Strikes that never expire, making the system feel arbitrary.
- Enforcement that the user cannot see or understand (silent shadow restrictions) where
  law requires notice.
- Automated bulk actions without a rollback plan.

## Verify
- [ ] Every policy mapped to severity and default action.
- [ ] Ladder with steps, skip rules, expiry and batching rules documented.
- [ ] User notices state policy, action, duration and appeal route.
- [ ] Abuse-vector and ban-evasion playbooks with evidence standards.
- [ ] Recidivism, overturn and disparity metrics reviewed on a schedule.
