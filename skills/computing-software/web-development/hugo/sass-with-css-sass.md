---
id: computing-software.web-development.hugo.sass-with-css-sass
name: sass-with-css-sass
category: computing-software
field: web-development
product: hugo
tags: [sass, css-sass, dart-sass, scss, hugo-vars]
level: practitioner
status: docs-checked
description: "Transpile Sass to CSS with css.Sass: transpilers (Dart Sass and deprecated LibSass), options such as outputStyle and includePaths, hugo:vars and a dev versus prod partial."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/css/Sass.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`css.Sass [OPTIONS] RESOURCE` (alias `toCSS`) returns a `resource.Resource`. It handles SCSS and indented syntax. Extended and extended/deploy editions include LibSass, deprecated in v0.153.0. Dart Sass works with Hugo v0.114.0 and later; select it with the `transpiler` option. If both Embedded Dart Sass and Dart Sass are installed, Hugo uses Dart Sass. `hugo env` lists active transpilers.

Options:

- `transpiler`: `libsass` (default) or `dartsass`.
- `outputStyle`: LibSass `nested` (default), `expanded`, `compact`, `compressed`; Dart Sass `expanded` (default) or `compressed`.
- `enableSourceMap`, `sourceMapIncludeSources` (Dart Sass only), `targetPath`.
- `includePaths`: paths relative to the project root for `@use` and `@import`.
- `silenceDeprecations` (Dart Sass only), `importContext` (since v0.165.0, Dart Sass only).
- `vars`: injects Sass variables through `hugo:vars`. Use `css.Quoted` or `css.Unquoted` to override type inference.

```go-html-template
{{ with resources.Get "sass/main.scss" }}
  {{ $opts := dict
    "enableSourceMap" hugo.IsDevelopment
    "outputStyle" (cond hugo.IsDevelopment "expanded" "compressed")
    "targetPath" "css/main.css"
    "transpiler" "dartsass"
    "vars" site.Params.styles
  }}
  {{ with . | css.Sass $opts }}
    {{ if hugo.IsDevelopment }}
      <link rel="stylesheet" href="{{ .RelPermalink }}">
    {{ else }}
      {{ with . | fingerprint }}
        <link rel="stylesheet" href="{{ .RelPermalink }}" integrity="{{ .Data.Integrity }}" crossorigin="anonymous">
      {{ end }}
    {{ end }}
  {{ end }}
{{ end }}
```

```scss
@use 'hugo:vars' as v;
.element { color: v.$primary-color; }
```

## Checked

2026-11-04. Confirmed against the Hugo docs page css.Sass: the alias and signature, LibSass deprecation in v0.153.0, Dart Sass from v0.114.0, `hugo env`, the option names, defaults and Dart-only notes, `importContext` since 0.165.0, and `hugo:vars` with `css.Quoted` and `css.Unquoted`. Removed the claim that Dart Sass is used whenever both transpilers are present (the page says this only for Embedded Dart Sass and Dart Sass) and dropped the second source, a stub page.

Method: documentation only; no commands were run.
