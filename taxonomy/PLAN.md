# Taxonomy plan: mapping all of humanity's skills

Goal: document every human skillset as AI skills — professions, lived skills, the mind,
history, every culture — built breadth-first over years.

## Principles
- **Breadth first.** A level is completely mapped, checked and frozen before any work starts on
  the level below it. Nothing moves to sub-areas until the top level covers all of humanity.
- **Place by activity, not by who does it.** Cooking at home and in a restaurant are both
  culinary; amateur vs professional is the skill's `level`.
- **Era is an attribute, not a place.** Historical and traditional ways of doing an activity
  live in that activity's category (tagged by era), not in a "history" category. History as a
  discipline (historians, archaeologists) is `humanities`.
- **Every skill is documented, including ones that can be misused.** Lockpicking, forgery,
  hacking and weapons are skills; misuse is a use, not a different skill. Every one gets a home
  in the taxonomy. (At the skill-writing stage, a small set of dangerous skills, such as weapons
  synthesis, may be documented at a high level only.)

## Scope every level is tested against
| Lens | What it catches |
|---|---|
| Professions | every occupation and industry, worldwide |
| Lived skills | daily life, home, family, relationships, the mind, every life stage to death |
| History | obsolete and rare skills, prehistory to now |
| Culture | Indigenous, traditional and non-Western knowledge and roles |
| Informal and unpaid | caring, subsistence, the informal economy, volunteering, grey and illicit work |
| Emerging | AI, space and fields still forming |

## The loop (run at every level, repeated until it converges)
1. **Sources.** Gather classifications from every lens (see `crosswalk.yaml`).
2. **Draft** the list with scope notes: covers, excludes, tie-break rules (`categories.yaml`).
3. **Crosswalk.** Every source entry maps to at least one category (`python taxonomy/check.py`).
4. **Gap hunt.** Independent agents with fresh context, one lens each, generate hundreds of
   concrete skills and try to place each one. A skill with no home, or two equally good homes,
   is a finding. Most lenses are genuine domains (history, a culture, a life stage, an
   industry sweep); some rounds also include an adversarial "rule breaker" told to attack the
   rules directly.
5. **Fix**, then repeat 3–4 with new agents and new probes.
6. **Converge (decided 13 Oct 2026, after round 3):** stop on **genuine-lens rounds**, not
   adversarial ones. Three rounds in a row of ordinary domain lenses need to find no top-level
   gaps or unresolved overlaps. A standing adversarial/rule-breaker pass keeps running
   alongside real work once the level is frozen (and at the start of the next level's gap
   hunts), logging what it finds into `gap-hunts/backlog.md` as tracked issues rather than
   blocking sign-off — adversarial review is expected to keep finding real boundary cases
   indefinitely, and waiting for it to go quiet would stall the project.
7. **Sign-off** by the owner; the level is frozen and versioned. Later changes are logged
   decisions, including fixes pulled from the adversarial backlog.

**Amendment, decided 13 Oct 2026 after round 12:** the strict "3 consecutive clean
genuine-lens rounds" target was never reached and the owner judged it unlikely to be — 6
straight rounds (7-12) landed in a 93-96% clean band with the category structure itself
unchanged since round 6; every remaining finding was a tie-break or wording gap, not a missing
category or a live rule conflict. **Level 1 is frozen at v1.3** on that basis rather than a
literal 3-clean streak. Edge cases a thorough reviewer can still find are expected
indefinitely in a taxonomy this size; they get fixed opportunistically as Level 2/3/4 work
hits them (logged in `gap-hunts/`, with a version bump), not chased in the abstract.

Each round's findings are recorded in `gap-hunts/round-N.md`.

## Levels
1. **Categories — FROZEN at v1.3** (`categories.yaml`; 29 categories, 11 global rules; see
   `gap-hunts/` for all 12 rounds and `gap-hunts/backlog.md` for open adversarial findings).
2. **Fields** (next): every profession and discipline in each category. Same loop, run
   separately per category.
3. Applications (specific tools) and crafts (tool-agnostic know-how) in each field.
4. Skills.
