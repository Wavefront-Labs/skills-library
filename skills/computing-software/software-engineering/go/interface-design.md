---
id: computing-software.software-engineering.go.interface-design
name: interface-design
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-interfaces, effective-go, go-idioms, accept-interfaces-return-structs, consumer-side-interfaces, nil-interface, mocking, go-accept-interfaces]
level: practitioner
status: verified
description: "Design Go interfaces idiomatically: small, defined by the consumer, accept interfaces return structs, compile-time assertions, and the nil-interface trap."
sources: ["https://go.dev/doc/effective_go#interfaces", "https://go.dev/wiki/CodeReviewComments#interfaces", "https://go.dev/ref/spec#Interface_types", "https://go.dev/doc/faq#nil_error"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Go interface design

**Goal:** interfaces that decouple code and make testing easy, instead of Java-style
interface-per-struct boilerplate.

## Principles
1. **Define interfaces where they are used, not where types are implemented.** The
   consumer states the minimal behaviour it needs:
   ```go
   // package billing
   type invoiceStore interface {
       Save(ctx context.Context, inv Invoice) error
   }
   func NewService(s invoiceStore) *Service { ... }
   ```
   The `postgres` package exports a concrete `*Store`; it satisfies the interface
   implicitly, and need not know billing exists.
2. **Small** (rule of thumb: one to three methods). `io.Reader`, `io.Writer`, `fmt.Stringer`. Compose
   bigger ones by embedding (`io.ReadWriter`).
3. **Accept interfaces, return concrete types.** Returning a struct lets callers use all
   its methods and lets you add methods without breaking anyone.
4. **Don't define an interface before a consumer uses it.** Go CodeReviewComments: do not define
   interfaces before they are used, and do not define them on the implementor side "for mocking";
   design the API so it can be tested through the real implementation's public API.

## Compile-time check
```go
var _ invoiceStore = (*postgres.Store)(nil)   // fails to compile if Store drifts
```

## The nil interface trap
An interface value is nil only if both its type and value are nil:
```go
func find() error {
    var e *NotFoundError = nil
    return e            // returns a NON-nil error (type set, value nil)
}
```
Return a literal `nil` for "no error". Same for any interface-typed return.

## Type assertions and switches
```go
if s, ok := v.(fmt.Stringer); ok { ... }      // always use the two-value form
switch x := v.(type) { case int: ...; case string: ... }
```
Optional capabilities via assertion is idiomatic (`io.WriterTo` fast path in `io.Copy`).

## Empty interface
`any` (alias for `interface{}`) discards type safety; prefer generics for containers
and helpers since Go 1.18.

## Testing
Consumer-side interfaces make hand-written fakes trivial:
```go
type fakeStore struct{ saved []Invoice }
func (f *fakeStore) Save(_ context.Context, inv Invoice) error { f.saved = append(f.saved, inv); return nil }
```
Generated mocks (gomock/mockery) are optional; fakes are often clearer.

## Verify
- [ ] No exported interface in a package that also contains its only implementation (unless it's a deliberate plugin point).
- [ ] Functions returning `error` never return a typed nil pointer.

## Checked
2026-10-21 on Go 1.27.3 (Windows): the consumer-side interface, `var _ invoiceStore = (*Store)(nil)` and fake compiled and satisfied the interface implicitly; `find()` returning a typed nil pointer compared `!= nil` (printed `false` for `== nil`); the comma-ok assertion returned `false` while the single-value assertion panicked (`interface conversion: string is not fmt.Stringer`); `io.Copy` used a source's `WriterTo` method. Guidance on consumer-side interfaces, 'do not define interfaces before they are used' and 'not for mocking' re-read from https://go.dev/wiki/CodeReviewComments#interfaces; 'two implementations' was not in that text and was removed, and the 1-3 method size is a rule of thumb.
