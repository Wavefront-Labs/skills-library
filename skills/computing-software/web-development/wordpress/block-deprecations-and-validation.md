---
id: computing-software.web-development.wordpress.block-deprecations-and-validation
name: block-deprecations-and-validation
category: computing-software
field: web-development
product: wordpress
tags: [gutenberg-blocks, block-development, block-deprecation, block-validation, invalid-content, migrate-attributes, block-recovery]
level: practitioner
status: docs-checked
description: "Changing saved block markup safely with deprecations: why validation fails, writing deprecated entries with save and migrate, ordering, and testing old content."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-deprecation.md
  - https://developer.wordpress.org/block-editor/reference-guides/block-api/block-deprecation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block deprecations and validation errors

**Goal:** update a static block's markup or attributes without every existing post showing "This block contains unexpected or invalid content".

## 1. Why validation fails
For static blocks the editor re-runs `save(attributes)` and compares with the HTML stored in the post. Any difference (new class, changed wrapper, different attribute source) = invalid block. PHP rendering isn't involved; dynamic blocks (`save` returns null) avoid this entirely.

## 2. Add a deprecation for every shipped save change
```js
import v1Save from './deprecated/v1-save';
const deprecated = [
  {
    attributes: { tone: { type: 'string', default: 'info' }, text: { type: 'string', source: 'html', selector: 'p' } },
    supports: { html: false },
    save: v1Save,                                          // exact old save function, frozen
    migrate: (attrs) => ({ ...attrs, content: attrs.text }), // old 'text' -> new 'content'
  },
];
registerBlockType(metadata.name, { edit: Edit, save, deprecated });
```
- The editor tries the current `save`, then each deprecation in array order (keep the array in reverse chronological order, newest first). The first whose `save` reproduces the stored HTML wins; `migrate` converts attributes; the block is upgraded on next save. Deprecations are not a chain: each one migrates straight to the current shape. A deprecation whose `save` does not validate is skipped entirely, including its `migrate`, even if `isEligible` returns true.
- Each deprecation needs the **old attributes and supports** (supports affect saved classes), not just the old save.
- Freeze old save code in separate files; never import shared helpers that may change later.
- `isEligible(attributes, innerBlocks)` returns true for a block that is valid but still needs migration (fix bad data).
- Inner blocks: `migrate` can return `[attributes, innerBlocks]` to restructure children.

## 3. Avoiding the problem
- Prefer dynamic rendering for blocks likely to evolve.
- Use `supports` features instead of hand-rolled classes.
- Never change a released `save` without a deprecation, including whitespace/class order.

## 4. Testing
Keep fixtures of saved markup from each version (for example a `fixtures/v1.html` file); a test parses them with `@wordpress/blocks` `parse()` and asserts `isValid === true` after registering the block. In the editor, "Attempt block recovery" is a last resort, not a fix.

## Verify
- [ ] Posts created with every previous version open without invalid-block warnings.
- [ ] Re-saving migrates to the new markup/attributes.
- [ ] Fixture tests run in CI.

## Checked

2026-10-25: against the Gutenberg trunk docs for block deprecation (repository last commit 2026-10-25). Confirmed: deprecations are tried when the current save is invalid or `isEligible` returns true, order of trial, `migrate` return shape (attributes or `[attributes, innerBlocks]`), attributes/supports/save not inherited. Added the skipped-when-invalid rule. Removed the unconfirmed fixture file path.

Method: documentation only; no commands were run.
