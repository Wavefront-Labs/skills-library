---
id: creative-arts.circus-arts.circus-act-creation.shock-loading-and-fall-arrest-for-performers
name: shock-loading-and-fall-arrest-for-performers
category: creative-arts
field: circus-arts
product: circus-act-creation
tags: [circus-act-creation, circus-arts, rigging-load-calculation, rigging-math, shock-load, fall-arrest, free-fall, stopping-distance, energy-absorber, safety-lines]
level: advanced
status: draft
description: "Estimate shock loads when a falling performer is arrested: fall height vs stopping distance, why slack is dangerous, arrest force limits."
sources: ["Harry Donovan, Entertainment Rigging (2002) - shock loads", "EN 355 energy absorbers (6 kN arrest force limit) and OSHA 1926.502 (1800 lbf maximum arresting force)", "ANSI E1.43 Performer Flying Systems - https://tsp.esta.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shock loading and fall arrest for performers

**Goal:** understand and estimate the forces when a falling performer or object is
stopped by a line, so you can choose slack, materials and hardware that keep forces
survivable for the body and within component ratings.

## The basic estimate
For a body of weight W falling freely a distance h and stopped over a distance d with
roughly constant deceleration:
  **Force F ~ W x (1 + h / d)** (constant-deceleration value)
- Fall 1 m, stop over 0.25 m: F ~ 5 W.
- Fall 1 m, stop over 0.05 m (stiff steel): F ~ 21 W.
- Fall 0.1 m, stop over 0.25 m: F ~ 1.4 W.
Real arrests are not constant deceleration, so peaks are higher; treat this as a lower
bound. For a line that behaves like a linear spring and stretches a maximum distance d, energy balance
(W x (h + d) = 1/2 x F x d) gives a peak of about **2 x W x (1 + h / d)**, twice the figures above
(10 W for a 1 m fall stopped over 0.25 m). Use the larger figure for hardware selection, and a load cell or the
manufacturer's data for real systems.

## Consequences
- **Slack is the enemy**: every bit of free fall before the line tightens raises h.
  Safety lines (lunges, belts) must be kept with minimal slack.
- **Stretch is your friend**: dynamic ropes, fabric and energy absorbers increase d.
  Static ropes and wire rope do not.
- **Body tolerance**: industrial fall arrest limits the force on a person to about
  6 kN (EN 355) or 8 kN (OSHA 1800 lbf). Performer systems should be designed well below.

## Design choices
- Use energy absorbers or dynamic elements in safety lines where falls are possible.
- Keep anchors above the performer to reduce fall distance and pendulum swing.
- Specify hardware for the calculated peak (see design factors skill).
- Prefer systems where the performer cannot free fall at all (constant tension lines,
  operated lunges).

## Gotchas
- A dropped object (prop, stage weight) also shock loads its line - and anyone below.
- Fabric slack drops are deliberate shock loads; plan them with the rigger.

## Verify
- [ ] Free-fall distance in every safety system estimated and minimised.
- [ ] Peak force estimate documented for any intentional drop.
- [ ] Hardware rated above the estimate with the agreed factor.
