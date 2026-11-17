---
id: computing-software.software-engineering.d.d-array-insert-replace-slice
name: d-array-insert-replace-slice
category: computing-software
field: software-engineering
product: d
tags: [d-array-insert-replace-slice, std-array, insertinplace, replace, replaceinplace, replacefirst, popback, array-edit, insert, splice, d]
level: practitioner
status: docs-checked
description: "Edit arrays with insertInPlace, replace, replaceInPlace, replaceFirst, popFront/popBack, back, and slicing helpers such as takeOne, array bounds and shrinking length."
sources:
  - https://dlang.org/phobos/std_array.html
  - https://dlang.org/phobos/std_algorithm_mutation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inserting, replacing and slicing: insertInPlace, replace, replaceInPlace, popBack

Goal: change contents without off-by-one bugs.

- `arr.insertInPlace(pos, a, b)` inserts the items (or an input range) at index `pos`.
- `replaceInPlace(arr, from, to, stuff)` replaces the elements at indices `[from, to)` with `stuff` and expands or shrinks the array as needed; `replace(arr, from, to, stuff)` returns a new array instead.
- Text: `replace(s, "old", "new")` (all occurrences, new array), `replaceFirst`, `replaceLast`, `replaceSlice(s, slice, repl)`; `std.string.translate` for character maps.
- Remove: `std.algorithm.remove(arr, i)` keeps order (the default `SwapStrategy.stable`); `remove!(SwapStrategy.unstable)(arr, i)` does not keep order. Assign the result: `arr = arr.remove(i);`.
- `popBack()` and `popFront()` (std.range.primitives) shorten the slice variable.
- Sorted insertion: `arr.insertInPlace(arr.assumeSorted.lowerBound(x).length, x)`.

Gotchas:
- `remove` does not change the length of the original range; use its return value.

Verify: unittest checks the array before and after for insert at 0, middle, and end.

## Checked

2026-11-03. Confirmed against: std.array and std.algorithm.mutation reference pages.

Removed because the pages read did not confirm it: 'O(1) swap with last' for unstable `remove`, 'stomp or detach' for shared slices, 'tail beyond is undefined', `arr[a .. b] = chunk[]` and `.dup` generic remarks.

Method: documentation only; no commands were run.
