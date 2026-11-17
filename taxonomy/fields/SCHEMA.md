# Level 2 schema: fields

One file per category: `taxonomy/fields/<category>.yaml`. A field is the discipline or
profession tier — `animation` under `creative-arts`, `cardiology` under `health-medicine`,
`structural-engineering` under `engineering-technology`. It is a lighter record than
Level 1's category entries: a name and a one-line scope are enough. Boundary disputes
between fields in different categories are already settled by Level 1's rules (activity,
method-vs-domain, etc.) — a field never re-argues which category it's in.

```yaml
category: creative-arts   # must match the Level-1 category id exactly
fields:
  - id: animation              # kebab-case, stable once skills reference it
    name: Animation
    scope: "Moving-image storytelling: character and environment art, rigging, lighting, editing, sound, and the production pipeline that turns a script into finished shots."
    examples: [character design, rigging, compositing, voice direction]   # a few recognisable sub-areas, not exhaustive — Level 3 fills these in
    status: live   # live = has skills in skills/<category>/<field>/ already; draft = proposed, no skills yet
```

## Rules
- `id` must be unique within the category, kebab-case, and stable once any skill uses it —
  moving a skill later follows the same `aliases` mechanism as Level 4.
- A field already in production (check `skills.index.jsonl`'s `field` values) must appear
  here with the same `id` and `status: live`. Never rename or drop one to "clean up" the list.
- `scope` is one sentence: what the field covers, written so a reader can tell whether a given
  skill belongs here without re-deriving the category boundary.
- Fields are drawn from real classifications per category (SOC/ISCO detailed groups for an
  industry category, ISCED subjects for an academic one, named sub-crafts for handcrafts or
  creative-arts) — cite the source style in a comment at the top of the file, not per field.
- No field count target. Some categories (mathematics) will have a handful; others
  (computing-software, creative-arts) will have dozens. Depth follows the category's real
  breadth, not a uniform template.

## Checking
`python taxonomy/fields/check.py` — validates: every category has a fields file, every field
id is unique and kebab-case, and every `field` value already live in `skills.index.jsonl` is
present with `status: live`.
