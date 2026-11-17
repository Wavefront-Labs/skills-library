---
id: creative-arts.game-design.systems-and-mechanics.systemic-design-interactions
name: systemic-design-interactions
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systemic-design, immersive-sim, emergence, game-systems-thinking, interaction-matrix, chemistry-engine, simulation, player-creativity]
level: advanced
status: draft
description: "Design systemic gameplay (immersive-sim style): consistent simulation rules, an interaction matrix of elements and properties, and signposting so players improvise solutions."
sources:
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Systemic design interactions

**Goal:** a world governed by consistent rules that interact, so players solve problems
in ways the designers did not script (immersive sims; The Legend of Zelda: Breath of the
Wild's "chemistry engine", described at GDC 2017 in "Breaking Conventions with The
Legend of Zelda: Breath of the Wild").

Rules of Play (ch14 Games as Emergent Systems) frames emergence as complex behaviour
arising from simple interacting rules.

## Build the system
1. **Define elements and properties** rather than per-object scripts:
   - Elements: fire, water, electricity, wind, ice.
   - Properties: flammable, conductive, metal, buoyant, heavy.
2. **Interaction matrix:** element x property -> result.
   | | flammable | metal | wet |
   |---|---|---|---|
   | fire | burns, spreads | heats | extinguished |
   | electricity | - | conducts | conducts, stuns |
   | ice | - | - | freezes |
3. **Agents obey the same rules** as the player (enemies burn, flee fire, get shocked in
   water). Consistency is what makes systems learnable.
4. **Signpost:** teach one interaction clearly early (a grass fire in a safe area), then
   trust players to generalise.
5. **Design levels as problems, not solutions:** place a goal and a set of system
   ingredients; test that several solutions exist.

## Testing
- Track **solution diversity:** for key obstacles, log how testers solved them. One
  solution dominating means the system is not being read or the level is over-constrained.
- **Exploit review:** combinations that trivialise content; decide to allow (often fun)
  or adjust.

## Gotchas
- Special cases destroy trust in the system ("why doesn't this wooden door burn?"). If
  something must be immune, communicate it visually (stone door).
- Systemic worlds are expensive to QA; budget for interaction bugs.
- Performance: simulation (fire spread, physics) needs caps and LOD.

## Verify
- [ ] Element/property list and interaction matrix documented.
- [ ] Enemies and NPCs follow the same rules as the player.
- [ ] Key obstacles have at least three tester-found solutions.
- [ ] No unexplained special-case immunities.
