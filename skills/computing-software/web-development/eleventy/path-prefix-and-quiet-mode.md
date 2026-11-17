---
id: computing-software.web-development.eleventy.path-prefix-and-quiet-mode
name: path-prefix-and-quiet-mode
category: computing-software
field: web-development
product: eleventy
tags: [pathprefix, quiet-mode, subdirectory-deploy, github-pages]
level: intro
status: docs-checked
description: "Deploy an Eleventy site to a subdirectory with pathPrefix and the --pathprefix flag, and silence per-file console output with quiet mode."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Path prefix.** If the site lives in a subdirectory (common with GitHub Pages), set `pathPrefix` (default `/`). It is a prefix added to URLs in HTML files. It does not change where files go in the output folder. Pair it with the HTML `<base>` plugin to rewrite absolute URLs in your HTML.

Override from the command line without touching config:

```sh
npx @11ty/eleventy --pathprefix=eleventy-base-blog
```

This lets one code base deploy to either GitHub Pages or Netlify.

**Quiet mode.** By default Eleventy prints each file it processes and its output file. Turn that off:

```js
export default function (eleventyConfig) {
  eleventyConfig.setQuietMode(true);
};
```

The command line overrides config: `npx @11ty/eleventy --quiet`.

**Data file naming.** Directory data files normally match the folder name. `setDataFileBaseName("index")` makes Eleventy look for `index.json` and `index.11tydata.json` instead. `setDataFileSuffixes([".11tydata", ""])` is the default; `[]` disables template and directory data files entirely. The empty string entry applies only to `*.json` files. Both data-file methods were added in 2.0.0-canary.19.

## Checked

2026-11-08. Confirmed against the Eleventy docs Configuration page (markdown source): pathPrefix default and meaning, the HTML base plugin pairing, the --pathprefix example (flag added 0.2.11), quiet mode default, setQuietMode and --quiet precedence, and setDataFileBaseName and setDataFileSuffixes behaviour. Added the version note. Nothing removed.

Method: documentation only; no commands were run.
