---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.steer-by-wire-considerations
name: steer-by-wire-considerations
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [steer-by-wire, sbw, drive-by-wire, steering-redundancy, steering-feel-emulation, steering-design, steering-safety-concept, un-r79, fault-tolerant-steering]
level: practitioner
status: verified
description: "Weigh steer-by-wire: architecture options, redundancy and ASIL implications, road-feel emulation, failure behaviour, and regulatory points to confirm. Safety-critical guidance."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "ISO 26262 parts 1-12 (confirm edition); UN Regulation 79 (steering equipment; confirm current series of amendments at https://unece.org)"
  - "https://villanyautosok.hu/wp-content/uploads/2019/05/r079r4e.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Steer-by-wire considerations

Safety-critical. This is practitioner orientation, not a safety case. Defer design and approval to functional-safety engineers and the approval authority.

## 1. What it is
No continuous mechanical link between steering wheel and road wheels: a hand-wheel actuator (feel motor, angle and torque sensors) and a road-wheel actuator (steering motor on the rack) joined by controllers and networks. Some designs keep a mechanical or clutch backup; some rely on electrical redundancy alone.

## 2. Why consider it
Free packaging (no column), variable ratio and feel by software, easier right/left-hand drive, integration with automated driving (retract wheel), isolation from road noise and kickback. Costs: complexity, cost, safety case.

## 3. Safety architecture
Loss of steering is a high-severity hazard; the hazard analysis (see hazard analysis and ASIL) typically assigns the highest integrity levels, so expect:
- Redundant sensors (hand-wheel angle, rack position) with plausibility checks.
- Redundant motor windings and power paths, dual controllers, independent supplies, and fault-tolerance so a single fault does not remove steering ability (fail-operational), at least for a defined time to reach a safe state.
- Diverse monitoring and tested degradation modes (reduced assist, limited speed).
Define fault-tolerant time intervals and safe-state behaviour with the safety manager.

## 4. Feel emulation
The hand-wheel motor must reproduce self-aligning torque, friction, damping, end stops and on-centre feel from road-wheel signals (rack force estimate, motor current, lateral acceleration). Latency from hand-wheel to road wheel and back must stay low and bounded; test closed-loop stability of the haptic loop.

## 5. Regulation and verification
UN R79 (approval of vehicles with regard to steering equipment) states in its introduction that steering systems with no positive mechanical connection between the steering control and the road wheels are permitted, and has been amended (02 and 03 series, in force 18 October 2018, among others) for advanced steering systems; the conditions that apply, and under what conditions, depends on the current series of amendments and market: confirm with the approval authority. Verification includes HIL fault injection, vehicle tests across temperature, EMC, and long-term durability of actuators and sensors.

## Verify
- [ ] Hazard analysis done, with integrity levels and safe states agreed.
- [ ] Redundancy covers sensors, actuators, power, communication, software.
- [ ] Feel and latency measured against targets.
- [ ] Regulatory path confirmed with the approval authority.
