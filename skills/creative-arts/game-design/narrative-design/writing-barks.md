---
id: creative-arts.game-design.narrative-design.writing-barks
name: writing-barks
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, barks, game-dialogue, ai-barks, combat-chatter, systemic-dialogue, voice-over, repetition, variation]
level: practitioner
status: draft
description: "Write and organise barks (short systemic voice lines): trigger list, variants per trigger, cooldowns and priority, information-carrying lines, and repetition control."
sources:
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing barks

**Goal:** short, triggered lines that make characters feel alive and give players
useful information, without becoming repetitive noise.

**Barks** are short lines triggered by game systems (spotting the player, reloading,
taking damage, idle chatter), as opposed to scripted conversation.

## Build the trigger list first
| Trigger | Purpose | Info carried |
|---|---|---|
| enemy spots player | tension, warning | "There!" + direction |
| enemy loses player | stealth feedback | "Where'd they go?" |
| reloading | opportunity window | "Reloading!" |
| grenade thrown | warning | "Grenade!" |
| ally low health | team status | "I'm hurt!" |
| idle | world building | lore, personality |
Barks are **feedback channels**: in stealth and combat they tell the player about AI
state. Write them for clarity first.

## Variants and repetition control
1. Write **several variants per trigger** (more for frequent triggers).
2. **Cooldowns** per trigger and per speaker so lines don't stack.
3. **No-repeat memory:** don't replay the last N lines for a trigger.
4. **Priority:** critical warnings interrupt idle chatter.
5. **Context tags:** vary by character, state (alerted/injured), location, number of
   allies left ("It's just me now!").

## Writing style
- 1-6 words for combat barks; idle barks can be longer.
- Distinct voice per character type; read aloud.
- Avoid memorable jokes in high-frequency barks (they wear out fastest).
- Use placeholders/variables only if the VO pipeline supports them.

## Spreadsheet format
`line_id | character | trigger | condition tags | priority | cooldown_s | line text | notes for actor`

## Gotchas
- Line counts explode (characters x triggers x variants); budget VO early.
- Barks are often heard partially over combat noise; mix and subtitle them (speaker
  names in subtitles).
- Localisation: short lines lose context for translators; add notes.

## Verify
- [ ] Trigger list with purpose and information per trigger.
- [ ] Variant counts scaled by trigger frequency.
- [ ] Cooldown, no-repeat and priority rules implemented.
- [ ] Playtesters don't report repetition in a typical session.
