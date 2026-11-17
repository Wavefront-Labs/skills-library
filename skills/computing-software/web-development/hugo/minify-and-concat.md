---
id: computing-software.web-development.hugo.minify-and-concat
name: minify-and-concat
category: computing-software
field: web-development
product: hugo
tags: [minify, concat, resources-minify, resources-concat, asset-bundling]
level: intro
status: docs-checked
description: "Minify a resource with resources.Minify and join resources with resources.Concat: supported types, same-media-type rule and publish behaviour."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/resources/Minify.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/resources/Concat.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Minify: `resources.Minify RESOURCE` (alias `minify`) returns a `resource.Resource`. Any CSS, JS, JSON, HTML, SVG or XML resource can be minified.

```go-html-template
{{ $css := resources.Get "css/main.css" }}
{{ $style := $css | minify }}
```

Concat: `resources.Concat` combines a slice of resources into one resource at a target path.

- All resources in the slice must share the same media type.
- The result is cached using the target path as its cache key.
- Hugo writes the combined resource to the target path when you call `Publish`, `Permalink` or `RelPermalink`.

```go-html-template
{{ $plugins := resources.Get "js/plugins.js" }}
{{ $global := resources.Get "js/global.js" }}
{{ $bundle := slice $plugins $global | resources.Concat "js/bundle.js" }}
```

## Checked

2026-11-04. Confirmed against the Hugo docs pages resources.Minify and resources.Concat: the `minify` alias, the minifiable types, the same-media-type rule, target-path cache key and publish-on-call behaviour. Nothing removed.

Method: documentation only; no commands were run.
