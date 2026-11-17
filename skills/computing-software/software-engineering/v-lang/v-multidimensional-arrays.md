---
id: computing-software.software-engineering.v-lang.v-multidimensional-arrays
name: v-multidimensional-arrays
category: computing-software
field: software-engineering
product: v-lang
tags: [v-multidimensional-arrays, fixed-arrays-and-slices, 2d array, matrix, multidimensional, nested array, grid, init, v-lang]
level: practitioner
status: docs-checked
description: "Build 2D and 3D arrays as arrays of arrays with len and init options, index with a[i][j], and flatten with arrays.flatten."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-dimensional arrays and matrices

Goal: create grids from arrays of arrays.

- 2D: `mut a := [][]int{len: 2, init: []int{len: 3}}`; set `a[0][1] = 2`, giving `[[0, 2, 0], [0, 0, 0]]`.
- 3D: `[][][]int{len: 2, init: [][]int{len: 3, init: []int{len: 2}}}`, indexed `a[0][1][1] = 2`.
- Iterate with `for y, row in grid { for x, v in row { ... } }`. Array elements are taken by value; use `for mut` or assign through the index to change them.
- Flatten with `import arrays` then `arrays.flatten(grid)` (takes `[][]T`, returns `[]T`).

Verify: set `grid[0][0] = 1` and assert `grid[1][0] == 0`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Multidimensional Arrays", "Array `for`") and vlib/arrays/arrays.v (`flatten`). Removed as not stated: fixed 2D `[3][3]int{}`, nested literals, aliasing advice about shared row variables, and the "slice headers" remark.

Method: documentation only; no commands were run.
