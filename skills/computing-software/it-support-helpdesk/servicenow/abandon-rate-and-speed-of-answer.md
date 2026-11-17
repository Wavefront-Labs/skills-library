---
id: computing-software.it-support-helpdesk.servicenow.abandon-rate-and-speed-of-answer
name: abandon-rate-and-speed-of-answer
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, abandon-rate, average-speed-of-answer, asa, service-level-percent, contact-center-metrics, metrics]
level: practitioner
status: draft
description: "Measure and act on phone abandon rate, average speed of answer and service level (80/20): formulas, short-abandon exclusion, interval analysis, and fixes."
sources:
  - "https://www.thinkhdi.com/library/supportworld/2019/metric-of-month-abandon-rate"
  - "https://www.thinkhdi.com/library/supportworld/2018/metric-of-month-average-speed-answer"
  - "https://www.icmi.com/resources/2017/the-three-most-important-contact-center-metrics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# abandon-rate-and-speed-of-answer

Phone metrics come from the ACD/telephony platform (Teams Phone queues, Genesys, Five9,
Amazon Connect), not the ticket tool. Pull them per 15- or 30-minute interval; daily
averages hide the problem.

## Definitions
- **Offered calls**: calls that reached the queue (after IVR).
- **Abandoned**: caller hung up before an agent answered. **Short abandons** (under 5-10 s,
  wrong number, IVR mistakes) are usually excluded; state your threshold.
- **Abandon rate** = abandoned (excluding short) / offered (excluding short). Typical IT
  desk target 3-8%.
- **ASA** = total queue wait time of answered calls / answered calls. Typical 30-60 s.
- **Service level** = calls answered within T seconds / offered (some exclude abandons
  before T). Common target 80% in 30 s ("80/30") or 80/20.
- **Longest wait**: worst case; complaints come from the tail, not the average.

## Reading them together
| Pattern | Likely cause |
|---|---|
| High abandon, high ASA, at 08:30-10:00 | Staffing not matched to the morning peak |
| High abandon, low ASA | Callers giving up in IVR, or callback option missing; check IVR menu drop-off |
| Good SL but complaints | Long tail; check longest wait and repeat callers |
| Spike on one day | Outage; check whether a banner/IVR message was up |

## Actions
1. Interval-level staffing: shift breaks and lunches out of the peak; stagger starts.
2. IVR outage message during major incidents (deflects duplicate calls).
3. Virtual hold/callback when the predicted wait exceeds about 2 minutes.
4. Shift-left: the top 3 call reasons get a self-service fix and portal promotion.
5. Forecast with Erlang C (see the staffing skill) using offered calls and AHT per
   interval.

## Bringing it into ServiceNow
Import interval data (Import Set or the telephony integration's CTI records) into a
custom table or Performance Analytics external indicators so the desk dashboard shows
phone metrics next to ticket metrics.

## Gotchas
- Comparing desks that use different short-abandon thresholds or SL definitions.
- Calls transferred out of the queue counted as answered inflate SL.
- Abandon rate rises when ASA targets are met by pushing callers to voicemail; count
  voicemail as offered.

## Verify
Monthly report per interval shows abandon rate, ASA, SL and longest wait with stated
definitions; peaks have a named action and the next month shows the effect.
