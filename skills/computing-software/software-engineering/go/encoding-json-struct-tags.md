---
id: computing-software.software-engineering.go.encoding-json-struct-tags
name: encoding-json-struct-tags
category: computing-software
field: software-engineering
product: go
tags: [go, go-stdlib, encoding-json, json-struct-tags, omitempty, json-decoding, custom-marshaler, go-encoding, go-json-marshalers, go-json-decoder]
level: practitioner
status: verified
description: "Encode and decode JSON in Go correctly: struct tags, omitempty vs omitzero, pointers for optional fields, strict decoding, custom marshalers, numbers and streaming."
sources:
  - https://pkg.go.dev/encoding/json
  - https://go.dev/blog/json
  - https://go.dev/doc/go1.24#encodingjson
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# encoding/json and struct tags

**Goal:** JSON payloads that map cleanly to Go types, reject bad input, and do not silently lose data.

## 1. Tags
```go
type Order struct {
    ID        string     `json:"id"`
    Customer  string     `json:"customer_id"`
    Note      string     `json:"note,omitempty"`        // omitted if ""
    Discount  *int       `json:"discount,omitempty"`    // nil = absent; 0 is sent
    CreatedAt time.Time  `json:"created_at,omitzero"`   // Go 1.24: omit zero time (omitempty never omits structs)
    Total     int64      `json:"total,string"`          // encode number as JSON string (JS precision)
    Internal  string     `json:"-"`                     // never serialised
    lines     []Line                                   // unexported: ignored
}
```
- Only exported fields are (un)marshalled.
- `omitempty` omits false, 0, "", nil pointers/maps/slices and empty maps/slices; it does **not** omit zero structs. `omitzero` uses the zero value or an `IsZero()` method.
- To tell "absent" from "zero" on input, use pointer fields (or a custom optional type).

## 2. Strict decoding at API boundaries
```go
dec := json.NewDecoder(http.MaxBytesReader(w, r.Body, 1<<20))
dec.DisallowUnknownFields()
var in CreateOrder
if err := dec.Decode(&in); err != nil { return badRequest(err) }
if dec.More() { return badRequest(errors.New("trailing data")) }
```
Default `Unmarshal` ignores unknown fields and matches keys **case-insensitively** (`"ID"`, `"Id"` both fill `ID`); be aware when security-relevant fields exist.

## 3. Numbers
- Decoding into `interface{}`/`any` produces `float64`: integers above 2^53 lose precision. Use concrete types, or `dec.UseNumber()` to get `json.Number`.
- `int` fields reject `1.5` with an `UnmarshalTypeError`.

## 4. Custom marshalling
```go
type Status int
func (s Status) MarshalText() ([]byte, error) { return []byte(s.String()), nil }   // used for values and map keys
func (s *Status) UnmarshalText(b []byte) error { v, ok := parseStatus(string(b)); if !ok { return fmt.Errorf("bad status %q", b) }; *s = v; return nil }
```
Implement `MarshalJSON`/`UnmarshalJSON` for full control; inside, convert to an alias type to avoid infinite recursion:
```go
func (o Order) MarshalJSON() ([]byte, error) {
    type alias Order
    return json.Marshal(struct{ alias; Kind string `json:"kind"` }{alias(o), "order"})
}
```
`json.RawMessage` defers decoding of polymorphic sub-documents until a discriminator field is read.

## 5. Streaming
`json.NewEncoder(w).Encode(v)` writes directly to the response (adds a newline). For large arrays, decode token by token with `dec.Token()` + `dec.More()`.

## Gotchas
- nil slice encodes as `null`, empty slice as `[]`; initialise slices if clients expect arrays.
- `map[string]any` output has sorted keys; struct output follows field order.
- HTML characters are escaped (`<` -> `<`) by default; `enc.SetEscapeHTML(false)` for non-HTML contexts.
- `encoding/json/v2` (experimental, `GOEXPERIMENT=jsonv2` in Go 1.25) changes defaults (case-sensitive, nil slices as `[]`); watch for migration.

## Verify
- Round-trip tests with golden JSON files, and negative tests: unknown fields, wrong types, oversized bodies and trailing data all return 400.

## Checked
- Go 1.25.1: tag behaviours (`omitempty` keeps a zero `time.Time` and a zero struct while `omitzero` drops the time, `,string` on int64, `-`, unexported field ignored), case-insensitive key matching (last of `ID`/`Id` wins), `DisallowUnknownFields` error, `dec.More()` seeing trailing data, `any` decoding a large integer as `float64` (precision lost) versus `UseNumber`, `UnmarshalTypeError` for `1.5` into `int`, `MarshalText`/`UnmarshalText` for values and map keys, the `alias` pattern for `MarshalJSON`, nil slice `null` versus `[]`, sorted map keys, HTML escaping and `SetEscapeHTML(false)`, `json.RawMessage` and `Token`; with `GOEXPERIMENT=jsonv2` `encoding/json/v2` encodes a nil slice as `[]` and matches field names case-sensitively, and without it the package is not importable. `MaxBytesReader` and the HTTP handler were not run.
