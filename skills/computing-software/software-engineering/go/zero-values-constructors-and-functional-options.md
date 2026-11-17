---
id: computing-software.software-engineering.go.zero-values-constructors-and-functional-options
name: zero-values-constructors-and-functional-options
category: computing-software
field: software-engineering
product: go
tags: [go, functional-options, zero-values, constructors, config-struct, api-design, effective-go, go-functional-options, go-types-values]
level: practitioner
status: docs-checked
description: "Design Go types and constructors: useful zero values, New functions returning concrete types, config structs vs functional options, validation, and evolving APIs compatibly."
sources: ["https://go.dev/doc/effective_go#allocation_new", "https://go.dev/blog/module-compatibility", "https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Zero values, constructors and functional options

**Goal:** types that are easy to use correctly, hard to misuse, and can gain options
later without breaking callers.

## Make the zero value useful
Effective Go: design types so `var x T` works. `sync.Mutex`, `bytes.Buffer`, `strings.Builder`
need no constructor.
```go
type Counter struct {
    mu sync.Mutex
    m  map[string]int
}
func (c *Counter) Inc(k string) {
    c.mu.Lock(); defer c.mu.Unlock()
    if c.m == nil { c.m = make(map[string]int) }   // lazy init keeps the zero value usable
    c.m[k]++
}
```

## Constructors
`NewX` when there are invariants or required dependencies:
```go
func NewClient(baseURL string, opts ...Option) (*Client, error)
```
Return concrete types (`*Client`), accept interfaces. Return an error for invalid input rather
than panicking (except `Must*` helpers for package-level initialisation).

## Config struct
```go
type ServerConfig struct {
    Addr         string
    ReadTimeout  time.Duration   // zero means default
    MaxBodyBytes int64
}
func NewServer(cfg ServerConfig) (*Server, error)
```
Simple, discoverable, easy to load from files; adding fields is compatible. Zero-means-default
needs care when zero is a legitimate value (use pointers or explicit "unset" sentinels).

## Functional options
```go
type Option func(*Client)

func WithTimeout(d time.Duration) Option { return func(c *Client) { c.http.Timeout = d } }
func WithRetries(n int) Option         { return func(c *Client) { c.retries = n } }

func NewClient(baseURL string, opts ...Option) (*Client, error) {
    c := &Client{baseURL: baseURL, http: &http.Client{Timeout: 10 * time.Second}, retries: 2}
    for _, o := range opts { o(c) }
    if c.retries < 0 { return nil, errors.New("retries must be >= 0") }
    return c, nil
}
c, err := NewClient("https://api.example.org", WithTimeout(3*time.Second))
```
Good for libraries with many optional settings and sensible defaults; options can be added
without breaking callers. Variant: `type Option interface{ apply(*Client) }` lets options carry
names in docs and be compared. Overkill for small internal types - use a struct.

## Compatibility rules (Go blog: keeping modules compatible)
- Adding a parameter to an exported function is breaking, and the Go blog notes that bolting on a variadic
  parameter later does not work around it; take `opts ...Option` from the start, add a new function, or
  use a config struct.
- Adding a method to an exported interface breaks implementers.
- Exported struct fields can be added, but callers using unkeyed composite literals break.

## Checked
2026-10-28: Confirmed in Effective Go (useful zero value), the Go blog post on keeping modules compatible (adding a parameter breaks callers; the variadic retrofit does not work; adding interface methods breaks implementers) and the functional options article. Corrected the advice to retrofit ...Option; removed the go vet claim about unkeyed literals.
Method: documentation only; no commands were run.

## Verify
- [ ] `var x T` of exported types either works or the type is documented as constructor-only.
- [ ] Constructors validate and return errors; defaults are documented.
