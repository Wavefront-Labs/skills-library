---
id: computing-software.web-development.hugo.shortcodes-in-content
name: shortcodes-in-content
category: computing-software
field: web-development
product: hugo
tags: [shortcodes, shortcode-arguments, markdown-notation, inline-shortcodes, nesting]
level: practitioner
status: docs-checked
description: "Call Hugo shortcodes from content: embedded, custom and inline kinds, named versus positional arguments, paired tags, standard versus Markdown notation and nesting."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/shortcodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shortcodes insert elements such as videos, images and embeds into content.

- **Embedded:** built into Hugo.
- **Custom:** templates in `layouts/_shortcodes/`.
- **Inline:** defined inside content. Disabled by default; enable with `enableInlineShortcodes = true` under `[security]`. They cannot be nested.

Arguments are named (case-sensitive key-value) or positional, never mixed in one call. They are space-delimited; quote values with spaces. Types: string, integer, float, boolean.

```md
{{< figure src=/images/kitten.jpg alt="A white kitten" >}}
{{< instagram CxOWiQNP2MO >}}
{{< my-shortcode name="John Smith" age=24 married=false >}}
```

Some shortcodes need paired tags, some take none, some take optional content:

```md
{{< details summary="See the details" >}}
This is a **bold** word.
{{< /details >}}

{{< qr text=https://gohugo.io />}}
```

Notation:

- Markdown notation `{{% foo %}}` is processed before Markdown rendering, so its headings appear in `TableOfContents`.
- Standard notation `{{< foo >}}` is processed after rendering, so they do not.

Shortcodes other than inline ones can be nested:

```md
{{< gallery class="content-gallery" >}}
  {{< image src="/images/a.jpg" >}}
{{< /gallery >}}
```

## Checked

2026-11-04: embedded/custom/inline kinds, enableInlineShortcodes under security, named versus positional rule, quoting, scalar types, paired and self-closing tags, notation and TableOfContents effect, and nesting confirmed against the Hugo docs Shortcodes page. Nothing removed.

Method: documentation only; no commands were run.
