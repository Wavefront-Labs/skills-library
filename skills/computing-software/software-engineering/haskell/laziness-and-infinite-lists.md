---
id: computing-software.software-engineering.haskell.laziness-and-infinite-lists
name: laziness-and-infinite-lists
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, infinite-lists, iterate, cycle, takewhile, lazy-evaluation, knot-tying, fibs, laziness-and-infinite-lists]
level: practitioner
status: draft
description: "Build and consume infinite lists with iterate, cycle, repeat and takeWhile, recursive definitions like fibs, and avoid forcing them with length or show."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Infinite lists and lazy patterns

**Goal:** use laziness productively and know what forces a whole list.

```haskell
nats    = [0..]
evens   = filter even nats
powers  = iterate (* 2) 1                         -- 1,2,4,8,...
fibs    = 0 : 1 : zipWith (+) fibs (tail fibs)    -- self-referential, memoised by sharing
primes  = sieve [2..] where sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
take 10 (cycle [1,2,3])
takeWhile (< 100) (map (^ 2) [1..])
```

## Rules
- Evaluation is by need: an expression is evaluated only when its value is demanded by pattern matching,
  arithmetic or IO.
- A shared binding (`fibs` above, a CAF) is evaluated once; a function call recomputes. Use a top-level
  list to memoise: `memo = map f [0..]; f n = memo !! (n - 1) + ...` (list indexing is O(n), prefer an array or `Data.Map` for real use).
- `zip [0..] xs` is the idiom for indexing; it needs no length.

## Failure modes
- `length`, `sum`, `last`, `reverse`, `show` and `print` on an infinite list never terminate.
- Holding the head of a huge lazy list (a CAF referenced later) keeps all elements alive: a space leak.
- `foldl` on an infinite list never returns; `foldr` with a lazy combinator can.
- Exceptions inside lazy values surface where forced, not where created.

## Self-check
- [ ] `take 10 fibs` returns `[0,1,1,2,3,5,8,13,21,34]` in GHCi.
- [ ] No terminal operation (length, sum) is applied to an unbounded list.
