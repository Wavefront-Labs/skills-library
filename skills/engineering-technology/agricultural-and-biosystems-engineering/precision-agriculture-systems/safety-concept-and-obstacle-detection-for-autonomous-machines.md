---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.safety-concept-and-obstacle-detection-for-autonomous-machines
name: safety-concept-and-obstacle-detection-for-autonomous-machines
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, autonomous-machine-safety, obstacle-detection, iso-18497, iso-13849, iso-25119, geofence, emergency-stop, risk-assessment, agricultural-robotics]
level: advanced
status: gated
description: "Frame the safety concept of an autonomous farm machine: risk assessment, safety functions, obstacle sensing, geofence, stops, standards to consult and who must sign off."
sources:
  - "ISO standards catalogue (https://www.iso.org)"
  - "Regulation (EU) 2023/1230 (https://eur-lex.europa.eu/eli/reg/2023/1230/oj)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Safety concept and obstacle detection for autonomous machines

**Safety-critical work: this is a framework to prepare discussions with a qualified machinery safety engineer and the regulator, not a design that can replace one.** People can be killed by an unsafe autonomous machine.

## Standards to consult (confirm current editions and which apply in your market)
- ISO 18497, safety of highly automated agricultural machines (scope wording (gated: unconfirmed, source is paywalled or blocked)) (principles and requirements for automated machines and for obstacle detection).
- ISO 12100 for risk assessment and risk reduction, ISO 13849-1 for the safety-related parts of control systems (performance levels), ISO 25119 for software and electronic safety of tractors and machinery for agriculture, and ISO 4254 for general agricultural machinery safety (titles and numbers (gated: unconfirmed, source is paywalled or blocked)).
- Regulation: in the EU, the Machinery Directive 2006/42/EC applies, with the Machinery Regulation (EU) 2023/1230, which applies from 14 January 2027 (Article 53) and repeals Directive 2006/42/EC with effect from that date (Article 52); other markets have their own machinery and workplace safety rules, and some require approvals for operation without a driver on public roads or near bystanders.

## Process
1. Define the operational design domain: where, when, who may be nearby, weather, speed, implement hazards.
2. Risk assessment for each hazard: collision with people and animals, runaway, implement actuation, loss of position, rollover on slopes, remote start surprise, cyber misuse.
3. Safety functions with their required performance level: emergency stop (on the machine and by remote), obstacle detection and stop, geofence stop when leaving the boundary, speed limiting, loss of communication or GNSS or sensor failure leading to a safe stop, and a safe state for the implements.
4. Sensing: combine different principles (for example lidar, radar, cameras, bumpers or bump-bars, ultrasonic) because each has failure modes in dust, rain, tall crop or glare; define the detection zone from the stopping distance at maximum speed and the worst-case slope and load; validate with realistic targets (people in various postures, animals) and test in dust and fog.
5. Operator and bystander measures: warning lights and sounds, fencing or controlled access to the field, supervised operation with a remote monitor, training and procedures for recovery and maintenance (lockout).
6. Verification: independent testing, documented evidence, periodic proof tests of the safety functions, and incident logs.
7. Sign-off by the competent safety engineer and the manufacturer or operator responsible for conformity.

## Verify
- [ ] Hazard log, safety requirement specification and test reports exist and are reviewed independently.
- [ ] Stopping distance test results exceed the detection range at every speed.
- Unconfirmed: standards editions, regulatory dates and local approvals; confirm them.
