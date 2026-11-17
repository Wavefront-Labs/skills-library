# Skills Library — master catalog

A searchable catalogue of human expertise as Claude skills, organised
**category → field/profession → product-or-SME-skill → skill**. Built to scale to
100k+ skills: nothing is ever listed all at once.

## How to find a skill (any project, any session)
1. **Search the manifest** (the fast path): grep `skills.index.jsonl` by keyword or
   tag — e.g. `blender`, `rhubarb`, `echocardiography`, `load-bearing`. Each line is
   one skill with its `path`, `tags`, `desc`. Open the 2–3 that match.
2. **Or drill down**: this file lists categories → open `skills/<category>/INDEX.md`
   for its fields → open `skills/<category>/<field>/INDEX.md` for its products/skills.

Each list only holds its direct children, so every file stays small no matter how
big the library grows.

## How to add a skill
```
python tools/new_skill.py <category> <field> <product> <name> "one-line description"
# write the body, fill tags + description
python tools/lint.py && python tools/reindex.py
```
`reindex` builds the manifest and every `INDEX.md`. They are git-ignored and rebuilt
locally (automatically after pull/checkout once hooks are on). See `SCHEMA.md`.

## Canonical categories (the roadmap — tier 1)
The top tier is anchored to established classifications (O*NET career clusters +
academic disciplines) so it is complete and non-arbitrary. A category gets a folder
once it has its first skill.

`agriculture-environment` · `energy-mining-utilities` · `architecture-construction` ·
`repair-maintenance` · `manufacturing-production` · `handcrafts` ·
`transportation-logistics` · `engineering-technology` · `computing-software` ·
`natural-sciences` · `mathematics` · `health-medicine` · `human-services` ·
`education-training` · `humanities` · `social-sciences` · `languages-linguistics` ·
`law-government` · `defence-public-safety` · `business-finance` · `sales-marketing` ·
`media-communication` · `creative-arts` · `hospitality-culinary` ·
`personal-care-services` · `sports-recreation` · `religion-philosophy` ·
`mind-self` · `relationships-social`

This list must match `taxonomy/categories.yaml` exactly (that file is the frozen
source of truth, v1.4, 29 categories) - update both together if it ever changes.
