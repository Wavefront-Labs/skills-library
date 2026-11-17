---
id: computing-software.software-engineering.groovy.closure-builder-pattern
name: closure-builder-pattern
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, closure-builder-pattern]
level: practitioner
status: draft
description: "Write a small builder with a delegate and invokeMethod/methodMissing capturing nested structure."
sources:
  - https://groovy-lang.org/dsls.html
  - https://docs.groovy-lang.org/latest/html/gapi/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Closure-based builder DSL
```groovy
class Html {
  StringBuilder out = new StringBuilder()
  def methodMissing(String tag, args) {
    out << "<$tag>"
    def c = args.find { it instanceof Closure }
    if (c) { c.delegate = this; c.resolveStrategy = Closure.DELEGATE_FIRST; c() }
    args.findAll { it instanceof String }.each { out << it }
    out << "</$tag>"
  }
}
def h = new Html(); h.div { p 'x' }
assert h.out.toString() == '<div><p>x</p></div>'
```
- Add `@DelegatesTo(Html)` on any method taking the closure for tooling.

## Gotchas
- Escape string content before output.
- Use the `DELEGATE_FIRST` strategy or outer variables win.

## Self-check
Run the snippet.
