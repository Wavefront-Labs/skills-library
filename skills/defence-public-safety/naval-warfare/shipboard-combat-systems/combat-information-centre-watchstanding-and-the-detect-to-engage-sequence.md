---
id: defence-public-safety.naval-warfare.shipboard-combat-systems.combat-information-centre-watchstanding-and-the-detect-to-engage-sequence
name: combat-information-centre-watchstanding-and-the-detect-to-engage-sequence
category: defence-public-safety
field: naval-warfare
product: shipboard-combat-systems
tags: [shipboard-combat-systems, combat-system, combat-management-system, cms, combat-information-centre, combat-information-center, cic, operations-room, ops-room, tactical-action-officer, tao, principal-warfare-officer, pwo, watchstanding, watch-turnover, detect-to-engage, kill-chain, track-management, tactical-picture, recognised-maritime-picture, rmp, common-tactical-picture, combat-identification, data-link, link-16, link-11, aegis, sensor-fusion, doctrine-modes, human-on-the-loop, rules-of-engagement, roe, scenario-fulfilment, uss-vincennes, uss-stark, naval-training]
level: practitioner
status: draft
description: "How a warship's combat system and CIC/ops room are run: functions, watch roles, track management and combat ID, the detect-to-engage sequence, ROE, automation, and Stark/Vincennes lessons."
sources: ["US Navy NAVEDTRA 14095 Operations Specialist training manual, CIC chapters (public editions)", "US Navy formal investigation into the downing of Iran Air Flight 655 (USS Vincennes), 1988, public report", "House Armed Services Committee, Report on the Staff Investigation into the Iraqi Attack on the USS Stark (1987)", "Hughes & Girrier, Fleet Tactics and Naval Operations (3rd ed., 2018)", "Gary Klein, Sources of Power (1998) — naturalistic decision-making studies of CIC teams"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Combat information centre watchstanding and the detect-to-engage sequence

**Goal:** understand how a warship turns sensor data into decisions — the combat
system architecture in outline, who does what in the combat information centre
(CIC, or "ops room"), how the tactical picture is built and how decisions are
disciplined by doctrine and rules of engagement. Content is drawn from public
training manuals and investigations; system specifics are generic by design.

## 1. The combat system in one diagram (described)
Every modern naval combat system has the same broad layers, whatever the brand
(Aegis, or the various national combat management systems):
1. **Sensors** — radars, sonars, electronic support, electro-optics, plus off-board
   data from other units via tactical data links (Link 11/Link 16 are the public
   names).
2. **Command and decision** — correlates and fuses contacts into **tracks**,
   identifies them, displays the picture, applies pre-set doctrine.
3. **Weapon direction / control** — assigns and supports weapons and countermeasures.
4. **The people** in CIC who supervise, interpret and decide.

## 2. CIC functions and roles
Classic CIC functions: **gather, process, display, evaluate, disseminate** (and,
when authorised, control/engage).
- **Tactical Action Officer (TAO) / Principal Warfare Officer (PWO):** the
  commanding officer's representative for fighting the ship; holds delegated
  engagement authority within ROE.
- **Warfare-area coordinators/controllers** (air, surface, undersea, electronic warfare).
- **Track supervisors and identification supervisors:** maintain the picture's quality.
- **Communications and link operators:** share and receive the wider picture.
- The **commanding officer** retains overall responsibility and can override.

## 3. Building the picture
- A **track** is a hypothesis: a position, motion and identity estimate, with a
  quality that decays without fresh data.
- **Combat identification** assigns standard identities (friend, assumed friend,
  neutral, suspect, hostile, unknown) from multiple cues; one cue is rarely enough.
- **Picture hygiene** matters: duplicate tracks, stale tracks and link errors
  create false confidence. Good teams continually prune and re-verify.
- Mistake to avoid: treating the display as reality. It is a model built from
  imperfect inputs.

## 4. The detect-to-engage sequence (conceptual)
**Detect → track → identify → decide (against ROE and intent) → engage → assess.**
Doctrine pre-plans as much as possible — threat-warning levels, weapon-readiness
states, and pre-authorised responses — because timelines can be very short.
Combat systems offer automated modes; doctrine sets how much is automated and keeps a
**human on the loop** with authority and responsibility to intervene. The trade-off
between speed and control is a command decision, made in advance, not in the moment.

## 5. Watchstanding discipline
- **Turnover:** the relieving watch gets a structured brief (picture, threats, ROE,
  equipment status, orders) and does not take the watch until satisfied.
- **Closed-loop communication:** repeat back critical orders and reports.
- **Fatigue and vigilance:** long quiet watches degrade detection; teams rotate
  positions and rehearse.
- **Drills:** realistic team training on simulators is how CIC teams are qualified.

## 6. Lessons from investigations
- **USS *Stark* (1987):** hit after the threat was detected but not acted on;
  investigation pointed to readiness, ROE understanding and alertness.
- **USS *Vincennes* (1988):** a civilian airliner was shot down amid a surface
  engagement; studies highlight **scenario fulfilment** (the team interpreting
  ambiguous data to fit an expected threat), interface and stress issues.
The two cases are taught together because they show opposite errors — under- and
over-reaction — under the same kind of time pressure.
Uncertainty: interpretations of both incidents remain contested; cite the official
reports and named analyses.

Related: picture-keeping overlaps with
`defence-public-safety.military-planning-and-command.command-and-control-systems.maintaining-a-common-operating-picture-and-c2-messaging`.

## Verify
- [ ] You can describe the sensor / command-and-decision / weapon layers.
- [ ] You can name the CIC roles and who holds engagement authority.
- [ ] You can explain why a track is a hypothesis and how identities are assigned.
- [ ] You can state the detect-to-engage sequence and where ROE and automation fit.
- [ ] You can contrast the *Stark* and *Vincennes* lessons.
