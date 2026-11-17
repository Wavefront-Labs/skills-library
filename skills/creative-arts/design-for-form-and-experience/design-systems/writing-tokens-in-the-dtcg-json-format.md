---
id: creative-arts.design-for-form-and-experience.design-systems.writing-tokens-in-the-dtcg-json-format
name: writing-tokens-in-the-dtcg-json-format
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [dtcg-format, dtcg-json, design-tokens-community-group, tokens-json, w3c-design-tokens, token-file-format]
level: practitioner
status: docs-checked
description: "Write tokens in the W3C DTCG JSON format: $value, $type, groups, aliases in curly braces, composite types, and check the spec version for value syntax."
sources:
  - https://www.designtokens.org/tr/drafts/format/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DTCG JSON format

The Design Tokens Community Group publishes a vendor-neutral JSON format for design tokens. The draft read for this review (2025.10 preview) says not to implement it yet, and value syntax differs between drafts, so check the spec version your tools support before copying examples.

## Core shape
```json
{
  "color": {
    "$type": "color",
    "blue": { "500": { "$value": { "colorSpace": "srgb", "components": [0.11, 0.31, 0.85] }, "$description": "Primary brand blue" } },
    "text": { "primary": { "$value": "{color.blue.500}" } }
  },
  "space": { "$type": "dimension", "4": { "$value": { "value": 16, "unit": "px" } } }
}
```
- An object with `$value` is a token; `$type` should be set on the token or inherited from the nearest ancestor group. Tools must not guess a type from the value.
- Optional: `$description` (plain text), `$extensions` (vendor data, reverse-domain keys), `$deprecated` (`true`, `false` or an explanation string).
- **Groups** are objects without `$value`; they can carry `$type`, `$description`, `$deprecated`, `$extensions` and `$extends`. A `$root` token gives a group a base value.
- **Aliases:** curly braces with a dot path, `"{color.blue.500}"`, point to a whole token; chains are allowed and cycles are errors. `$ref` with a JSON Pointer can reach inside a value.
- **Names** must not start with `$` or contain `{`, `}` or `.`.
- **Colour** is an object with `colorSpace` and `components` (optional `alpha`, `hex`). **Dimension** is an object with numeric `value` and unit `px` or `rem`; the unit is required even at 0.
- **Composite types** include shadow, border, transition, typography, stroke style and gradient; sub-values may be explicit or references.
- File extensions `.tokens` and `.tokens.json`; preferred media type `application/design-tokens+json` (`application/json` also allowed).

## Version differences to check
Older drafts used plain strings such as `"#1D4ED8"` and `"16px"`. Read the version your tooling targets (see `...design-systems.building-tokens-with-style-dictionary`) before authoring.

## Verify
- [ ] The file parses as JSON and every alias resolves.
- [ ] Types on groups apply as intended.
- [ ] The spec version used is noted in the repo.

## Checked
2026-11-01. Confirmed on the Design Tokens Format Module 2025.10 preview draft (first 100000 characters read): token and group properties, `$type` inheritance, alias and `$ref` forms, name restrictions, colour and dimension object forms, composite type list, extensions and media type. Removed: the list of primitive types (font family, weight, duration, cubic bezier, number) and the "later stable version" claim, which were not in the portion read.
Method: documentation only; no commands were run.
