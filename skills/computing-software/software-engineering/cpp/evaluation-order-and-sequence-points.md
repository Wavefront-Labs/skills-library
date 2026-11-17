---
id: computing-software.software-engineering.cpp.evaluation-order-and-sequence-points
name: evaluation-order-and-sequence-points
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-expressions, cpp-ex-order, evaluation-order, sequenced-before, unsequenced, undefined-behavior, function-arguments, evaluation-order-sequencing]
level: advanced
status: docs-checked
description: "Know which C++ subexpression orders are guaranteed (C++17 changes), spot unsequenced modifications and argument-order bugs, and restructure code to avoid them."
sources: ["https://en.cppreference.com/w/cpp/language/eval_order", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es44-dont-depend-on-order-of-evaluation-of-function-arguments"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluation order and sequencing

## What is guaranteed
- `a && b`, `a || b`, `a ? b : c`, and the comma operator: left operand fully evaluated first.
- Sequenced-before rules on cppreference: `E1[E2]` evaluates E1 first, `E1 << E2` and `E1 >> E2` evaluate E1 first, in `E1 = E2` and `E1 @= E2` E2 is sequenced before E1, and in a function call the expression naming the function is sequenced before every argument. Core Guidelines ES.44: in C++17 `cout << f1() << f2();` works left to right and `f1() = f2();` evaluates `f2()` first (undefined behaviour in C++14). The operator rules also hold for overloaded operators in operator notation.
- A `new` expression: the allocation function call is sequenced before the evaluation of the constructor arguments since C++17 (indeterminately sequenced before).
- **Not guaranteed (still)**: the order in which **function arguments** are evaluated (`f(g(), h())`), and operands of most operators (`a() + b() + c()`: operator associativity does not fix runtime order). Each parameter initialization is indeterminately sequenced against the others: they may not overlap, but any order is allowed.

```cpp
int i = 0;
int a[3] = {};
a[i] = i++;          // undefined behaviour until C++17 (cppreference); do not write this
f(++i, ++i);          // undefined until C++17; since C++17 f(1, 2) or f(2, 1), unspecified which
cout << f1() << f2(); // left to right since C++17 (ES.44)
auto p = std::make_unique<T>(a(), b());   // a and b are function arguments: order unspecified
```

## Unsequenced modification = UB
A side effect on a memory location that is unsequenced relative to another side effect or a value computation on the same location is undefined behaviour. cppreference examples: `i = ++i + i++;` and `n = ++i + i;` are undefined; `i = ++i + 2;` is well-defined; `i = i++ + 2;` was undefined until C++17.

## Rules of thumb
1. One side effect per statement; separate calls with named temporaries:
```cpp
auto x = g(); auto y = h(); f(x, y);
```
2. Never pass two calls that depend on each other's side effects as arguments of the same call or operator.

## Gotchas
- The compiler may choose another order when the same expression is evaluated again, so a passing test proves little.
- Overloaded operators obey the sequencing rules of the built-in operator when called with operator notation; called as a function (`operator<<(a, b)`) they follow function-call rules.

## Verify
- [ ] clang-tidy `bugprone-inc-dec-in-conditions` passes.
- [ ] Run the same test compiled with GCC and Clang: identical output.

## Checked
2026-11-03. Confirmed on cppreference Order of evaluation (rules 1-21, undefined-behaviour examples, `a() + b() + c()` note) and Core Guidelines ES.44 (C++17 left-to-right `<<`, `f1() = f2()`, `f(++i, ++i)`). Fixed: `i = i++ + 1` was claimed undefined in all standards (cppreference: `i = i++ + 2` is undefined only until C++17), and the `a[i++] = i` comment ("a[0] = 1") was wrong. Removed: GCC/Clang/MSVC warning flags and compiler-difference claims, the shared_ptr leak rule, the `bugprone-unsequenced` check name (not in the clang-tidy list), the optimisation-level claim.
Method: documentation only; no commands were run.
