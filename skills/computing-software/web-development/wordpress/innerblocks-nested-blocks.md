---
id: computing-software.web-development.wordpress.innerblocks-nested-blocks
name: innerblocks-nested-blocks
category: computing-software
field: web-development
product: wordpress
tags: [gutenberg-blocks, block-development, innerblocks, nested-blocks, allowedblocks, block-templates, template-lock, useinnerblocksprops]
level: practitioner
status: docs-checked
description: "Building container blocks with InnerBlocks/useInnerBlocksProps: allowed blocks, templates and templateLock, parent/ancestor restrictions and passing block context."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/how-to-guides/block-tutorial/nested-blocks-inner-blocks.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-templates.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-metadata.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InnerBlocks and nested blocks

**Goal:** container blocks (cards, tabs, sections) that hold other blocks, with control over what editors can put inside.

## 1. useInnerBlocksProps
```js
import { useBlockProps, useInnerBlocksProps, InnerBlocks } from '@wordpress/block-editor';
const TEMPLATE = [ ['core/heading', { level: 3, placeholder: 'Card title' }], ['core/paragraph', { placeholder: 'Card text' }] ];
export function Edit() {
  const blockProps = useBlockProps({ className: 'acme-card' });
  const innerBlocksProps = useInnerBlocksProps(blockProps, {
    allowedBlocks: ['core/heading', 'core/paragraph', 'core/image', 'core/buttons'],
    template: TEMPLATE,
    templateLock: false,            // 'all' | 'insert' | 'contentOnly' | false
  });
  return <div {...innerBlocksProps} />;
}
export function save() {
  return <div {...useInnerBlocksProps.save(useBlockProps.save({ className: 'acme-card' }))} />;
}
```
- Only **one** InnerBlocks area per block. Multiple regions = child blocks (e.g. `acme/tab` inside `acme/tabs`).
- `templateLock: 'all'` blocks all changes, `'insert'` blocks adding blocks but allows reordering, `'contentOnly'` blocks structural operations and hides blocks without content from the list view (it cannot be overridden by children). If `templateLock` is not set, the parent area's lock (or the post type's) is inherited.
- `allowedBlocks` can also be set in block.json (WordPress 6.5.0+) and names the block types allowed as direct children.

## 2. Parent/child relationships
```json
// acme/tab block.json
{ "parent": ["acme/tabs"] }          // only directly inside tabs
{ "ancestor": ["acme/tabs"] }        // anywhere within tabs (ancestor: WordPress 6.0.0+)
```
A block with `parent` is not offered in the inserter outside that parent.

## 3. Block context
Parent provides, children consume - no prop drilling:
```json
// tabs: "providesContext": { "acme/tabsId": "anchorId" }
// tab:  "usesContext": ["acme/tabsId"]
```
Available in edit as `props.context['acme/tabsId']` and in PHP render via `$block->context`.

## 4. Gotchas
- A `template` prefills the InnerBlocks area only when it has no existing content.
- The wrapper element structure in edit and save must match for static blocks, or validation fails.
- Set `orientation: 'horizontal'` (documented as a prop of `InnerBlocks`) when you style children as a row, so drag-and-drop and the inserter match.

## Verify
- [ ] Only allowed blocks can be inserted; locked templates behave as intended.
- [ ] Child blocks can't be inserted outside their parent.
- [ ] Saved posts reload without validation errors.

## Checked

2026-10-25: against the Gutenberg trunk docs (last commit 2026-10-25). Confirmed: one InnerBlocks component per block, `template` only prefills empty areas, `templateLock` values and inheritance, `orientation`, `allowedBlocks` in block.json since 6.5.0, `ancestor` since 6.0.0, `providesContext`/`usesContext`, `$block->context` in PHP. Reworded the `parent` inserter note and the `orientation` note to what the docs state (the documented `orientation` prop of `InnerBlocks`).

Method: documentation only; no commands were run.
