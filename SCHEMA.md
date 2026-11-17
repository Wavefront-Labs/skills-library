# Skill file schema

Every skill is one Markdown file with YAML frontmatter, stored at:

```
skills/<category>/<field>/<product-or-skill>/<name>.md
```

- **category** — broad domain of human endeavour (tier 1). See `SKILLS.md`.
- **field** — discipline or profession (tier 2), e.g. `animation`, `cardiology`.
- **product-or-skill** (tier 3) — either an **application** (a specific tool:
  `blender`, `photoshop`, `vectorcraft`) or a **craft** (tool-agnostic know-how:
  `echocardiography`, `screenwriting`). Never a project: what was learned on a project
  is written as an application or craft skill, with the project at most a worked example.
- **name** — the skill itself (the file), e.g. `cel-shading`.

## Required frontmatter

```yaml
---
id: creative-arts.animation.blender.cel-shading   # = dotted path; set by new_skill.py, checked by lint
name: cel-shading
category: creative-arts
field: animation
product: blender
tags: [blender, npr, eevee, toon, cel, shader]     # lowercase, the search keys
level: practitioner        # intro | practitioner | advanced | sme
status: verified           # stub | draft | docs-checked | verified
description: "One sentence. This is what shows in the manifest and indexes."   # keep it quoted
sources: []                # optional list of refs/URLs
licence: Apache-2.0        # the whole library's licence; tools/serve.py prints the notice
version: 1                 # bump on every change (CI checks it)
updated: 2026-10-13        # date of the last change
aliases: []                # optional: old ids, if the skill was ever moved
---
```

Then the skill body (the actual craft/knowledge), any length.

## Rules (enforced by `tools/lint.py`)
- `category` / `field` / `product` MUST match the file's folder path.
- `id` = `<category>.<field>.<product>.<name>` and MUST be unique.
- All fields above except `sources` are required. `description` ≤ 200 chars, one line.
- `tags` is a list (≥1) of lowercase strings.
- `category` must be one of the canonical categories in `SKILLS.md`.
- `version` is a whole number and `updated` a YYYY-MM-DD date. Any change to a
  published skill bumps `version` (CI compares against the base branch).
- No machine-specific paths (`D:/...`, `C:\Users\...`, `/home/...`); use placeholders.
- Frontmatter is real YAML (parsed with PyYAML). Quote `description`: unquoted, YAML
  cuts the value at ` #` and rejects `: ` inside it.
- `level` ∈ {intro, practitioner, advanced, sme}; `status` ∈ {stub, draft, verified}.
- Filenames and path segments: lowercase kebab-case.

## Ids are permanent
Once a skill is merged its id is published: consumers and other skills refer to it.
If a skill must move to a better path, move the file, set the new id, and put the old
id in `aliases`. CI fails if a published id disappears without an alias, and `tools/serve.py`
resolves aliases to the skill's new home.

## The one rule that makes 100k work
Tags + description are the search surface. A skill nobody can find by tag does
not exist. Tag generously and specifically (tools, techniques, synonyms).

## Lifecycle
0. `pip install -r requirements.txt` (once; the tools need PyYAML).
1. `python tools/new_skill.py <category> <field> <product> <name>` — scaffolds the file.
2. Write the body; fill tags + description.
3. `python tools/lint.py` — validates.
4. `python tools/reindex.py` — rebuilds `skills.index.jsonl` and all `INDEX.md`
   (git-ignored; never hand-edited).
