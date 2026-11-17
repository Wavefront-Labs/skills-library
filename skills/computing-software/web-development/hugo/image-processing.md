---
id: computing-software.web-development.hugo.image-processing
name: image-processing
category: computing-software
field: web-development
product: hugo
tags: [image-processing, resize, page-resource, remote-resource, image-cache]
level: practitioner
status: docs-checked
description: "Process images in Hugo templates: capture page, global and remote resources, resize safely, skip missing images, and manage the image cache."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/image-processing/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo can manage any image format as a resource, but only processable images can be transformed. Results are cached so later builds stay fast. Capture the image first.

Page resource (in a bundle), global resource (in `assets`), or remote:

```go-html-template
{{ $image := .Resources.Get "sunset.jpg" }}
{{ $image := resources.Get "images/sunset.jpg" }}
{{ $image := resources.GetRemote "https://gohugo.io/img/hugo-logo.png" }}
```

Render with `Permalink`, `RelPermalink`, `Width` and `Height`. Guard against a missing image with `with`:

```go-html-template
{{ with .Resources.GetMatch "sunset.jpg" }}
  <img src="{{ .RelPermalink }}" width="{{ .Width }}" height="{{ .Height }}">
{{ end }}
```

Processing methods generate the image on demand, cache it and return a new resource:

```go-html-template
{{ with .Resources.Get "sunset.jpg" }}
  {{ with .Resize "400x" }}
    <img src="{{ .RelPermalink }}" width="{{ .Width }}" height="{{ .Height }}">
  {{ end }}
{{ end }}
```

- Metadata is not preserved on transform; use `Meta` on the original resource.
- Remote fetches should use `try` to handle errors.
- Cache location: `[caches.images]` `dir`. `hugo build --gc` removes unused cached files.
- Time and memory grow with image size; scaling down large sources before the build can help.

## Checked

2026-11-04. Confirmed against the Hugo docs page Image processing: processable-image rule, page, global and remote capture, rendering methods and the `with` guard, on-demand cached processing, the metadata and `Meta` note, the `[caches.images]` setting, `hugo build --gc` and the resource-usage advice. Nothing removed.

Method: documentation only; no commands were run.
