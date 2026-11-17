---
id: computing-software.software-engineering.swift.swift-subscripts
name: swift-subscripts
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-types, subscripts]
level: intro
status: docs-checked
description: "Define subscripts on types, with multiple parameters, get/set and static subscripts, and avoid unchecked indexing traps."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/subscripts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subscripts
A subscript is a shortcut for reading and writing a type's members by key or index. Classes, structs and enums can define them, and they may take several parameters of any type.

```swift
struct Grid {
    let rows: Int, columns: Int
    private var cells: [Double]
    init(rows: Int, columns: Int) {
        self.rows = rows; self.columns = columns
        cells = Array(repeating: 0, count: rows * columns)
    }
    func indexIsValid(row: Int, column: Int) -> Bool {
        (0..<rows).contains(row) && (0..<columns).contains(column)
    }
    subscript(row: Int, column: Int) -> Double {
        get { precondition(indexIsValid(row: row, column: column)); return cells[row * columns + column] }
        set { precondition(indexIsValid(row: row, column: column)); cells[row * columns + column] = newValue }
    }
}
var g = Grid(rows: 2, columns: 2)
g[0, 1] = 3.5
```

- Subscripts are read-write or read-only. A read-only subscript can drop the `get` keyword and its braces: `subscript(i: Int) -> Int { i * 2 }`.
- In the setter, `newValue` is provided by default and has the same type as the subscript's return value.
- Like functions, subscripts can take variadic parameters and default values, but they cannot use in-out parameters.
- A type can define several subscripts; the one used is chosen by the types of the values in the brackets (subscript overloading).
- Add `static subscript` for type-level lookups (an enum case table, for example). A class can write `class subscript` instead so subclasses may override it.

Gotcha: `Dictionary` uses a subscript that takes and returns an optional, so a missing key is nil and assigning nil removes the entry. An array-style subscript instead traps on bad input, as the book's `Matrix` does with `assert`. Pick one convention and document it; do not mix.

Verify: build a small test that reads and writes `g[0, 1]`, and confirm an out-of-range index fails deliberately (precondition) rather than reading adjacent cells.

## Checked
2026-11-08: read the whole Subscripts chapter of The Swift Programming Language (swift-book source on GitHub). Confirmed: get/set and read-only syntax, default `newValue`, no in-out parameters, variadic and default parameters, overloading, multi-parameter `Matrix` example with assertions, `static` and `class` type subscripts, optional-returning `Dictionary` subscript. Removed: the claims that labels are absent by default, that subscripts can be generic, and that `Array` traps (not on this page).
Method: documentation only; no commands were run.
