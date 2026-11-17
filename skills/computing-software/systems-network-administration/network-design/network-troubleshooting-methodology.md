---
id: computing-software.systems-network-administration.network-design.network-troubleshooting-methodology
name: network-troubleshooting-methodology
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-methodology, seven-step, comptia-troubleshooting, divide-and-conquer, bottom-up, top-down, follow-the-path, spot-the-difference, post-incident-review, root-cause-analysis, escalation, problem-identification, theory-of-probable-cause, preventive-measures]
level: practitioner
status: draft
description: "Apply a disciplined troubleshooting method: CompTIA's 7 steps, choosing top-down/bottom-up/divide-and-conquer, evidence capture, rollback and post-incident review."
sources:
  - https://www.comptia.org/certifications/network
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network troubleshooting methodology

## CompTIA Network+ seven steps
1. **Identify the problem**: gather information, question users, identify symptoms, determine
   if anything changed, duplicate the problem, approach multiple problems individually.
2. **Establish a theory of probable cause**: question the obvious; consider multiple approaches
   (top-down, bottom-up, divide and conquer).
3. **Test the theory**: if confirmed, determine next steps; if not, new theory or escalate.
4. **Establish a plan of action** to resolve the problem and identify potential effects.
5. **Implement the solution or escalate** as necessary.
6. **Verify full system functionality** and implement preventive measures if applicable.
7. **Document findings, actions, outcomes and lessons learned.**

## Questions that save hours (step 1)
- Who/what/where exactly? One user, a VLAN, a site, everyone? One app or all?
- When did it start? What changed (changes calendar, config archive diffs, patch windows)?
- Is it constant or intermittent? Reproducible on demand?
- What does "slow"/"down" mean in numbers (time to load, error text, screenshot)?

## Choosing an approach
| Approach | Use when |
|---|---|
| Bottom-up (L1 up) | physical/link suspicion, new installs, "nothing works" |
| Top-down (app down) | one application fails, others fine |
| Divide and conquer | start mid-stack (ping/traceroute at L3) and go up or down by result; fastest generally |
| Follow the path | trace the packet hop by hop (routing tables, ACLs, NAT) from source to destination and back |
| Spot the difference | compare a working and a failing host/site/config (diff configs, versions) |
| Swap components | quick isolation of hardware (cable, optic, port), keep one variable at a time |

## Discipline
- Change one thing at a time; record each test and result with timestamps.
- Capture evidence before fixing (show outputs, pcaps) for the root cause and the review.
- Have a rollback before acting (see safe remote change practices).
- Know escalation points (vendor TAC, ISP) and what they need: serials, outputs, pcaps, timeline.

## Post-incident review
Timeline, impact, root cause (5 whys), what detected it, what slowed resolution, actions with
owners: monitoring gaps, config standards, automation, documentation updates. Blameless format.

## Verify
- [ ] Ticket contains symptoms, timeline, tests with results, root cause, fix, and verification.
- [ ] Preventive actions tracked to completion.
