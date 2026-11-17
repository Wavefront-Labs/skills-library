---
id: creative-arts.design-for-form-and-experience.figma.scoping-variables-and-setting-code-syntax
name: scoping-variables-and-setting-code-syntax
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [variable-scoping, figma-variable-scopes, code-syntax, variable-code-syntax, hide-from-publishing, figma-variables]
level: practitioner
status: docs-checked
description: "Scope Figma variables to the properties they should be used for, hide primitives from publishing, and set code syntax so developers see your token names."
sources:
  - https://developers.figma.com/docs/rest-api/variables-endpoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Variable scoping and code syntax

## Scoping
Scoping limits where a variable appears in pickers so designers choose the right ones.
- Variables have a `scopes` property that limits which properties they apply to; the enum values are on the Types page of the Figma developer docs.
- Scope semantic variables to their intended use (`color/text/*` to text; `color/border/*` to stroke) and leave primitives unused by designers.
- **Hide from publishing:** the `hiddenFromPublishing` flag hides a variable when the file is published as a library. Mark primitives this way.

## Code syntax
- Each variable can carry **code syntax** per platform, with keys `WEB`, `ANDROID` and `iOS`: the name developers use.
- Set it to the exact output of your token build (see `...design-systems.building-tokens-with-style-dictionary`).
- Keep a deterministic transform from variable name to code name; automate with the Variables REST API where possible (see `...figma.using-the-variables-rest-api-and-import-export`).

## Verify
- [ ] Pickers show only semantic variables relevant to the property.
- [ ] Primitives are hidden from publishing.
- [ ] Code syntax matches the build output.

## Checked
2026-11-01. Confirmed on the Figma Variables REST API endpoints page: `hiddenFromPublishing` (hidden when published as a library), `codeSyntax` examples keyed `WEB`, `ANDROID`, `iOS`, and a `scopes` property. Removed: per-type scope option lists, "all scopes" default, edit-dialog steps and the Dev Mode display claim, which no page read stated.
Method: documentation only; no commands were run.
