---
id: computing-software.software-engineering.go.doc-comments-and-pkg-go-dev
name: doc-comments-and-pkg-go-dev
category: computing-software
field: software-engineering
product: go
tags: [go, go-design-style, go-doc-comments, godoc, doc-comments, pkg-go-dev, examples]
level: practitioner
status: docs-checked
description: "Write Go doc comments that render on pkg.go.dev: package comments, headings, lists, links, deprecations and testable examples."
sources:
  - https://go.dev/doc/comment
  - https://pkg.go.dev/testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Doc comments and pkg.go.dev

**Goal:** every exported name documented in the format `go doc` and pkg.go.dev render.

```go
// Package billing computes invoices and tax.
//
// # Usage
//
// Create a [Calculator] and call [Calculator.Total]:
//
//	c := billing.NewCalculator(billing.USD)
//	total, err := c.Total(items)
//
// See [RFC 3339] for time formats.
//
// [RFC 3339]: https://www.rfc-editor.org/rfc/rfc3339
package billing

// Total returns the sum of items including tax.
// It returns [ErrEmpty] if items has no entries.
//
// Deprecated: use [Calculator.TotalWithDiscount].
func (c *Calculator) Total(items []Item) (Money, error)
```

Rules from the Go doc comment guide: doc comments sit immediately before top-level package, const, func, type and var declarations, and every exported name should have one; they use complete sentences, and a package comment's first sentence begins with "Package ". Paragraphs are unindented non-blank lines; indented lines are preformatted code blocks; a heading is an unindented `# Text` line set off by blank lines (the `#` syntax was added in Go 1.19); list items only contain paragraphs; `[Name]` and `[pkg.Name]` are doc links to identifiers in the current or another package; `[Text]: URL` lines define link targets. A paragraph starting `Deprecated:` is a deprecation notice; pkg.go.dev hides the docs of deprecated identifiers by default. `gofmt` reformats doc comments to a canonical form.

Example functions may end with a line comment beginning `Output:`, which is compared with standard output when tests run (leading and trailing space ignored); `Unordered output:` matches any line order:

```go
func ExampleCalculator_Total() { /* ... */ fmt.Println(total); // Output: 12.50 USD }
```

## Gotchas
- For a multi-file package, put the package comment in only one source file; several are concatenated.
- Example functions without an output comment are compiled but not executed.
- For a struct with exported fields, the doc comment or per-field comments should explain each field.

## Verify
`go test` runs the examples that have output comments; view the rendered result with `go doc` or on pkg.go.dev.

## Checked
2026-11-09. Read go.dev/doc/comment (syntax, headings, links, Deprecated:, gofmt, package comments) and the Examples section of pkg.go.dev/testing. Removed: the doc.go convention, `go vet` example-name check, `pkgsite` and `go doc -all` commands, and the pkg.go.dev/about source (not relevant to the claims kept).
Method: documentation only; no commands were run.
