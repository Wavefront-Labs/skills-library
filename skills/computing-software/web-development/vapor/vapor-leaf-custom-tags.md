---
id: computing-software.web-development.vapor.vapor-leaf-custom-tags
name: vapor-leaf-custom-tags
category: computing-software
field: web-development
product: vapor
tags: [vapor, leaf, leaftag, custom-tags, templates, unsafeunescapedleaftag, swift]
level: advanced
status: docs-checked
description: "Write and register a custom Leaf tag in Vapor by conforming to LeafTag, reading LeafContext parameters and data, and emitting unescaped HTML."
sources:
  - https://docs.vapor.codes/leaf/custom-tags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add your own `#tag` to Leaf templates.

## Implement
Conform a type to `LeafTag` and implement `render(_:)`:

```swift
enum NowTagError: Error { case invalidFormatParameter, tooManyParameters }

struct NowTag: LeafTag {
    func render(_ ctx: LeafContext) throws -> LeafData {
        let formatter = DateFormatter()
        switch ctx.parameters.count {
        case 0: formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        case 1:
            guard let string = ctx.parameters[0].string else {
                throw NowTagError.invalidFormatParameter
            }
            formatter.dateFormat = string
        default:
            throw NowTagError.tooManyParameters
        }
        return LeafData.string(formatter.string(from: Date()))
    }
}
```

## Register
Typically in `configure.swift` (works for tags from other packages too):

```swift
app.leaf.tags["now"] = NowTag()
```

Use it: `The time is #now()`.

## LeafContext
- `parameters`: array of the tag's parameters (`ctx.parameters[0].string`).
- `data`: dictionary of the view context passed to render (`ctx.data["name"]?.string`).

Parameter version: `#hello("John")`. Data version: `#hello()` with `req.view.render("home", ["name": "John"])`.

## HTML output
If the tag returns HTML, conform to `UnsafeUnescapedLeafTag` so it is not escaped (for example `return LeafData.string("<p>Hello \(name)</p>")`). Check or sanitize any user input first.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) leaf/custom-tags, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
