---
id: computing-software.web-development.vapor.vapor-leaf-templates
name: vapor-leaf-templates
category: computing-software
field: web-development
product: vapor
tags: [vapor, leaf, leaf-setup, templates, views, html, extend, swift]
level: practitioner
status: docs-checked
description: "Add Leaf to a Vapor app, render views from routes, and use its conditions, loops, extend/export/import layouts and built-in tags."
sources:
  - https://docs.vapor.codes/leaf/getting-started/
  - https://docs.vapor.codes/leaf/overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: render dynamic HTML (or email bodies) with Leaf from a Vapor route.

## Setup
Add the dependency in Package.swift and the product to your target:

```swift
.package(url: "https://github.com/vapor/leaf.git", from: "4.4.0"),
// target dependencies:
.product(name: "Leaf", package: "leaf"),
```

Configure in `configure.swift`:

```swift
import Leaf
app.views.use(.leaf)
```

- Templates live in `./Resources/Views` (relative to project root) as `.leaf` files.
- Enable `FileMiddleware` to serve `/Public` for JS and CSS.
- Running from Xcode needs the custom working directory set, or templates will not be found.
- Cache: disabled when the environment is `.development`, enabled in `.production` and all others (template edits then need a restart). `app.leaf.cache.isEnabled = false` turns it off, but that hurts performance in production because templates recompile on every request.

## Render
`Resources/Views/hello.leaf`: `Hello, #(name)!`

```swift
app.get("hello") { req async throws -> View in
    return try await req.view.render("hello", ["name": "Leaf"])
}
```

Use `req.view` (not Leaf directly) so tests can swap the renderer. Future style returns `EventLoopFuture<View>`.

## Context
Pass any `Encodable`. `[String: Any]` is unsupported, so wrap arrays in a struct:

```swift
struct WelcomeContext: Encodable { var title: String; var numbers: [Int] }
return req.view.render("home", WelcomeContext(title: "Hello!", numbers: [42, 9001]))
```

## Syntax
A tag is `#` + name + optional `(parameters)` + optional body after a colon closed by an end tag. Swift-like expressions work (`+ % > == ||`).

```leaf
#if(title == "Welcome"):
    Hello new user!
#elseif(title == "Welcome back!"):
    Hello old user
#else:
    Unexpected page!
#endif

#if(count(users) > 0):
    You have users!
#endif

#for(index, planet in planets):
    <li>#(index + 1) #(planet)</li>
#endfor
```

`#if(title)` checks the variable exists. When using a tag inside a condition, omit its `#` (as in `count(users)`). `#for(item in items):` loops.

## Layouts
Omit the `.leaf` extension in `#extend`.

```leaf
#extend("main"):
    #export("body"):
        <p>Welcome to Vapor!</p>
    #endexport
#endextend
```

`main.leaf` pulls it in with `#import("body")` and can use other context such as `#(title)`.

## Other built-in tags
`#count(arr)`, `#lowercased`, `#uppercased`, `#capitalized`, `#contains(arr, value)`, `#isEmpty(str)`, `#comment("...")` (not rendered), `#dumpContext` (debug the context), `#date(now)` (ISO8601 by default; `#date(now, "yyyy-MM-dd")`; third argument a time zone ID such as "America/New_York"), and `#unsafeHTML(var)` which skips HTML escaping, so guard against XSS.

## Checked

2026-11-08: read in full the Leaf getting-started and overview pages at docs.vapor.codes/leaf/ (package, cache behaviour, folder layout, rendering, context, tags, layouts). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
