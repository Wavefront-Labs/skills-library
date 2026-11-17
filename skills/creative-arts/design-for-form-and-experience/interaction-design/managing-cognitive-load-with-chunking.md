---
id: creative-arts.design-for-form-and-experience.interaction-design.managing-cognitive-load-with-chunking
name: managing-cognitive-load-with-chunking
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [cognitive-load, chunking, working-memory, laws-of-ux, millers-law, intrinsic-extraneous-load, information-design]
level: practitioner
status: draft
description: "Manage cognitive load: cut extraneous load, chunk information into meaningful groups, support recognition over recall, and test load with time-on-task and error measures."
sources:
  - "Sweller, Cognitive Load During Problem Solving (1988) and Cognitive Load Theory"
  - "Miller, The Magical Number Seven, Plus or Minus Two (1956); Cowan (2001), working memory about 4 chunks"
  - "Nielsen Norman Group - Minimize Cognitive Load to Maximize Usability (nngroup.com/articles/minimize-cognitive-load)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cognitive load and chunking

**Goal:** leave users' limited working memory for their task, not for deciphering the interface.

## Types of load
- **Intrinsic:** inherent task difficulty (filing taxes). Reduce by sequencing and scaffolding, not by removing necessary content.
- **Extraneous:** caused by the design (clutter, inconsistent patterns, unclear labels). **Eliminate.**
- **Germane:** effort that builds understanding; support it with good structure and examples.

## Tactics
1. **Chunk** information into meaningful groups of about 4 (Cowan) rather than a magic 7: phone numbers (3-3-4), card numbers (4-4-4-4), grouped settings, sections with headings.
2. **Recognition over recall:** show options, recent items, autocomplete, visible labels rather than commands to remember (`creative-arts.design-for-form-and-experience.ux-design.heuristic-evaluation-with-nielsens-ten`).
3. **Reduce visual noise:** whitespace, consistent patterns, limited colours and fonts, remove decoration that competes with content (`creative-arts.design-for-form-and-experience.interaction-design.balancing-whitespace-and-information-density`).
4. **One primary task per screen;** progressive disclosure for the rest.
5. **Defaults and automation:** prefill known data; compute rather than ask.
6. **Externalise memory:** show progress, summaries, running totals, breadcrumbs, and previously entered answers on later steps.
7. **Familiar patterns** reduce learning load (`creative-arts.design-for-form-and-experience.interaction-design.applying-jakobs-law-and-web-conventions`).

## Measure
Time on task, error rate, SEQ ratings, NASA-TLX (6-item subjective workload questionnaire) or a Paas mental-effort scale; compare design variants.

## Verify
- [ ] Extraneous load sources listed and removed.
- [ ] Long strings and lists are chunked and grouped.
- [ ] Load compared across variants with a measure.
