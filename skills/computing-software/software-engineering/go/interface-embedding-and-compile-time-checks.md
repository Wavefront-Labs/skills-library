---
id: computing-software.software-engineering.go.interface-embedding-and-compile-time-checks
name: interface-embedding-and-compile-time-checks
category: computing-software
field: software-engineering
product: go
tags: [go, go-interfaces, go-interface-satisfaction, interface-embedding, compile-time-assertion]
level: practitioner
status: docs-checked
description: "Compose interfaces by embedding and assert at compile time that a type satisfies them with var _ I = (*T)(nil)."
sources:
  - https://go.dev/ref/spec
  - https://go.dev/doc/effective_go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Interface embedding and compile-time satisfaction checks

**Goal:** make missing methods a build error at the definition site, not at a distant call site.

```go
type Reader interface{ Read(p []byte) (int, error) }
type Closer interface{ Close() error }
type ReadCloser interface { Reader; Closer }   // embedding unions method sets

type fileStore struct{ f *os.File }
var _ ReadCloser = (*fileStore)(nil)   // compile-time assertion
```

Effective Go ("Interface checks") uses exactly this form, `var _ json.Marshaler = (*RawMessage)(nil)`, to have the compiler verify a type implements an interface. It describes the embedded form as a union of the embedded interfaces, and says only interfaces can be embedded within interfaces. The spec says interface embedding was added in Go 1.14, and that when embedding interfaces, methods with the same names must have identical signatures.

Embedding an interface in a struct promotes its methods (the spec lists promoted methods in the struct's method set), which lets a wrapper override one method and delegate the rest. The embedded interface may be nil, and the spec says calling a method on a nil interface value causes a run-time panic:

```go
type loggingRW struct{ io.ReadWriter }       // delegates unless overridden
func (l loggingRW) Write(p []byte) (int, error) { log.Printf("%d bytes", len(p)); return l.ReadWriter.Write(p) }
```

## Gotchas
- Value versus pointer receivers: the method set of a defined type `T` has only methods declared with receiver `T`, while `*T` includes both `T` and `*T` receivers. If any method has a pointer receiver, assert with `(*T)(nil)`.
- A struct embedding an interface satisfies it even if the field is never set; calls then panic as above. Initialise it in constructors.

## Verify
Remove a method on purpose and confirm `go build` fails at the `var _` line.

## Checked
2026-11-09. Read the Go spec (interface embedding, method sets, promoted methods, nil interface method call) and Effective Go ("Interface checks", interface embedding). Removed: the "zero cost" remark and the advice to keep interfaces at the consumer (not stated on pages read); replaced fragment-anchor sources with the pages.
Method: documentation only; no commands were run.
