---
id: computing-software.web-development.hugo.postcss-pipeline
name: postcss-pipeline
category: computing-software
field: web-development
product: hugo
tags: [postcss, css-postcss, autoprefixer, inline-imports, node]
level: practitioner
status: docs-checked
description: "Process CSS with css.PostCSS: install packages, config file search order, inlineImports and other options, environment variables, and a partial."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/css/PostCSS.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`css.PostCSS [OPTIONS] RESOURCE` (alias `postCSS`) returns a `resource.Resource`.

Setup: install Node.js, install packages in the project root, create a PostCSS config, put CSS in `assets/css`, then create and call a partial.

```sh
npm install --save-dev postcss postcss-cli autoprefixer
```

Config files searched in the project root and modules: `postcss.config.js`, `postcss.config.mjs`, `postcss.config.cjs`.

```js
import autoprefixer from 'autoprefixer';
const isDev = process.env.HUGO_ENVIRONMENT === 'development';
export default {
  plugins: [!isDev ? autoprefixer : null],
  map: isDev ? { inline: true } : false
};
```

Options with a config file: `config` (config directory), `inlineImports` (default `false`; resolves relative to the module mount; external URL imports and imports with media queries are ignored), `skipInlineImportsNotFound`, `importContext` (0.165.0). Without a config file: `noMap`, `parser`, `stringifier`, `syntax`, `use` (space-delimited plugins).

Hugo passes `PWD`, `HUGO_ENVIRONMENT` (default `production` for `hugo build`, `development` for `hugo server`), `HUGO_PUBLISHDIR` and a `HUGO_FILE_*` variable per mounted config file.

```go-html-template
{{ with resources.Get "css/main.css" }}
  {{ $opts := dict "inlineImports" true }}
  {{ with . | css.PostCSS $opts }}
    {{ if hugo.IsDevelopment }}
      <link rel="stylesheet" href="{{ .RelPermalink }}">
    {{ else }}
      {{ with . | minify | fingerprint }}
        <link rel="stylesheet" href="{{ .RelPermalink }}" integrity="{{ .Data.Integrity }}" crossorigin="anonymous">
      {{ end }}
    {{ end }}
  {{ end }}
{{ end }}
```

## Checked

2026-11-04. Confirmed against the Hugo docs page css.PostCSS: the alias and signature, setup steps, the npm install command, the config file search order, the config example, options with and without a config file (including `inlineImports` behaviour and `importContext` in 0.165.0), the environment variables and their defaults. Dropped the second source, a stub page.

Method: documentation only; no commands were run.
