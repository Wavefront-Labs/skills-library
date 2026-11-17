---
id: creative-arts.game-design.systems-and-mechanics.applying-game-accessibility-guidelines
name: applying-game-accessibility-guidelines
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, game-accessibility, accessibility, game-ux, xbox-accessibility-guidelines, xag, game-accessibility-guidelines, subtitles, remapping, colour-blindness, cvaa]
level: practitioner
status: draft
description: "Audit and plan accessibility using the Game Accessibility Guidelines and Xbox Accessibility Guidelines: motor, vision, hearing and cognitive features, prioritised by cost and impact."
sources:
  - https://gameaccessibilityguidelines.com/
  - https://learn.microsoft.com/en-us/gaming/accessibility/guidelines
  - https://caniplaythat.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Applying game accessibility guidelines

**Goal:** an accessibility plan built from established guidelines early in development,
so features are cheap to add and players with disabilities can play.

## Reference sets
- **Game Accessibility Guidelines** (gameaccessibilityguidelines.com): grouped by
  motor, cognitive, vision, hearing, speech and general, and graded basic / intermediate
  / advanced by effort and reach.
- **Xbox Accessibility Guidelines (XAG)**: Microsoft's numbered guidelines (text
  display, contrast, additional channels for visual and audio cues, subtitles, input,
  difficulty options, and more), useful as a checklist for any platform.
- In the US, the CVAA requires accessible communication features (e.g. text/voice chat)
  in games with such features; check current legal advice.

## High-impact basics (commonly cited)
| Area | Feature |
|---|---|
| Motor | full control remapping; hold-to-toggle options; no required rapid button mashing or provide alternative |
| Vision | scalable text and UI; colour-blind safe (don't rely on colour alone); high-contrast option |
| Hearing | subtitles with size/background options and speaker names; visual cues for important sounds |
| Cognitive | objective reminders; adjustable game speed/difficulty; clear, consistent UI |
| General | settings available before gameplay starts; save settings; allow skipping/pausing cutscenes |

## Procedure
1. **Audit** the design against the basic tier of both guideline sets; mark each as
   done / planned / not applicable (with reason).
2. **Prioritise** intermediate/advanced items by audience and cost (remapping and
   subtitles early, because they get expensive late).
3. **Test with disabled players** (organisations and consultants exist; community sites
   like Can I Play That? review accessibility).
4. **Document** accessibility features on the store page; players need to know before
   buying.

## Gotchas
- Retrofitting remapping or subtitle systems late is costly; architect input and text
  systems for it from the start.
- Accessibility options also help many non-disabled players (subtitles are widely used).
- Flashing content: provide warnings and reduction options (photosensitive epilepsy).

## Verify
- [ ] Basic-tier audit completed against both guideline sets.
- [ ] Remapping, subtitles, text scaling and colour-independence implemented or scheduled.
- [ ] At least one test session with disabled players.
- [ ] Accessibility features listed on the store page.
