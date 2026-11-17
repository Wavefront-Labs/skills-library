---
id: computing-software.web-development.eleventy.ignore-files
name: ignore-files
category: computing-software
field: web-development
product: eleventy
tags: [eleventyignore, gitignore, node-modules-ignore, ignores-set]
level: intro
status: docs-checked
description: "Keep files out of an Eleventy build with .eleventyignore, the ignores Set, .gitignore handling and the default node_modules exclusion."
sources:
  - https://www.11ty.dev/docs/ignores/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add `.eleventyignore` to the input directory or project root: one file or glob per line.

```
README.md
_drafts/
secretNunjucksTemplates/anotherFolder/**/*.njk
```

Paths in `.gitignore` are ignored automatically. Layouts, includes and similar lower-level files are not affected by this feature.

**Config API** (1.0.0+): `eleventyConfig.ignores` is a `Set`.

```js
export default function (eleventyConfig) {
  eleventyConfig.ignores.add("README.md");
  eleventyConfig.ignores.delete("README.md");
}
```

It starts with `**/node_modules/**` (v2.0; v1.0 had `node_modules/**` for the root only). To search `node_modules` for templates, delete that entry. These ignores are separate from the file watcher's ignores (v2.0.0+).

Where Eleventy looks (entries relative to the ignore file): project root `.eleventyignore` and `.gitignore`; input directory `.eleventyignore`. A `.gitignore` in a separate input directory stopped being read in 1.0.

**Opt out of .gitignore**: `eleventyConfig.setUseGitIgnore(false)`. Then `.eleventyignore` is the only source, and `node_modules` is processed unless you list it.

The preprocessor API can also ignore files.

## Checked

2026-11-04. Confirmed against the Eleventy Ignore Template Files page: .eleventyignore in the input directory or project root with the sample entries, automatic .gitignore handling, lower-level template files unaffected, eleventyConfig.ignores as a Set (v1.0.0), the default **/node_modules/** entry in v2.0 (node_modules/** in v1.0) and how to delete it, decoupling from the watcher ignores in v2.0.0, ignore file locations, the 1.0 removal of .gitignore support in a separate input directory, setUseGitIgnore(false) and the preprocessor note. Removed the unconfirmed 0.3.5+ gate and corrected the canary gate.

Method: documentation only; no commands were run.
