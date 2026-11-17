---
id: computing-software.software-engineering.cpp.mdspan-multidimensional-views
name: mdspan-multidimensional-views
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-modern, cpp-mo-mdspan, mdspan, multidimensional-array, layout-mapping, submdspan, extents]
level: advanced
status: docs-checked
description: "Use C++23 std::mdspan for non-owning multidimensional views over contiguous data: extents, layouts, indexing with operator[], submdspan, and library support caveats."
sources: ["https://en.cppreference.com/w/cpp/container/mdspan", "https://en.cppreference.com/w/cpp/container/mdspan/extents"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mdspan

`std::mdspan<T, Extents, Layout, Accessor>` (C++23, `<mdspan>`) views a flat buffer as an N-dimensional array without owning or copying it.

```cpp
#include <mdspan>
#include <vector>
std::vector<double> data(3 * 4);
std::mdspan m(data.data(), 3, 4);                    // CTAD: dynamic extents, row-major (layout_right)
m[1, 2] = 5.0;                                        // multidimensional operator[] (C++23)
for (std::size_t i = 0; i != m.extent(0); ++i)
  for (std::size_t j = 0; j != m.extent(1); ++j)
    m[i, j] = double(i * m.extent(1) + j);

std::mdspan<double, std::extents<std::size_t, 3, 4>> fixed(data.data());   // static extents known at compile time
std::mdspan<double, std::dextents<std::size_t, 2>, std::layout_left> col(data.data(), 3, 4);   // column-major (Fortran)
```

## Layouts and views
- `layout_right` (row-major, rightmost extent has stride 1; the default), `layout_left` (column-major, leftmost extent has stride 1), `layout_stride` (user-defined strides); custom layouts implement the layout mapping policy requirements.
- `std::submdspan` is C++26 and takes slice specifiers such as `std::full_extent`, e.g. `submdspan(m, 1, std::full_extent)` for row 1; `std::strided_slice` (C++26) selects regularly spaced indices.
- Each mdspan specialization is copyable with nothrow move and swap, so pass it by value like `span`; it is trivially copyable when its accessor, mapping and data handle types are.
- Accessors customise element access: `std::default_accessor` (C++23), `std::aligned_accessor` (C++26).
- Observers: `rank()`, `extent(i)`, `size()`, `empty()`, `stride(i)`, `mapping()`, `data_handle()`, `is_unique()`, `is_exhaustive()`, `is_strided()`.

## Gotchas
- `std::mdspan` is C++23 (feature-test macro `__cpp_lib_mdspan`); `submdspan` is C++26 (`__cpp_lib_submdspan`). Check the standard library's version support before relying on either.
- `operator[]` does no bounds checking; the bounds-checked `at()` is C++26. Add your own asserts until then.
- It does not own memory: the buffer must outlive the view.
- Each extent is either static (a value representable in `IndexType`) or `std::dynamic_extent`; pick an `IndexType` wide enough for the total size.
- Loop order should follow layout (innermost index = the stride-1 dimension) for cache efficiency.

## Verify
- [ ] Test that `m.stride(1)` and `m.mapping()(i, j)` match the expected offsets for both layouts.
- [ ] Benchmark row-major traversal against column-major to confirm loop order matches layout.

## Checked
2026-11-08. Confirmed on cppreference std::mdspan (template parameters and default layout_right/default_accessor, layout stride definitions, observers, C++23/26 markers, feature-test macros, copy/trivially-copyable rules) and std::extents/dextents (static versus dynamic extent, dextents alias). Removed: Kokkos reference implementation advice, per-compiler version support, hardened libc++ remark, `m(i, j)` call form and the `-std=c++23` flag detail (not on the pages read).
Method: documentation only; no commands were run.
