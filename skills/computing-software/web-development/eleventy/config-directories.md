---
id: computing-software.web-development.eleventy.config-directories
name: config-directories
category: computing-software
field: web-development
product: eleventy
tags: [eleventy-config, input-directory, output-directory, includes-directory, layouts-directory]
level: intro
status: docs-checked
description: "Set up an Eleventy config file and change the input, output, includes, layouts and data directories with config API methods or CLI flags."
sources:
  - https://www.11ty.dev/docs/config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configuration is optional. Put the first of these in the project root; the first one found is used: `.eleventy.js`, `eleventy.config.js`, `eleventy.config.mjs`, `eleventy.config.cjs`.

```js
export default async function (eleventyConfig) {
  // Configure Eleventy
};
```

Directories (defaults in brackets):

| Option | Default | API | CLI |
| --- | --- | --- | --- |
| `dir.input` | `.` | `setInputDirectory()` | `--input` |
| `dir.includes` | `_includes` | `setIncludesDirectory()` | none |
| `dir.layouts` | the includes dir | `setLayoutsDirectory()` | none |
| `dir.data` | `_data` | `setDataDirectory()` | none |
| `dir.output` | `_site` | `setOutputDirectory()` | `--output` |

The includes, layouts and data directories are relative to the input directory.

```js
export default function (eleventyConfig) {
  // Order matters: put these at the top of the config file.
  eleventyConfig.setInputDirectory("views");
  eleventyConfig.setIncludesDirectory("my_includes");
  eleventyConfig.setOutputDirectory("dist");
};
```

The setter methods are not available in plugins; use the named `dir` export there.

`dir.layouts` applies only to Eleventy layouts set in front matter or data. A template-language `{% extends %}` still searches the includes directory.

CLI: `npx @11ty/eleventy --input=views --output=dist`. `--input` accepts a directory, a single file or a glob.

## Checked

2026-11-04. Confirmed against the Eleventy Configuration page: the four default config filenames and first-found rule, the dir.input, dir.includes, dir.layouts, dir.data and dir.output defaults, the setter methods (v3.0.0, not available in plugins, order matters), CLI overrides --input and --output only, directories relative to input, the dir.layouts note about {% extends %}. Nothing removed.

Method: documentation only; no commands were run.
