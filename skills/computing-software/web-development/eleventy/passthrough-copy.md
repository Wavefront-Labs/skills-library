---
id: computing-software.web-development.eleventy.passthrough-copy
name: passthrough-copy
category: computing-software
field: web-development
product: eleventy
tags: [passthrough-copy, addpassthroughcopy, static-assets, glob-copy, recursive-copy]
level: practitioner
status: docs-checked
description: "Copy non-template files to the Eleventy output with addPassthroughCopy: paths, globs, remapping, HTML-relative mode, serve emulation and extensions."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/copy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```js
export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("img");          // _site/img/
  eleventyConfig.addPassthroughCopy("css/fonts");
  eleventyConfig.addPassthroughCopy("**/*.jpg");     // glob (0.9.0+), slower
}
```

Paths are relative to the project root, not the input directory. If the path is inside the input directory the input directory is stripped from the output: with input `src`, `src/img` copies to `_site/img`.

**Remap output** with an object `{ input: target }`: `addPassthroughCopy({ "src/img": "subfolder/img" })`. With a glob target `{ "**/*.jpg": "img" }` the directory structure is not kept.

**HTML-relative mode** (3.1.0-alpha.1+): copies files referenced by HTML output next to the page, honouring permalinks. Unreferenced files are not copied.

```js
eleventyConfig.addPassthroughCopy("content/**/*.mp4", { mode: "html-relative" });
```

Dot files are filtered by default, files must be inside the project root and absolute paths are ignored. Extra options: `paths`, `failOnError`, `copyOptions`.

**Serve emulation** (2.0.0-canary.12+): `setServerPassthroughCopyBehavior("passthrough")` references files directly during `--serve` instead of copying. The default is `"copy"`, and it reverts to copy outside `--serve` or when not using Eleventy Dev Server.

**By extension:** add an unregistered extension such as `css` to `setTemplateFormats`; matching files are copied (slower on large projects).

Extra `recursive-copy` options go as the second argument (`expand: true` for symlinks, `debug: true`).

## Checked

2026-11-08. Confirmed against the Eleventy docs Passthrough File Copy page (markdown source): path rules and input-directory stripping, globs (0.9.0) and their slower speed, object remapping, HTML-relative mode (3.1.0-alpha.1) and its restrictions, serve emulation and when it reverts to copy, copying by extension via setTemplateFormats, and recursive-copy options. Nothing removed.

Method: documentation only; no commands were run.
