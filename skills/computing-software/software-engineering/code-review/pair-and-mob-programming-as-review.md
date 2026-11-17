---
id: computing-software.software-engineering.code-review.pair-and-mob-programming-as-review
name: pair-and-mob-programming-as-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, pair-programming, mob-programming, ensemble-programming, continuous-review, async-review]
level: practitioner
status: draft
description: "Use pair and mob (ensemble) programming as continuous review: driver/navigator roles, rotation, remote tooling, and when pairing can replace or reduce async PR review."
sources: ["https://martinfowler.com/articles/on-pair-programming.html", "https://www.agilealliance.org/glossary/mob-programming/", "https://www.remotemobprogramming.org/", "https://mob.sh/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pair and mob programming as review

## Pairing basics
- **Driver** types and thinks tactically; **navigator** reviews each line as it's written, thinks
  ahead (design, edge cases, tests), keeps notes. Switch roles every 15-30 minutes or per TDD cycle
  (ping-pong: one writes a failing test, the other makes it pass).
- **Strong-style** (Llewellyn Falco): "for an idea to go from your head into the computer, it must go
  through someone else's hands": the navigator directs, the driver types. Great for knowledge
  transfer.
- Take breaks (Pomodoro); pairing all day is exhausting.

## Mob / ensemble programming
Whole team, one screen, rotating driver every few minutes (`mob.sh` timer: `mob start 10`,
`mob next`, `mob done`). Best for complex problems, onboarding, design-heavy work, and spreading
context across a team.

## As a replacement for async review
Code written in a pair has had continuous review by a second person. Team options:
- Paired code merges with the pair's approval only (record "paired with @x" in the commit
  `Co-authored-by:` trailer and PR); compliance regimes may still require an independent approver.
- Paired code gets a lighter async review focusing on design, not lines.
- Unpaired code gets normal review.
Agree explicitly; document it in the team's working agreement.

## Remote pairing tools
VS Code Live Share, JetBrains Code With Me, Tuple, Pop, `tmux` + SSH for terminal work; `mob.sh`
to hand over via git between drivers. Good audio matters more than video.

## When pairing helps most / least
Most: tricky logic, unfamiliar code, production incidents, onboarding, high-risk changes.
Least: simple well-understood tasks, research spikes, when either person needs deep solo focus.
Measure by outcomes (defects, lead time, knowledge spread), not lines per person.

## Pitfalls
Navigator disengaged (checking phone), one person dominating, never rotating pairs (knowledge silos
in pairs), pairing used as surveillance.
