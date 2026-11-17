---
id: computing-software.software-engineering.go.reflect-basics-type-value-settability
name: reflect-basics-type-value-settability
category: computing-software
field: software-engineering
product: go
tags: [go, go-unsafe-reflect, go-reflect-basics, reflect, reflection]
level: advanced
status: docs-checked
description: "Use Go reflection safely: Type vs Value, Kind switches, settability through pointers and struct tags."
sources:
  - https://go.dev/blog/laws-of-reflection
  - https://pkg.go.dev/reflect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# reflect: Type, Value and settability

**Goal:** write generic helpers (validators, mappers) that do not panic.

```go
v := reflect.ValueOf(&cfg).Elem()          // pointer -> addressable struct
t := v.Type()
for i := 0; i < t.NumField(); i++ {
    f := t.Field(i)
    if !f.IsExported() { continue }
    tag := f.Tag.Get("env")                // struct tag lookup
    fv := v.Field(i)
    if fv.CanSet() && fv.Kind() == reflect.String { fv.SetString(os.Getenv(tag)) }
}
```

The three laws: reflection goes from interface to reflection object; from reflection object to interface (`v.Interface()`); to modify a reflection object the value must be settable (addressable, and not obtained through unexported struct fields; in practice, reached via `Elem()` of a pointer). `Kind()` reports the underlying kind and returns `Invalid` for the zero Value. `reflect.TypeFor[T]()` (added in Go 1.22) returns the `Type` for the type argument `T`.

## Gotchas
- If `IsValid()` is false, all other Value methods except `String` panic; `Elem` panics unless the Kind is Interface or Pointer; `CanSet()` false means `Set` and the typed setters panic.
- `CanInterface()` reports whether `Value.Interface` can be used without panicking; use it before calling `Interface()` on fields.

## Verify
Table-test with pointer, non-pointer, nil and unexported-field inputs; none may panic and errors should name the field.

## Checked
2026-11-03. Confirmed on go.dev/blog/laws-of-reflection (the three laws, settability via Elem of a pointer) and pkg.go.dev/reflect (`CanSet`, `CanInterface`, `IsValid`, `Elem`, `Kind`, `StructField.IsExported` go1.17, `TypeFor` go1.22, `StructTag.Get`). Removed: "several times slower" and inlining claims, cache-the-Type advice, prefer-generics advice, the `TypeOf((*T)(nil)).Elem()` equivalence and the switch-on-Kind rationale (not stated on the pages).
Method: documentation only; no commands were run.
