---
id: computing-software.web-development.jekyll.assets-sass-coffeescript
name: assets-sass-coffeescript
category: computing-software
field: web-development
product: jekyll
tags: [sass, scss, sass-dir, coffeescript, asset-pipeline, liquid-in-assets]
level: practitioner
status: docs-checked
description: "Process Sass, SCSS and CoffeeScript in Jekyll: empty front matter trigger, sass_dir load path, output style, Liquid conflicts and the jekyll-coffeescript plugin."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/assets.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/sass.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sass is built in; CoffeeScript needs a gem. A `.sass`, `.scss` or `.coffee` file must start with two lines of triple dashes:

```sass
---
---

// start content
.my-definition
  font-size: 1.2em
```

Output lands in the same directory as the source, so `css/styles.scss` becomes `css/styles.css`.

Liquid tags and filters are processed in asset files. If a JavaScript templating language (e.g. Mustache) conflicts, wrap code in raw and endraw tags.

Sass:

- Partials go in `sass_dir` (default `_sass`); main files go where you want the output, e.g. `css`.
- `sass_dir` is only the Sass import load path. Files in it must not have empty front matter, or they will not be transformed as intended.
- Directory paths under `sass` resolve relative to `source`, not `_config.yml`.
- Output style is passed to Sass: `sass:` with `style: compressed`.
- Jekyll 4 does not allow `css/main.scss` to import a partial named `_sass/main.scss`.
- Further options are in the jekyll-sass-converter docs.

CoffeeScript (3.0+): install the `jekyll-coffeescript` gem and list it:

```yaml
plugins:
  - jekyll-coffeescript
```

## Checked

2026-11-04. Confirmed against the Jekyll assets doc and the Sass/SCSS options doc: the two-line triple-dash trigger and `.sass`/`.scss`/`.coffee` extensions, output location, Liquid and raw/endraw note, `sass_dir` default and load-path role, `style: compressed`, source-relative sass paths, the Jekyll 4 `main` partial restriction, and CoffeeScript via `jekyll-coffeescript` (3.0 and up). Nothing removed.

Method: documentation only; no commands were run.
