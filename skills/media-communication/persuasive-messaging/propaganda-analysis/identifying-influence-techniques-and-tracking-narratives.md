---
id: media-communication.persuasive-messaging.propaganda-analysis.identifying-influence-techniques-and-tracking-narratives
name: identifying-influence-techniques-and-tracking-narratives
category: media-communication
field: persuasive-messaging
product: propaganda-analysis
tags: [propaganda-analysis, propaganda, influence-operations, information-operations, disinformation, misinformation, coordinated-inauthentic-behaviour, cib, astroturfing, sockpuppets, bot-detection, narrative-tracking, network-analysis, attribution, osint, disarm-framework, abcde-framework, fact-checking, info-ops, persuasive-messaging, media-literacy]
level: advanced
status: draft
description: "Analyse an influence campaign: name the techniques, track narratives across platforms, map accounts for coordination signals, and state attribution with honest confidence levels."
sources: ["DISARM framework (open taxonomy of disinformation tactics) — referenced, not reproduced", "ABCDE framework (Actor, Behaviour, Content, Degree, Effect), C. François et al. — paraphrased"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identifying influence techniques and tracking narratives

**Goal:** a defensible, evidence-based account of an influence campaign — what it says, how
it spreads, how coordinated it is, who is plausibly behind it, and whether it matters —
without overclaiming. This is analytic work for researchers, journalists, trust-and-safety
and comms teams.

## 1. Structure the analysis (ABCDE)
- **Actor:** who appears to be behind it? (state, party, company, activist group, unknown)
- **Behaviour:** *how* it operates — fake accounts, coordinated posting, paid amplification,
  laundering through "independent" sites.
- **Content:** the narratives and claims, true, false or misleading.
- **Degree:** reach, audience, platforms, languages.
- **Effect:** is it actually changing anything, or just noise?
Keep **behaviour** separate from **content**: a true claim pushed by fake accounts is still
an inauthentic operation; a false claim shared sincerely by real people is misinformation,
not an operation.

## 2. Name the techniques
Common ones to label explicitly (map to an open taxonomy like DISARM for consistency):
- **Emotional manipulation:** fear, outrage, disgust, in-group pride.
- **Scapegoating** and **us-vs-them** framing.
- **False dilemma**, **whataboutism**, **firehose of falsehood** (high volume, repetitive,
  inconsistent — aims to exhaust, not convince).
- **Impersonation** of media, officials or ordinary people; **fake experts**.
- **Information laundering:** a claim originates on a fringe site, is cited by a
  semi-credible outlet, then by mainstream figures as "reports say".
- **Selective truth / decontextualised media** — real photo, wrong event or date.
- **Astroturfing** — manufactured grassroots appearance.

## 3. Track narratives
- Define each narrative as a short claim ("The flood was caused by a secret dam release").
- Build keyword, hashtag and URL lists in all relevant languages; expand them iteratively.
- Log each sighting: platform, URL, archive link (archive everything — posts vanish),
  timestamp, account, engagement.
- Plot over time: where it first appears (**patient zero**), which accounts bridge it to
  new communities, when mainstream pickup happens.

## 4. Coordination and inauthenticity signals
No single signal proves anything; look for clusters:
- accounts created in batches; recycled or AI-generated profile images;
- **synchronised posting** (identical text or links within seconds/minutes);
- unusual hours for the claimed location; language errors consistent with another native
  language;
- high-volume posting with little original content; follower networks that mostly follow
  each other;
- shared infrastructure (same domain registrar, analytics IDs, hosting) for "independent" sites.
Network-graph tools help visualise co-sharing and retweet clusters. Platform access for
researchers changes often and has narrowed on some services — note your data limits.

## 5. Attribution with confidence levels
Attribution is the hardest and most consequential step.
- Separate **technical** evidence (infrastructure, account data), **behavioural** patterns,
  and **content alignment** with an actor's interests (weakest on its own).
- State confidence explicitly (low / moderate / high) and what would change it.
- Platforms' own takedown reports are often the strongest public attribution source; cite them.
- Avoid "it benefits X, so X did it".

## 6. Judge impact before publishing
Many operations get little real engagement. Publishing a report on a tiny campaign can hand
it the audience it failed to get. Consider the **breakout scale** — has it crossed from one
platform/community to many, or into mainstream media? Report proportionately.

## Gotchas
- Calling everyone you disagree with a bot.
- Losing evidence because nothing was archived.
- Treating engagement counts as reach (they can be faked too).
- Analyst safety: researchers exposed in reports can be targeted; consider operational
  security and anonymised bylines.

## Verify
- [ ] Behaviour and content assessed separately.
- [ ] Each technique labelled with an example and archive link.
- [ ] Narrative timeline shows origin and spread points.
- [ ] Coordination claims rest on multiple independent signals.
- [ ] Attribution stated with a confidence level and its basis.
- [ ] Impact assessed before deciding to publish.
