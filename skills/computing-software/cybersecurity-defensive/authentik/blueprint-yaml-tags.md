---
id: computing-software.cybersecurity-defensive.authentik.blueprint-yaml-tags
name: blueprint-yaml-tags
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, blueprints, yaml-tags, keyof, find, enumerate]
level: advanced
status: docs-checked
description: "Reference for authentik blueprint YAML tags: !KeyOf, !Find, !Context, !Env, !File, !Format, !If, !Condition, !Enumerate/!Index/!Value and !AtIndex with examples."
sources:
  - https://docs.goauthentik.io/customize/blueprints/v1/tags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write dynamic blueprints. For VS Code add to `settings.json` `yaml.customTags`: `!Condition sequence`, `!Context scalar`, `!Enumerate sequence`, `!Env scalar`, `!File scalar`, `!File sequence`, `!Find sequence`, `!Format sequence`, `!If sequence`, `!Index scalar`, `!KeyOf scalar`, `!Value scalar`, `!AtIndex scalar`.

- `!KeyOf my-policy-id`: primary key of the entry with that `id`; missing entry makes the blueprint invalid.
- `!Env my_env_var` or `!Env my_env_var, default`; `!File /path/to/file` (also with default).
- `!Find [authentik_flows.flow, [slug, default-password-change]]`: first arg model, then key/value pairs; resolves to the primary key. `!FindObject` (2025.8) returns the serialized data; combine `!AtIndex [!FindObject [...], designation]`.
- `!Context foo` reads the instance context; default via `!Context [foo, default-value]`.
- `!Format [my-policy-%s, !Context instance_name]`: Python % formatting.
- `!If [cond, when-true, when-false]` (short form `!If [true]`); dictionaries and lists are truthy unless empty; branches are fully resolved so tags nest.
- `!Condition [MODE, args...]` with modes EQ, NEQ, AND, NAND, OR, NOR, XOR, XNOR; at least one argument; a single argument returns its boolean (negated for negated modes). Use with `!If` or an entry's `conditions`.
- `!Enumerate [<iterable>, SEQ|MAP, <item yaml>]` with `!Index <depth>` (key or position) and `!Value <depth>` valid only inside it; depth 0 is the current Enumerate, 1 the enclosing one. An Enumerate's iterable can never be `!Index 0` or `!Value 0`.
```yaml
example: !Enumerate [!Context list_of_totp_stage_names, MAP, [!Index 0, !Value 0]]
```
- `!AtIndex [["first", "second"], 0]` returns `first`; a mapping key works too; a third argument is the default, otherwise a missing index raises an error and invalidates the blueprint.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/customize/blueprints/v1/tags/ (read in full); dropped the nested dot-notation note for !Context, which the page does not state.
