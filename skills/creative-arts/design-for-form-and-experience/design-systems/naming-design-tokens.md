---
id: creative-arts.design-for-form-and-experience.design-systems.naming-design-tokens
name: naming-design-tokens
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [token-naming, token-naming-conventions, design-token-names, naming-conventions, token-taxonomy, design-systems]
level: practitioner
status: docs-checked
description: "Name design tokens with a consistent structure: category, property, variant, state and scale, avoiding appearance words in semantic names, and keeping names stable."
sources:
  - "https://www.designtokens.org/tr/2025.10/format/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Token naming conventions

Good names are predictable, searchable and stable. The structure below is a team convention, not part of any standard; the W3C Design Tokens format only constrains which characters a name may use.

## A workable structure
`category / property / role or variant / state`, written as nested groups in a token file, with a scale step for primitives.
- Primitives: `color` > `blue` > `500`, `space` > `4`.
- Semantic: `color` > `text` > `primary`, `color` > `border` > `subtle`.
- Component: `button` > `primary` > `bg` > `hover`.

## Format rules (Design Tokens Format Module 2025.10)
- A token or group name must be a valid JSON string, is case-sensitive, and must not start with `$` (that prefix is reserved for format properties).
- A name must not contain `{`, `}` or `.`, because those characters belong to alias syntax. A dotted path such as `color.text.primary` is therefore a path through nested groups, not a single name.
- A token can be an alias for another token (a reference), and aliases can reference other aliases. Semantic tokens should alias primitives.
- A token or group can be marked with `$deprecated` (true, false or an explanation string), which is the format's way to retire a name.

## Rules
1. **Use one separator and case** for exported names (for example kebab-case in CSS output) and keep to it.
2. **Order from general to specific** so sorting groups related tokens.
3. **Name by purpose, not appearance** for semantic tokens (`danger`, not `red`), and not by theme (`text.primary`, not `text.dark`).
4. **Pick one scale vocabulary** for primitives (numbers or t-shirt sizes) and use it everywhere.
5. **State and mode in a fixed position** (`hover`, `disabled`, `pressed`).
6. **Avoid abbreviations** unless standard and used consistently.
7. **Avoid renaming:** deprecate with `$deprecated` and an alias instead (see `...design-systems.versioning-deprecating-and-changelogging`).
8. **Match across tools:** design variables, the tokens file and code should line up through a deterministic transform (see `...design-systems.building-a-token-sync-pipeline`).

## Verify
- [ ] Every token name can be parsed into the structure.
- [ ] No name uses `$`, `{`, `}` or `.`.
- [ ] No semantic token name contains a colour or theme word.

## Checked
2026-11-01. Confirmed in the Design Tokens Format Module 2025.10: name rules (JSON string, case-sensitive, no leading `$`, no braces or period), aliases and chained aliases, `$deprecated`. Removed: the Nathan Curtis attribution and its description of naming levels (article not read), and specific CSS variable examples. Rules 1-6 are stated as team convention.
Method: documentation only; no commands were run.
