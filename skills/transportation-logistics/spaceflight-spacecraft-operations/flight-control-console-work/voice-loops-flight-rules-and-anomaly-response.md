---
id: transportation-logistics.spaceflight-spacecraft-operations.flight-control-console-work.voice-loops-flight-rules-and-anomaly-response
name: voice-loops-flight-rules-and-anomaly-response
category: transportation-logistics
field: spaceflight-spacecraft-operations
product: flight-control-console-work
tags: [flight-controller, mission-control, console, voice-loop, flight-director, capcom, flight-rules, go-no-go, poll, anomaly-response, malfunction-procedures, failure-investigation, console-log, handover, shift-handover, mission-operations, crew-resource-management, comm-discipline, front-room, back-room]
level: practitioner
status: draft
description: "The flight controller's craft: voice-loop discipline, applying pre-agreed flight rules, running anomalies (stabilise, assess, recommend), Go/No-Go polls and clean shift handovers."
sources: ["Kranz, Failure Is Not an Option (memoir, for culture)", "NASA public descriptions of Mission Control flight rules and console positions", "ESA ESOC flight operations public material"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Voice loops, flight rules and anomaly response

**Goal:** be a console operator whose calls are short, correct and trusted — so that
when something breaks, the room converges on a decision fast.

## 1. Voice-loop discipline
- **Monitor several loops, talk on one.** Typically the flight director's loop
  (decision loop) plus your discipline's back-room loop.
- Call format: **"<who you're calling>, <your position>"**, wait for acknowledgement,
  then the message. e.g. "Flight, EPS." — "Go ahead, EPS." — "Battery 2 temperature
  trending up 2 degrees per hour, still in limits, I'm watching it, no action."
- Lead with **impact and action**, then detail. Say "no action required" explicitly.
- Use standard words: *Go / No-Go, copy, stand by, say again, affirmative / negative*.
  Avoid "yes/no" — easily lost in noise.
- Don't step on the flight director's loop during critical events (burns, dockings,
  entry) unless it's an action-now item; use the back room or chat for the rest.

## 2. Flight rules
Flight rules are **pre-agreed decisions** made calmly before flight: "if X, then Y".
- Know the rules for your system by number and title; have the document open.
- When an event matches a rule, cite it: "Flight, EPS, per rule <number>, we're required
  to shed non-essential loads." The decision is then fast and pre-approved.
- If no rule applies, say so explicitly; the flight director decides in real time and
  the gap becomes a post-flight rule change.
- Rules beat improvisation, but they don't beat the vehicle: if the data contradict the
  rule's assumptions, raise it.

## 3. Anomaly response (the core loop)
1. **Recognise:** an alarm, limit violation or unexpected trend. Confirm it is real —
   check a second sensor, a related parameter, data staleness.
2. **Stabilise / safe the vehicle** with the malfunction procedure if one exists
   (power down, isolate, switch to backup) — preserve crew and vehicle first, diagnose
   second.
3. **Report** to the flight director: what, impact, what you've done, what you need.
4. **Assess:** time to effect ("how long before this matters?") sets the pace.
5. **Recommend** options with consequences; the flight director decides.
6. **Log** every event with UTC time, data seen, decisions and actions.
7. **Open an anomaly report** for the follow-up investigation.

## 4. Go/No-Go polls
- The flight director polls each position in a fixed order before critical events.
- Answer "**Go**" or "**No-Go**" and, if No-Go, one sentence why. Never "Go, but…" —
  if there's a "but", it's a conditional you must state as a constraint ("Go, with
  constraint that we lose heater 3").
- Your Go means you've checked your data in the last minutes, not that you haven't
  heard of a problem.

## 5. Shift handover
- Written handover log plus a face-to-face briefing: vehicle state, open anomalies,
  upcoming events, pending commands, anything you're "watching".
- Incoming controller confirms understanding and takes the loop explicitly
  ("I have the console").

## Gotchas
- Normalisation of deviance: a recurring yellow limit is still telling you something.
- Fixation on one anomaly while missing a second — assign someone to keep scanning.
- *Call formats differ between agencies and commercial operators; follow your
  programme's comm protocol.*

## Verify
- [ ] Every call you made led with impact and action.
- [ ] Each anomaly entry has recognise → safe → report → assess → recommend recorded with times.
- [ ] Flight rules cited by number where applicable.
- [ ] Handover log lists open anomalies and upcoming critical events.
