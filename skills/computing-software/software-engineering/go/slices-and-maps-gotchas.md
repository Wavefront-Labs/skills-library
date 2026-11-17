---
id: computing-software.software-engineering.go.slices-and-maps-gotchas
name: slices-and-maps-gotchas
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-slices, slice-aliasing, append, nil-map, map-iteration-order, slice-capacity, full-slice-expression, concurrent-map-writes, go-composite-types, go-slice-aliasing, go-map-semantics, go-slices-maps-pkg]
level: practitioner
status: verified
description: "Avoid Go slice and map bugs: append aliasing, capacity and the full slice expression, memory retention from subslices, nil maps, iteration order and concurrent access."
sources: ["https://go.dev/blog/slices-intro", "https://go.dev/blog/slices", "https://go.dev/blog/maps", "https://go.dev/ref/spec#Slice_expressions"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Slices and maps gotchas

**Goal:** know exactly when two slices share memory and when a map will panic, which is
where most surprising Go bugs come from.

## Slices share backing arrays
A slice is (pointer, len, cap). Slicing and assigning copy the header, not the data.
```go
a := []int{1, 2, 3, 4}
b := a[:2]          // len 2, cap 4, same array
b = append(b, 99)   // fits in cap: OVERWRITES a[2]; a is now [1 2 99 4]
```
- Whether `append` reallocates depends on capacity, so behaviour changes with data size.
- Protect a subslice you hand out with the full slice expression:
  `b := a[:2:2]` (cap = 2) forces the next append to copy.
- Need an independent copy: `c := slices.Clone(a)` or `append([]int(nil), a...)`.
- Functions that modify a slice they receive and also append must RETURN the new slice
  (`s = addItem(s, x)`); the caller's header does not change otherwise.

## Memory retention
`small := big[:10]` keeps the whole `big` array alive. Copy small results out of large
buffers (file contents, network reads) before keeping them.

## Loop variables
Since Go 1.22 each iteration has a fresh variable; `&v` in `for _, v := range` is safe.
On go < 1.22 (check `go.mod`'s `go` line) it is the same variable every iteration.
`for _, v := range items { v.Count++ }` modifies a COPY; use `items[i].Count++`.

## Maps
- A nil map reads fine and panics on write: `var m map[string]int; m["x"] = 1` panics.
  Initialise with `make` or a literal.
- Iteration order is randomised on purpose; sort keys (`slices.Sorted(maps.Keys(m))`) for
  deterministic output, tests and golden files.
- Map values are not addressable: `m["k"].Field = 1` doesn't compile; store pointers or
  read-modify-write.
- Concurrent map write = fatal error `concurrent map writes` (not recoverable). Guard
  with `sync.RWMutex` or use `sync.Map` for append-only/disjoint-key caches.
- Deleting during range is allowed.
- Maps never shrink after deletes; recreate a map that grew huge and then emptied.

## nil vs empty slices
`var s []int` (nil) and `[]int{}` both have len 0 and range fine, but encode to JSON as
`null` vs `[]`. Return `[]T{}` from APIs where clients expect an array.

## Verify
- [ ] `go test -race` passes (catches concurrent map access).
- [ ] Functions that append to an argument return the slice and callers use the result.

## Checked
- Go 1.25.1: the shared-array `append` overwrite (`[1 2 99 4]`), `a[:2:2]` forcing a copy, `slices.Clone` and `append([]int(nil), a...)` independence, an `append` without returning the slice leaving the caller's header unchanged, `range` value copies versus `items[i]`, nil map reads and the write panic `assignment to entry in nil map`, `slices.Sorted(maps.Keys(m))`, deleting during range, JSON `null` versus `[]`, and `fatal error: concurrent map writes` from eight goroutines. `go test -race` was not run (cgo); memory retention and map-shrink notes are runtime documentation, not measured here.
