---
id: computing-software.web-development.wordpress.editor-extensibility-slotfills-and-data
name: editor-extensibility-slotfills-and-data
category: computing-software
field: web-development
product: wordpress
tags: [slotfill, wordpress-data, plugin-sidebar, editor-extensibility, gutenberg]
level: advanced
status: docs-checked
description: "Extending the block editor UI: registerPlugin, PluginSidebar and document panels, SlotFills, @wordpress/data stores, editing post meta and block filters."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/slotfills/plugin-sidebar.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/slotfills/plugin-document-setting-panel.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/data/data-core-editor.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/filters/block-filters.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/data/data-core-notices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editor extensibility: SlotFills, sidebars and @wordpress/data

## 1. Register a plugin with a panel
```js
import { registerPlugin } from "@wordpress/plugins";
import { PluginDocumentSettingPanel } from "@wordpress/editor";   // SlotFills are documented as @wordpress/editor exports
import { useSelect, useDispatch } from "@wordpress/data";
import { store as editorStore } from "@wordpress/editor";
import { TextControl, ToggleControl } from "@wordpress/components";
import { __ } from "@wordpress/i18n";

function SeoPanel() {
  const meta = useSelect((select) => select(editorStore).getEditedPostAttribute("meta"), []);
  const { editPost } = useDispatch(editorStore);
  return (
    <PluginDocumentSettingPanel name="acme-seo" title={__("SEO", "acme")}>
      <TextControl label={__("Meta description", "acme")} value={meta?.acme_description ?? ""}
        onChange={(v) => editPost({ meta: { acme_description: v } })} __nextHasNoMarginBottom />
      <ToggleControl label={__("Hide from search", "acme")} checked={!!meta?.acme_noindex}
        onChange={(v) => editPost({ meta: { acme_noindex: v } })} />
    </PluginDocumentSettingPanel>);
}
registerPlugin("acme-seo", { render: SeoPanel });
```
- Meta must be registered with `show_in_rest: true` (and `auth_callback`) for the post type; edits save with the post.
- Build with `@wordpress/scripts`; enqueue on `enqueue_block_editor_assets` with the generated `index.asset.php` dependencies.

## 2. SlotFills available
`PluginSidebar` + `PluginSidebarMoreMenuItem`, `PluginDocumentSettingPanel`, `PluginPostStatusInfo`, `PluginPrePublishPanel`/`PluginPostPublishPanel`, `PluginMoreMenuItem`, `PluginBlockSettingsMenuItem`; the docs import all of them from `@wordpress/editor`. To limit a panel to certain post types, read `select(editorStore).getCurrentPostType()`.

## 3. @wordpress/data essentials
| Store | Use |
|---|---|
| `core/editor` (`editorStore`) | current post, edited attributes, save state, `lockPostSaving` |
| `core/block-editor` | blocks, selection, `insertBlocks`, `updateBlockAttributes` |
| `core` (`coreStore`) | entities via REST: `getEntityRecords("postType","page",{per_page:20})`, users, settings |
| `core/notices` | `createNotice("warning", "...", { isDismissible: true })` |

- `useSelect` re-renders when selected data changes; select narrowly and pass a dependency array.
- Block saving until a requirement is met: `lockPostSaving("acme-seo")` / `unlockPostSaving`.

## 4. Block filters
`addFilter("blocks.registerBlockType", "acme/attr", (settings, name) => ...)` adds attributes; `editor.BlockEdit` with `createHigherOrderComponent` adds inspector controls to existing blocks; `blocks.getSaveContent.extraProps` or the PHP `render_block` (and `render_block_{namespace/block}`) filter to output them.

## Verify
- [ ] Panel appears for the intended post types only; meta edits persist after save and reload; no console warnings.

## Checked

2026-10-25: against the Gutenberg trunk docs (last commit 2026-10-25). Confirmed: `registerPlugin` from `@wordpress/plugins`; SlotFill components imported from `@wordpress/editor`; editor store selectors/actions `getEditedPostAttribute`, `editPost`, `lockPostSaving`, `unlockPostSaving`, `getCurrentPostType`; `createNotice` with `isDismissible`; block filters `blocks.registerBlockType`, `editor.BlockEdit`, `blocks.getSaveContent.extraProps`, `render_block`. Removed the unconfirmed 6.6 version gate, the `@wordpress/edit-post` deprecation claim and the advice to prefer `render_block`.

Method: documentation only; no commands were run.
