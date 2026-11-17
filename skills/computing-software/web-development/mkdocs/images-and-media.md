---
id: computing-software.web-development.mkdocs.images-and-media
name: images-and-media
category: computing-software
field: web-development
product: mkdocs
tags: [images, media-files, cname, static-files]
level: intro
status: docs-checked
description: "Include images and other non-Markdown files in a MkDocs site: store them under docs, link relatively, and know they are copied unaltered."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Any file in `docs_dir` that is not recognised as Markdown is copied to the built site unaltered. Put images beside the pages:

```text
mkdocs.yml
docs/
    CNAME
    index.md
    about.md
    license.md
    img/
        screenshot.png
```

Reference with standard Markdown image syntax:

```markdown
![Screenshot](img/screenshot.png)
```

The relative path also lets Markdown editors preview the image.

Notes:
- The page's example layout puts a GitHub Pages `CNAME` file in the docs root (see `github-custom-domain`).
- `*.js` and `*.css` files are copied the same way whether or not a config option references them.
- Links inside raw HTML are not validated or converted; format them yourself for the rendered site.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (File layout; Linking to images and media; Linking from raw HTML) and the `extra_javascript` note in "Configuration" that `*.js` and `*.css` files are always copied. Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
