---
id: computing-software.web-development.wordpress.create-block-and-block-json
name: create-block-and-block-json
category: computing-software
field: web-development
product: wordpress
tags: [gutenberg-blocks, block-development, create-block, block-json, wordpress-scripts, register-block-type, block-attributes, block-supports]
level: practitioner
status: docs-checked
description: "Scaffolding custom WordPress blocks with @wordpress/create-block: block.json metadata, attributes, supports, wp-scripts build and register_block_type."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/getting-started/devenv/get-started-with-create-block.md
  - https://github.com/WordPress/gutenberg/blob/trunk/packages/create-block/README.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-metadata.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-api-versions/README.md
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/blocks.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# create-block and block.json

**Goal:** a custom block with metadata in `block.json`, built with the official toolchain and registered in PHP.

## 1. Scaffold
```bash
npx @wordpress/create-block@latest acme-callout --namespace acme
cd acme-callout && npm start          # wp-scripts watch build
```
Generates a plugin: `block.json`, `src/edit.js`, `src/save.js`, `src/index.js`, `style.scss`, `editor.scss`, PHP bootstrap. Options: `--namespace`, `--variant` (for example `--variant dynamic` for PHP rendering), `--template` (`standard` by default, or an npm package such as `@wordpress/create-block-interactive-template` for the Interactivity API), `--no-plugin`, `--wp-env`. For several blocks in one plugin, put each under `src/<block>/` and register the built `block.json` files; `wp_register_block_types_from_metadata_collection()` (WordPress 6.8+) registers a whole collection with a generated manifest.

## 2. block.json
```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "acme/callout",
  "title": "Callout",
  "category": "text",
  "icon": "megaphone",
  "attributes": {
    "tone": { "type": "string", "enum": ["info", "warning"], "default": "info" },
    "content": { "type": "string", "source": "html", "selector": "p" }
  },
  "supports": { "html": false, "align": ["wide", "full"], "color": { "background": true, "text": true }, "spacing": { "padding": true } },
  "textdomain": "acme",
  "editorScript": "file:./index.js",
  "editorStyle": "file:./index.css",
  "style": "file:./style-index.css"
}
```
- `apiVersion` defaults to 1; the latest is 3 (introduced in WordPress 6.3). Version 3 means the block must work inside the iframed editor, so load block styles through block.json fields rather than relying on admin-wide enqueues.
- `supports` gives you colour/spacing/typography/alignment UI and serialises styles for free - prefer it over custom attributes.
- Attributes with `source` are parsed from saved HTML; others are stored in the block comment delimiter JSON.

## 3. Register
```php
add_action( 'init', function () { register_block_type( __DIR__ . '/build/callout' ); } );
```
Reads block.json, registers scripts/styles with dependencies from the generated `index.asset.php`.

## 4. Edit/save basics
`useBlockProps()` in edit and `useBlockProps.save()` in save must wrap the root element (adds classes/supports styles). `RichText` for editable text; `InspectorControls` for sidebar settings.

## Verify
- [ ] Block appears in the inserter, saves and reloads without "This block contains unexpected or invalid content".
- [ ] Colour/spacing supports apply on front end and editor.
- [ ] `npm run build` output committed/deployed (not `src/`), `npm run lint:js` passes.

## Checked

2026-10-25: against Gutenberg trunk docs and wordpress-develop `blocks.php` (last commits 2026-10-25). Confirmed: create-block CLI options and `@latest` invocation, interactive template command, `npm start`/`build`/`lint:js` scripts, block.json `$schema`, `apiVersion` default and iframe behaviour, `file:` asset fields. Corrected the collection-registration function from 6.7 to 6.8.0 (`@since 6.8.0` in source).

Method: documentation only; no commands were run.
