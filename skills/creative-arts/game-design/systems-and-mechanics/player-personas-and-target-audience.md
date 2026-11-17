---
id: creative-arts.game-design.systems-and-mechanics.player-personas-and-target-audience
name: player-personas-and-target-audience
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, player-personas, target-audience, player-motivation, demographics, lens-of-the-player, schell, user-research, audience-definition]
level: practitioner
status: draft
description: "Define a game's target audience and write 2-3 evidence-based player personas (context, motivation, skill, time) that the team uses to settle design decisions."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.nngroup.com/articles/persona/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Player personas and target audience

**Goal:** a shared, concrete picture of who the game is for, so "players will love
this" is replaced with "Sam, who plays 20 minutes on the train, will/won't use this".

Schell (2nd ed.) ch9 (The Game Is Made for a Player) uses the Lens of the Player: think about
the general and specific players, their likes and dislikes, and what they expect.
Personas are the UX practice for doing this rigorously (Nielsen Norman Group).

## Persona template
```
NAME / one-line summary     "Sam, commuter puzzle player"
CONTEXT                     where/when they play, device, session length
MOTIVATIONS                 top 3 (use a motivation model; see player-motivation-models)
GAMES THEY PLAY NOW         3 titles, and what they like about each
SKILL / EXPERIENCE          genre literacy, controls comfort
FRUSTRATIONS                what makes them quit
WHAT SUCCESS LOOKS LIKE     what they'd tell a friend
EVIDENCE                    which interviews/surveys/data this is based on
```

## Procedure
1. **Gather evidence:** interviews with 5-10 people from the intended audience,
   surveys, store reviews of comparable games, platform data.
2. **Cluster** findings into 2-3 personas (primary, secondary). More dilute focus.
3. Mark one as **primary**: when personas conflict, the primary wins.
4. Add an **anti-persona** if useful: who the game is explicitly not for (e.g. "players
   wanting competitive ranked play").
5. Use personas in reviews: for each feature, which persona benefits? Features for no
   persona are cut candidates.
6. Recruit playtesters matching personas.

## Gotchas
- Personas invented without research encode the team's assumptions; always record
  evidence.
- Demographics (age, gender) alone predict less than context and motivation.
- Designers are rarely the target persona; "I would play this" is weak evidence.
- Personas age; refresh after soft launch or early access data arrives.

## Verify
- [ ] 2-3 personas with evidence listed; one marked primary.
- [ ] Feature list mapped to personas.
- [ ] Playtest recruitment criteria derived from personas.
