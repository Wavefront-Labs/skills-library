---
id: computing-software.software-engineering.refactoring.change-function-declaration
name: change-function-declaration
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-first-set, change-function-declaration, rename-function, add-parameter, remove-parameter, migration-mechanics, published-api]
level: practitioner
status: draft
description: "Rename functions and add or remove parameters safely, using the simple mechanics for local code and the migration (wrap, deprecate, inline) mechanics for published APIs."
sources: ["https://refactoring.com/catalog/changeFunctionDeclaration.html", "Refactoring, 2nd ed. (Fowler), ch6 Change Function Declaration"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change Function Declaration (rename, add/remove parameter)

**Goal:** a function name that says what it does and parameters that match what it
needs, changed without breaking callers you can't see.

## Simple mechanics (all callers in reach)
1. If removing a parameter, make sure the body doesn't use it.
2. Change the declaration.
3. Update every caller (IDE "Change Signature" / "Rename Symbol" does steps 2-3 atomically).
4. Test.
Use this when the function is private or internal to one codebase and the IDE can see
every call site, including reflection/string references (check templates, configs, SQL).

## Migration mechanics (published or widely used functions)
1. Refactor the body if needed so extraction is easy.
2. Extract the body into a NEW function with the desired name/signature:
   ```python
   def circumference(radius):               # new
       return 2 * math.pi * radius

   def circum(radius):                       # old, now a thin wrapper
       warnings.warn("use circumference()", DeprecationWarning, stacklevel=2)
       return circumference(radius)
   ```
3. If adding a parameter, give it a sensible default in the old wrapper's call.
4. Test. Migrate callers one by one (Inline Function the old wrapper at each call site).
5. When no callers remain (or after the deprecation window for public APIs), delete
   the old function.
Language aids: `@Deprecated(forRemoval=true)` (Java), `[Obsolete]` (C#), `// Deprecated:`
comment (Go), `@deprecated` JSDoc / TS, `warnings.deprecated` decorator (Python 3.13).

## Choosing names
Name for what it does from the CALLER's perspective; if you can't name it well, the
function may be doing too much (split it first). Write the call site you wish you had,
then make the declaration match.

## Parameters
- Remove unused parameters: they mislead.
- Too many parameters -> Introduce Parameter Object or Preserve Whole Object.
- Boolean flag parameters -> Remove Flag Argument (separate functions).

## Gotchas
- Overloads and default arguments can make the "same" call resolve differently after a change.
- Dynamic languages: grep for string uses (`getattr(obj, "circum")`, routes, mocks `patch("mod.circum")`).
- Interface/virtual methods: change every implementation in the hierarchy together.

## Verify
- [ ] No remaining references (IDE usages + grep for the old name).
- [ ] Deprecation warnings visible in CI logs for remaining external callers.
