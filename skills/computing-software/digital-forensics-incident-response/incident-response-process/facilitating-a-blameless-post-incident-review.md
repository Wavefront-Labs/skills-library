---
id: computing-software.digital-forensics-incident-response.incident-response-process.facilitating-a-blameless-post-incident-review
name: facilitating-a-blameless-post-incident-review
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [blameless-postmortem, lessons-learned, post-incident-review, facilitation, dfir]
level: practitioner
status: docs-checked
description: "Facilitate a blameless post-incident review: timing, attendees, ground rules, timeline walk-through, contributing-factor questions and turning findings into actions."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://sre.google/sre-book/postmortem-culture/", "https://www.atlassian.com/incident-management/postmortem/blameless", "https://www.etsy.com/codeascraft/blameless-postmortems"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Facilitating a blameless post-incident review

NIST SP 800-61 covers lessons learned after incidents. If people fear blame they hide the detail that explains why the incident happened. "Blameless" means focusing on systems and decisions given the information available at the time; it does not mean no accountability for wilful misconduct.

## Setup
- Hold it soon after closure, while memory is fresh but after the adrenaline.
- Invite responders, system owners, SOC analysts who saw early alerts, comms/legal reps, and the person whose action was the entry point if they are willing. Keep the group small enough that everyone speaks.
- Facilitator is someone who was not leading the response. A separate scribe.
- Circulate the draft timeline beforehand.

## Ground rules (read aloud at the start)
1. We assume everyone acted reasonably with what they knew at that moment.
2. We talk about what happened and why, not who is at fault.
3. "Human error" is a starting point for asking what made the error easy, never a root cause.
4. What is said here is not used for performance review.

## Running it
1. **Timeline walk-through** (longest part): each phase, stop at decision points: "What did you know then? What were you looking at? What options did you see?"
2. **What went well**: keep it; it tells you what to protect.
3. **Contributing factors**: for each problem ask how detection, tooling, process, staffing, communication and architecture contributed.
4. **Actions**: each finding gets a proposed action, an owner role and a rough size. Large ones become projects.

Useful questions: When could we first have detected this? What slowed containment? What information did you need and could not find? Where did handoffs drop context?

## Gotchas
- Hindsight bias: the attacker's path looks obvious after the timeline is built; responders did not have that timeline.
- Executives in the room can silence staff; brief them on the rules or run a separate exec session.
- Insider or HR-sensitive cases need a restricted session; still apply blameless language to process gaps.

## Verify
The written review contains no named individual as a root cause, and every contributing factor maps to an action item in the tracker.

## Checked
2026-11-01. Confirmed against the Google SRE book postmortem-culture chapter and Atlassian's blameless postmortem page: assume good intentions given the information at the time; blameless review lets people escalate without fear; a blame culture hides issues. NIST SP 800-61 r2 page is a landing page only. Removed: section number, meeting timings, attendee cap and scheduling window (unsourced practice figures). Etsy page was blocked (403) and is not relied on.
Method: documentation only; no commands were run.
