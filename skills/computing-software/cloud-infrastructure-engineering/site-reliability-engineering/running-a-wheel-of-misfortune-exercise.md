---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.running-a-wheel-of-misfortune-exercise
name: running-a-wheel-of-misfortune-exercise
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [wheel-of-misfortune, disaster-role-playing, game-master, on-call-training, incident-simulation]
level: practitioner
status: docs-checked
description: "Run a Wheel of Misfortune role-play: pick a past incident or plausible failure, prepare the game master's scenario, run the session, and share what the team learned."
sources: ["https://sre.google/sre-book/accelerating-sre-on-call/", "https://sre.google/sre-book/postmortem-culture/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running a Wheel of Misfortune

**Goal:** bring SREs of different experience levels together, practise incident response safely and expose gaps in
tooling and knowledge. The SRE Book also calls it disaster role playing or "Walk the Plank"; the humorous name makes it
less intimidating to new hires.

## Format (SRE Book)
- The game master (GM) picks two team members to be primary and secondary on-call; they join the GM at the front of
  the room. The GM announces an incoming page and the on-callers say what they would do to mitigate and investigate.
- The session runs about 30 to 60 minutes. The GM provides context as it unfolds, for example what the monitoring
  graphs would look like, and plays the part of any other team they escalate to.
- The GM may steer participants away from red herrings, add stimuli for urgency, or ask pointed questions.
- At its best it is a weekly ritual in which everyone learns something; teammates may volunteer to be GM next time.

## Choosing the scenario
- A previous outage that newer members missed or older members have forgotten.
- A hypothetical breakage of a new or soon-to-launch feature, which leaves everyone equally unprepared.
- A novel breakage a coworker found in production.
- When re-enacting a postmortem, cast engineers in the roles it lays out and invite the original incident commander to
  make it realistic (SRE Book, postmortem chapter).

## Gotchas
- No virtual scenario is perfect; prepare enough dashboard and log detail that the GM can answer the actions players
  are likely to take.

## Checked
2026-11-01. Confirmed against the SRE Book chapters "Accelerating SREs to On-Call and Beyond" (Disaster Role Playing
section) and "Postmortem Culture" (re-enactment with the original incident commander). Removed: the 60-90 minute
booking, the 20-30 minute debrief, the weekly-or-biweekly and onboarding-gate cadence, the action-item step and the
verify list; the pages do not state them.
Method: documentation only; no commands were run.
