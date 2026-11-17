---
id: computing-software.software-engineering.software-architecture.event-storming-workshop
name: event-storming-workshop
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, domain-driven-design, ddd, event-storming, big-picture-event-storming, domain-discovery, collaborative-modelling]
level: practitioner
status: draft
description: "Facilitate EventStorming (big picture, process and design level): sticky colour grammar, timeline, hotspots, pivotal events and deriving bounded contexts and aggregates."
sources:
  - https://www.eventstorming.com/
  - https://leanpub.com/introducing_eventstorming
  - https://github.com/ddd-crew/eventstorming-glossary-cheat-sheet
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EventStorming workshops

Alberto Brandolini's workshop format for exploring a business domain with domain experts and engineers together, using sticky notes on a long wall (or Miro).

## Formats
1. **Big Picture:** whole business flow, 10-30 people, 1 day. Goal: shared understanding, find problems and boundaries.
2. **Process Level:** one process in detail with the grammar below; who does what and which rules apply.
3. **Design Level:** add aggregates and enough detail to write code.

## Colour grammar (ddd-crew cheat sheet)
| Sticky | Meaning |
|---|---|
| Orange | Domain event - past tense ("Order Placed") |
| Blue | Command - an intention ("Place Order") |
| Small yellow | Actor / person |
| Lilac / purple | Policy - "whenever X then Y" reactive logic |
| Pink (large) | External system |
| Green | Read model / information needed to decide |
| Large yellow | Aggregate (design level) |
| Red / hot pink | Hotspot - problem, question, conflict |
Process grammar: actor + read model -> command -> aggregate/system -> event -> policy -> command...

## Big Picture steps
1. **Chaotic exploration:** everyone writes orange events silently and sticks them on the wall roughly in time order (15-30 min).
2. **Enforce the timeline:** sort left to right, remove duplicates, discuss the gaps.
3. **Pivotal events:** mark the few events where the business changes phase ("Order Placed", "Order Shipped"); they suggest boundaries.
4. **Hotspots:** red stickies on every disagreement, question, or pain point. Do not resolve them now.
5. **People and systems:** add actors and external systems.
6. **Opportunities and problems:** dot-vote on hotspots to pick what to work on.

## From stickies to design
- Clusters of events and language between pivotal events -> candidate **bounded contexts** (same word meaning different things marks a boundary).
- Commands that must be checked against the same rules -> **aggregates** (invariants).
- Policies -> event handlers, sagas, or process managers.
- Read models -> queries/projections (CQRS).

## Facilitation tips
- Unlimited modelling space (8+ m of paper), no chairs, plenty of markers. Remote: Miro template, pre-made sticky palettes.
- The domain experts must be in the room; developers alone produce guesses.
- Keep it in business language; ban technical events ("DB Updated").
- Photograph the wall and transcribe key outcomes into a context map and backlog.

## Verify
- [ ] Output includes: event timeline, list of hotspots with owners, candidate bounded contexts, and next steps.
- [ ] Domain experts confirm the timeline reflects reality.
