---
id: computing-software.software-engineering.cpp.parameter-passing-conventions
name: parameter-passing-conventions
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-interfaces, cpp-if-params, parameter-passing, const-reference, sink-parameters, string-view, span, parameter-passing-conventions]
level: practitioner
status: docs-checked
description: "Choose how C++ functions take parameters: by value, const reference, string_view/span views, sink by value plus move, non-owning pointers and when to use out-parameters."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f15-prefer-simple-and-conventional-ways-of-passing-information", "https://en.cppreference.com/w/cpp/string/basic_string_view"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter passing conventions

Core Guidelines F.15 table in practice:

| Intent | Signature |
|---|---|
| Cheap to copy, input | pass by value: `void f(int x)`, `void f(std::string_view s)` |
| Read-only, expensive to copy | `void f(const Widget& w)` |
| In/out, mutated in place | `void f(Widget& w)` |
| Will unconditionally move from the argument ("sink") | `void f(Widget&& w)` then `store(std::move(w));` (F.18) |
| Keeps a copy to store elsewhere (advanced) | `const Widget&` overload plus a `Widget&&` overload that moves it (F.16) |
| Takes ownership of a move-only owner | `void f(std::unique_ptr<Widget> p)`: by value is fine and simpler (F.18 exception) |
| Optional value | a pointer, `std::optional` or a special value (F.15 notes); a reference is assumed to refer to a valid object |

```cpp
class Person {
  std::string name_;
public:
  Person(const std::string& name) : name_(name) {}        // lvalues: copy (F.16 advanced rule)
  Person(std::string&& name) : name_(std::move(name)) {}  // rvalues: move
};
std::size_t count_a(std::string_view s);        // read-only view of characters
```

## Gotchas
- `std::basic_string_view` is a non-owning view of a contiguous character sequence; it does not own the characters, so do not keep it beyond the lifetime of the referenced data.
- Prefer returning values over out-parameters (F.20); return a struct or tuple for several outputs.
- Passing a `shared_ptr` implies a run-time cost (F.15 family of rules); take a plain reference or pointer unless the function shares or takes ownership.

## Verify
- [ ] No `string_view` parameter is stored past the call.

## Checked
2026-11-03. Confirmed on Core Guidelines F.15 (conventional ways of passing information, F.16-F.20 family) and cppreference std::basic_string_view. Fixed: the skill taught a by-value sink for strings, while F.16 marks `void f2(string s)` as potentially expensive and advises `const&` plus `&&` overloads (by value is fine for `unique_ptr`, F.18). Removed: the "<= 2 words" threshold, `span`, optional-argument and `not_null` rows, string-literal temporary claim, sink-cost claim, top-level const note, and the clang-tidy and AddressSanitizer checks.
Method: documentation only; no commands were run.
