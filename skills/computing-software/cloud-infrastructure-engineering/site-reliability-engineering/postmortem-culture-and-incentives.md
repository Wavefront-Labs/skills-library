---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.postmortem-culture-and-incentives
name: postmortem-culture-and-incentives
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [postmortem-incentives, postmortem-culture, blameless-culture, postmortem-of-the-month, psychological-safety]
level: practitioner
status: docs-checked
description: "Build a postmortem culture that people opt into: leadership modelling, recognition, reading clubs, postmortem of the month, and removing incentives that punish disclosure."
sources: ["https://sre.google/sre-book/postmortem-culture/", "https://sre.google/workbook/postmortem-culture/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Postmortem culture and incentives

A postmortem process only works if people want to write them. The SRE Book says introducing the culture "requires
continuous cultivation and reinforcement", with senior management taking part in review and collaboration, while
blameless postmortems are ideally the product of engineer self-motivation.

## Practices from the SRE Book
- **Postmortem of the month**: an interesting, well-written postmortem shared in a monthly newsletter.
- **Postmortem reading clubs**: regular sessions where an interesting or impactful postmortem (often months or years
  old) is discussed with participants, nonparticipants and new joiners.
- **Wheel of Misfortune**: new SREs re-enact a previous postmortem; the original incident commander attends.
- **Visible rewards**: reward and celebrate good postmortems publicly and through performance management; encourage
  senior leaders to acknowledge them.
- **Ask for feedback**: survey teams on whether the culture supports their work and whether writing a postmortem is too
  much toil.
- **Ease it in**: a trial period of several complete, successful postmortems helps prove their value and shows which
  criteria should trigger one.

## Workbook organisational incentives
- **Model and enforce blameless behaviour**: leaders use blameless language, include all incident participants in
  authoring, and gather feedback through a clear review process.
- **Reward outcomes, not only writing**: if engineers are rewarded for writing but not for closing the action items,
  postmortems go unclosed. Also reward organisational change (peer bonuses, reviews, promotion), highlight improved
  reliability, and hold owners up as leaders.
- **Gamification**: a leaderboard or burndown of action items can motivate some people.
- **Share openly**: announce drafts across the organisation, run cross-team reviews, hold training exercises, and publish
  a weekly outage report.

## Culture failure patterns (Workbook) and responses
| Pattern | Response the Workbook gives |
|---|---|
| People avoid association with postmortems | review high-visibility ones for blameful prose; share good examples and how people were rewarded |
| Executive uses blameful language | steer back to asking about warning signs and why they were dismissed |
| No time to write them | prioritise the work, track completion and review, allow time for the action plan |
| Incidents repeat | ask whether action items close too slowly, feature velocity trumps fixes, or the right items were captured |

## Gotchas
- Blameless does not mean no accountability: ownership stays, aimed at systems and follow-through.
- Brief executives beforehand; a "who did this?" question in a review erodes psychological safety.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Postmortem Culture: Learning from Failure" (practices, trial period,
rewards, feedback survey) and the SRE Workbook chapter "Postmortem Culture" (organisational incentives and failure
patterns). Removed: the disincentive table (rotating authorship, co-authoring managers, lightweight templates below a
severity threshold), the auto-filled timeline claim as advice, and the near-miss and quarterly-trend verify items; none
is stated by either page.
Method: documentation only; no commands were run.
