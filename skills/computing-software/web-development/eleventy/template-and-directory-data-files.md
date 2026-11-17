---
id: computing-software.web-development.eleventy.template-and-directory-data-files
name: template-and-directory-data-files
category: computing-software
field: web-development
product: eleventy
tags: [directory-data, template-data-files, 11tydata, default-layout]
level: practitioner
status: docs-checked
description: "Scope Eleventy data to one template or a whole folder with .11tydata.js and .json files, and see which file names and priorities apply."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/data-template-dir.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For a template at `posts/subdir/my-first-blog-post.md`, Eleventy looks for data in this order (highest priority first):

1. Template front matter, merged with layout front matter
2. Template data file (applies only to that template): `my-first-blog-post.11tydata.js`, `my-first-blog-post.11tydata.json`, `my-first-blog-post.json`
3. Directory data file (all templates in `posts/subdir/*`): `subdir.11tydata.js`, `subdir.11tydata.json`, `subdir.json`
4. Parent directory data file (all of `posts/**/*`): `posts.11tydata.js`, `posts.11tydata.json`, `posts.json`
5. Global data files in `_data`

Example: a default layout for every template in `posts/`, in `posts/posts.json`:

```json
{ "layout": "layouts/post.njk" }
```

The data file name must match the template or the directory it lives in. Change this with `setDataFileBaseName`. Use `setDataFileSuffixes` to change the suffixes or disable the feature.

Custom data formats added in config are also read, at lower priority than their JavaScript or JSON counterparts.

## Checked

2026-11-08. Confirmed against the Eleventy docs Template and Directory Specific Data Files page (markdown source): the five-level lookup order with file names, the default-layout example, setDataFileBaseName, setDataFileSuffixes and custom formats at lower priority. Nothing removed.

Method: documentation only; no commands were run.
