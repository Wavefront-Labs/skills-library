---
id: computing-software.software-engineering.cpp.variadic-templates-fold-expressions-and-type-traits
name: variadic-templates-fold-expressions-and-type-traits
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-templates, cpp-tp-variadic, cpp-tp-traits, variadic-templates, fold-expressions, type-traits, if-constexpr, sfinae, variadic-fold-expressions, type-traits-metaprogramming]
level: advanced
status: docs-checked
description: "Write variadic templates with parameter packs and fold expressions, branch with if constexpr, and detect members with std::void_t."
sources:
  - https://en.cppreference.com/w/cpp/language/fold
  - https://en.cppreference.com/w/cpp/language/parameter_pack
  - https://en.cppreference.com/w/cpp/language/if
  - https://en.cppreference.com/w/cpp/types/void_t
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variadic templates, fold expressions and if constexpr

## Parameter packs and folds (C++17)
```cpp
template <class... Ts>
auto sum(Ts... xs) { return (xs + ... + 0); }                  // binary right fold with init
template <class... Ts>
void print_all(const Ts&... xs) { ((std::cout << xs << ' '), ...); }   // unary right fold over the comma operator
template <class... Ts> bool all_positive(Ts... xs) { return ((xs > 0) && ...); }   // unary fold, empty pack = true
template <class... Ts> constexpr std::size_t count = sizeof...(Ts);
```
- Four forms, parentheses required: `(pack op ...)` unary right, `(... op pack)` unary left, `(pack op ... op init)` binary right, `(init op ... op pack)` binary left. In a binary fold both operators must be the same.
- `(pack op ...)` expands to `E1 op (... op (EN-1 op EN))`; `(... op pack)` to `((E1 op E2) op ...) op EN`. Associativity matters for non-associative operators.
- With an empty pack a unary fold is allowed only for `&&` (true), `||` (false) and `,` (`void()`). Supply an init for other operators.
- If the pack or init expression has an operator below cast precedence at the top level it must be parenthesised: `(args + ... + (1 * 2))`.
- A pack expansion of pattern `f(args...)` or `f(&args...)` repeats the pattern per element. Inside a brace-enclosed initializer list, elements are sequenced, so `{(std::cout << args, 0)...}` calls in order.
- Expanding an empty pack yields an empty list. `sizeof...(Ts)` gives the pack length.

## if constexpr
```cpp
template <class T> std::string to_text(const T& v) {
  if constexpr (std::is_arithmetic_v<T>) return std::to_string(v);
  else if constexpr (std::is_convertible_v<T, std::string_view>) return std::string(v);
  else static_assert(dependent_false_v<T>, "unsupported type");
}
template <class> constexpr bool dependent_false_v = false;
```
- The discarded statement of an `if constexpr` inside a template is not instantiated when the condition is not value-dependent after instantiation. This allows recursion like `if constexpr (sizeof...(rs) > 0) g(rs...);`.
- Outside a template a discarded statement is still fully checked; it is not a substitute for `#if`.
- A discarded statement cannot be ill-formed for every possible specialization. `static_assert(false)` there was ill-formed before CWG2518; the type-dependent `dependent_false_v<T>` workaround is the standard fix for older compilers.
- `return` statements in a discarded statement do not take part in return type deduction.

## Detecting members with void_t
```cpp
template <class T, class = void> struct has_size : std::false_type {};
template <class T> struct has_size<T, std::void_t<decltype(std::declval<T>().size())>> : std::true_type {};
```
- `std::void_t<...>` maps any types to `void`; it is a convenient pre-C++20 SFINAE tool for detecting ill-formed types or expressions in an unevaluated context such as `decltype`. The C++20 alternative is a `requires` expression.

## Verify
- [ ] `static_assert` tests of fold results for an empty pack, one element and many.
- [ ] Instantiate the trait with a type that has the member and one that does not.

## Checked
Method: docs-checked 2026-11-09 against the cppreference fold expressions, parameter pack, if statement (constexpr if) and std::void_t pages. Corrected the fold label (init on the right is a right fold). Dropped the type-traits catalogue, perfect-forwarding example, compile-time advice and trivially-copyable notes, as the type_traits page was not read.
