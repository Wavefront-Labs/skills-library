---
id: computing-software.digital-forensics-incident-response.incident-response-process.standing-up-an-incident-war-room
name: standing-up-an-incident-war-room
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [war-room, incident-commander, csirt, incident-communications, dfir]
level: practitioner
status: draft
description: "Stand up a physical or virtual war room for a major incident: channels, roles, cadence, access control, information radiators and teardown."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.fema.gov/emergency-managers/nims/components"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Standing up an incident war room

**Goal:** within the first hour of a Sev-1, give responders one place to coordinate that the
attacker cannot read and that does not drown in chatter.

## Virtual war room (default)
- **Out-of-band platform** if identity or email may be compromised: separate tenant or
  Signal/Wire group created from personal devices; do not use the corporate Slack/Teams if the
  attacker has had admin rights.
- **Channels:** `#ir-<case>-command` (decisions only, IC and leads), `#ir-<case>-tech`
  (analysis chatter), `#ir-<case>-comms` (legal, PR, exec liaison). Keep exec chatter out of tech.
- **Bridge line** with a fixed dial-in and PIN, open during working hours; recorded only if legal
  agrees.
- **Shared storage** for evidence notes and the master timeline with access limited to named
  responders; no evidence files in chat.

## Physical war room
- Room with a lock, whiteboards, wired network on a clean segment, printer, spare laptops.
- Badge-controlled; sign-in sheet if evidence is handled there.
- No speakerphones near windows/corridors; clean whiteboards before visitors.

## Operating rhythm
- IC sets cadence: e.g. tech stand-up every 2 h, leadership update twice daily.
- Each stand-up: what changed, current scope, containment status, blockers, next actions with owners.
- A scribe maintains the decision log and action list in real time.

## Information radiators
- Current severity, phase, scope numbers (hosts, accounts, data).
- Action board (owner, due, status).
- Timeline of key events (first known compromise, detection, containment).

## Teardown
- Archive channel history and bridge notes to the case record; revoke war-room accounts and
  guest access; rotate the bridge PIN.

## Gotchas
- Inviting too many people: everyone in the command channel becomes a decision maker.
- Discussing response actions on systems the attacker controls tips them off.
- Forgetting to archive chat before workspace retention deletes it.

## Verify
Every participant is named, the channel is out of attacker reach, and the decision log is
being written from minute one.
