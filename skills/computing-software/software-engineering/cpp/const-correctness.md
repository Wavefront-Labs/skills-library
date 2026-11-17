---
id: computing-software.software-engineering.cpp.const-correctness
name: const-correctness
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-expressions, cpp-ex-const, const-correctness, const-member-functions, mutable, thread-safety, east-const]
level: practitioner
status: docs-checked
description: "Apply const consistently in C++: const members, const references, mutable caches and constness not being transitive."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con-constants-and-immutability", "https://en.cppreference.com/w/cpp/language/cv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Const correctness

Make everything `const` that can be (Con.1-5): variables, parameters passed by reference, member functions that do not change observable state.

```cpp
class Account {
  std::string id_;
  mutable std::mutex m_;               // mutable: lockable inside const methods
  double balance_ = 0;
public:
  const std::string& id() const { return id_; }
  double balance() const { std::lock_guard g{m_}; return balance_; }
  void deposit(double x) { std::lock_guard g{m_}; balance_ += x; }
};
const auto limit = compute_limit();     // locals: const by default, remove only when mutated
```

## Guidelines
- Mark a member function `const` unless it changes the object's observable state (Con.2); a plain `T*` or `T&` parameter tells readers the function modifies the object (Con.3).
- `mutable` members can change inside `const` functions; cppreference says it is for members that do not affect externally visible state, such as mutexes, memo caches and lazy evaluation (the "M&M rule": mutable and mutex go together).
- Constness is not transitive: a `const` member function can change `mutable` members and objects reached through non-const pointers, so the class must keep such mutation within its invariants.
- Use `constexpr` for values computable at compile time (Con.5) and `const` for objects whose value does not change after construction (Con.4).

## Gotchas
- Modifying a const object through a pointer or reference to non-const is undefined behaviour: `const_cast<int&>(r2) = 2` on a const object is UB on cppreference, while the same cast on a reference to a non-const object is fine.
- Wrapping a const-incorrect old API with `const_cast` is a patch for code you cannot change (Con.2); update the library when you can.

## Verify
- [ ] The clang-tidy check `misc-const-correctness` reports no findings in new code.
- [ ] Calling each getter on a `const Account&` compiles.

## Checked
2026-11-03. Confirmed on Core Guidelines Con.1-Con.5 (Con.2 notes on mutable and non-transitive constness) and cppreference cv (mutable specifier, M&M rule, const_cast undefined behaviour), and the `misc-const-correctness` check in the clang-tidy list. Removed: the pointer-declaration reading rules, the claim that const methods must be thread-safe by a standard-library assumption, advice not to return `const T` by value, `std::span<const T>` and `propagate_const` as deep constness, the const/non-const overload trick, static const members, top-level const parameters, `const Widget w;`, reference members blocking assignment, the clang-tidy 15 version claim and the ThreadSanitizer step.
Method: documentation only; no commands were run.
