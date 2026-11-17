---
id: computing-software.web-development.hugo.menu-templates
name: menu-templates
category: computing-software
field: web-development
product: hugo
tags: [menu-templates, nested-menu, ismenucurrent, hasmenucurrent, menu-partial]
level: practitioner
status: docs-checked
description: "Render Hugo menus in a recursive partial: mark current and ancestor entries, localize names via identifier, and read page or params from menu entries."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/menu.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Menu templates render one or more defined menus. Three factors shape the template: how entries are defined (automatically, in front matter or configuration), whether the structure is flat or nested, and how entries are localized (configuration or translation tables).

The page builds `layouts/_partials/menu.html`, a recursive partial taking a `menuID` and the current page, and calls it:

```go-html-template
{{ partial "menu.html" (dict "menuID" "main" "page" .) }}
{{ partial "menu.html" (dict "menuID" "footer" "page" .) }}
```

Core ideas from the partial:

```go-html-template
{{- with index site.Menus $menuID }}
...
{{- if $page.IsMenuCurrent .Menu . }}
  {{- $attrs = merge $attrs (dict "class" "active" "aria-current" "page") }}
{{- else if $page.HasMenuCurrent .Menu . }}
  {{- $attrs = merge $attrs (dict "class" "ancestor" "aria-current" "true") }}
{{- end }}
{{- with .Children }} ...recurse... {{- end }}
```

- A localized name: use the entry's `Identifier` with `T`, falling back to `.Name`.
- Entries tied to a page expose page context through `.Page`; use `with` or `if` for entries that point to external resources or lack a parameter.
- Entries defined in configuration or front matter can carry `params`; guard possibly undefined values:

```go-html-template
<a {{ with .Params.class -}} class="{{ . }}" {{ end -}} href="{{ .URL }}">{{ .Name }}</a>
```

## Checked

2026-11-04: the three rendering factors, recursive partial, call pattern, IsMenuCurrent/HasMenuCurrent use, Identifier with T and Name fallback, .Page access and params guard confirmed against the Hugo docs Menu templates page. Nothing removed.

Method: documentation only; no commands were run.
