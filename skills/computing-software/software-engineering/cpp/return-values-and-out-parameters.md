---
id: computing-software.software-engineering.cpp.return-values-and-out-parameters
name: return-values-and-out-parameters
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-functions, cpp-fn-returns, return-value-optimization, structured-bindings, nodiscard, out-parameters, return-values-out-params]
level: practitioner
status: docs-checked
description: "Return results from C++ functions by value, return several values in a struct or tuple, apply [[nodiscard]], and know when an out-parameter is justified."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f20-for-out-output-values-prefer-return-values-to-output-parameters", "https://en.cppreference.com/w/cpp/language/attributes/nodiscard"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Return values and out-parameters

Prefer returning by value (F.20): a return value is self-documenting, whereas an `&` parameter could be in-out or out-only and is liable to be misused. Large objects such as standard containers use implicit move operations.

```cpp
struct ParseResult { int value; std::size_t consumed; };
[[nodiscard]] ParseResult parse(std::string_view s);

auto [value, consumed] = parse("42 rest");          // structured bindings

std::vector<int> make() {
  std::vector<int> v;
  v.push_back(1);
  return v;                 // returned by value; a container moves rather than copies (F.20)
}
```

## Rules
- Multiple outputs: F.20 says use a tuple or similar multi-member type; F.21 prefers returning a struct.
- `[[nodiscard]]` (since C++17) on a function, enumeration or class: the compiler is encouraged to warn when the result is discarded, except through a cast to `void`. `[[nodiscard("reason")]]` with an unevaluated string literal explaining why is since C++20.
- Exceptions in F.20 where an out-parameter is acceptable: a type that is expensive to move (consider returning a `unique_ptr` handle, or filling a caller-supplied object), and reusing an object that carries capacity (a `std::string` or `std::vector`) across calls in an inner loop, treated as an in/out parameter.
- For non-concrete types such as types in an inheritance hierarchy, return the object by `unique_ptr` or `shared_ptr`.

## Gotchas
- A struct of many individually cheap-to-move elements might in aggregate be expensive to move (F.20 note).
- The return value optimization does not handle the assignment case (`y = m3 + m3;`), but move assignment does (F.20).

## Verify
- [ ] A test with a copy-counting type shows the copies and moves you expect on return.

## Checked
2026-11-03. Confirmed on Core Guidelines F.20 (reasons, exceptions, Matrix and Package examples) and cppreference nodiscard (C++17 form, C++20 string form, warning conditions). Removed: mandatory copy elision since C++17 and NRVO wording, the `std::move(local)` warning advice, dangling-reference warnings and compiler flags, `std::expected`, the `const T` return claim, branch-dependent NRVO, structured-binding capture note and the warning-flag check.
Method: documentation only; no commands were run.
