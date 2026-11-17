---
id: computing-software.software-engineering.go.range-over-func-iterators
name: range-over-func-iterators
category: computing-software
field: software-engineering
product: go
tags: [go, range-over-func, iter-seq, iterators, slices-package, maps-package, go-generics, go-iterators, go-iter-pull, go-iter-composition]
level: practitioner
status: verified
description: "Write and use Go 1.23 iterators: iter.Seq and Seq2 functions, honouring yield's return value, pull iterators, slices/maps helpers, and when a slice is still simpler."
sources: ["https://go.dev/blog/range-functions", "https://pkg.go.dev/iter", "https://go.dev/ref/spec#For_range", "https://pkg.go.dev/slices"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Range-over-func iterators

**Goal:** expose sequences (DB rows, tree nodes, paginated API results) to `for range`
without materialising slices or leaking goroutines.

## The shapes
```go
type Seq[V any]     func(yield func(V) bool)
type Seq2[K, V any] func(yield func(K, V) bool)
```
A push iterator calls `yield` for each element and must stop when `yield` returns false
(the loop body did `break`/`return`).

## Writing one
```go
func (t *Tree[T]) All() iter.Seq[T] {
    return func(yield func(T) bool) {
        t.walk(t.root, yield)
    }
}
func (t *Tree[T]) walk(n *node[T], yield func(T) bool) bool {
    if n == nil { return true }
    return t.walk(n.left, yield) && yield(n.val) && t.walk(n.right, yield)
}

for v := range tree.All() {
    if v > 100 { break }          // yield returns false; walk unwinds
}
```
Calling `yield` again after it returned false panics at runtime ("range function continued
iteration after function for loop body returned false").

## Resource-backed iterators
```go
func (s *Store) Users(ctx context.Context) iter.Seq2[User, error] {
    return func(yield func(User, error) bool) {
        rows, err := s.db.QueryContext(ctx, "SELECT id, name FROM users")
        if err != nil { yield(User{}, err); return }
        defer rows.Close()                     // runs even if the consumer breaks early
        for rows.Next() {
            var u User
            if err := rows.Scan(&u.ID, &u.Name); err != nil { yield(User{}, err); return }
            if !yield(u, nil) { return }
        }
        if err := rows.Err(); err != nil { yield(User{}, err) }
    }
}
```
`Seq2[T, error]` is the common pattern for fallible streams.

## Standard library helpers
```go
for i, v := range slices.All(xs) {}
keys := slices.Sorted(maps.Keys(m))          // deterministic map iteration
for v := range slices.Values(xs) {}
chunks := slices.Chunk(xs, 100)               // Go 1.23
for line := range strings.Lines(text) {}      // Go 1.24
```

## Pull iterators
When you need to advance two sequences in lockstep:
```go
next, stop := iter.Pull(seqA)
defer stop()                                   // always: releases the coroutine
for b := range seqB { a, ok := next(); if !ok { break }; merge(a, b) }
```

## When not to
If callers need length, random access or multiple passes, return a slice. Iterators shine for
large/unbounded/lazy sequences and composable adapters (filter/map), which you can write as
small generic functions.

## Verify
- [ ] Every iterator checks yield's result and stops; resources released via defer.
- [ ] Tests break out of the loop early and confirm cleanup (e.g. rows closed).

## Checked
2026-10-21 on Go 1.27.3 (Windows): `Tree.All` with an early `break`; calling `yield` after it returned false panics with `runtime error: range function continued iteration after function for loop body returned false`; the rows-backed `Seq2[User, error]` (modernc sqlite) released its connection after the consumer broke out (`InUse` 0); `slices.All/Values/Sorted/Collect/Chunk`, `maps.Keys`, `strings.Lines` and `iter.Pull` with `defer stop()` produced the expected output; `slices.Chunk` is listed in https://go.dev/doc/go1.23 and `strings.Lines` in https://go.dev/doc/go1.24.
