---
id: computing-software.web-development.hugo.resources-from-string
name: resources-from-string
category: computing-software
field: web-development
product: hugo
tags: [resources-fromstring, execute-as-template, generated-files, publish, virtual-resource]
level: practitioner
status: docs-checked
description: "Create a resource from a string with resources.FromString, publish it, and run template actions with resources.ExecuteAsTemplate."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/resources/FromString.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`resources.FromString` takes a target path and a string and returns a resource created from that string. The result is cached using the target path as the cache key.

- Publish with `.Publish`, or inline with `resources.Publish`.
- Calling `Permalink` or `RelPermalink` also publishes the resource.
- If the string contains template actions, pipe the result through `resources.ExecuteAsTemplate`, which takes the target path and context.

The documented example builds a `security.txt` file from `site.Params.email` and publishes it with `.Publish`.

## Checked

2026-11-04: FromString behaviour, target-path cache key, Publish and Permalink/RelPermalink publishing, ExecuteAsTemplate use and the security.txt example confirmed against the Hugo docs resources.FromString page. Nothing removed.

Method: documentation only; no commands were run.
