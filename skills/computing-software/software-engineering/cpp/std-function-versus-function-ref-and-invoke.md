---
id: computing-software.software-engineering.cpp.std-function-versus-function-ref-and-invoke
name: std-function-versus-function-ref-and-invoke
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-functional, cpp-fu-function, cpp-fu-invoke, std-function, function-ref, move-only-function, std-invoke, bind-front, std-function-ref, invoke-bind-front]
level: practitioner
status: docs-checked
description: "Pick callable wrappers in C++: templates, std::function, move_only_function, function_ref, plus std::invoke and bind_front for member pointers."
sources: ["https://en.cppreference.com/w/cpp/utility/functional/function", "https://en.cppreference.com/w/cpp/utility/functional/invoke", "https://en.cppreference.com/w/cpp/utility/functional/bind_front"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std::function vs function_ref, invoke, bind_front

| Need | Choice | Cost |
|---|---|---|
| Algorithm taking a callback, called synchronously | template parameter `F&&` (or `std::invocable` concept) | no wrapper |
| Callback parameter, non-templated API, not stored | `std::function_ref<R(Args...)>` (C++26) | non-owning wrapper |
| Store a callable (copyable) | `std::function<R(Args...)>` | type-erased owning wrapper; needs a CopyConstructible target |
| Store move-only callable (captures `unique_ptr`) | `std::move_only_function<R(Args...) const>` (C++23) | move-only wrapper (C++23), no copy requirement |

```cpp
template <std::invocable<int> F> void for_each_id(F&& f);          // best for hot code

void run(std::function_ref<void(int)> cb);                          // non-owning wrapper
std::function<void()> task = [p = std::make_unique<Job>()]{ };     // ERROR: lambda is move-only, std::function needs copyable
std::move_only_function<void()> task2 = [p = std::make_unique<Job>()]{ (*p)(); };   // ok C++23
```

## invoke and bind_front
```cpp
std::invoke(&Widget::draw, w, 3);           // member function pointer: object first
std::invoke(&Widget::name, &w);             // data member pointers work too; also pointers/ reference_wrapper (see the invoke page)
auto f = std::bind_front(&Widget::draw, &w);  // C++20: partial application, no placeholders
f(3);
```

## Gotchas
- `std::function` calls an empty target by throwing `std::bad_function_call`; check `if (f)`.
- `function_ref` is a non-owning wrapper: do not keep one past the lifetime of the callable it refers to.
- `std::move_only_function` is C++23 and `std::function_ref` is C++26: check your standard library's support before relying on them.

## Verify
- [ ] A move-only lambda stored in `std::function` fails to compile and compiles in `std::move_only_function`.
- [ ] A `std::function` with no target throws `std::bad_function_call` when called.

## Checked
2026-11-09. Confirmed on the cppreference pages for std::function (bad_function_call on empty call, CopyConstructible requirement), std::move_only_function (C++23), std::function_ref (C++26), std::bind_front (C++20) and std::invoke. Removed as not on those pages: third-party function_ref library names, small-buffer sizes, compiler availability versions, y-combinator, advice against bind, and benchmark checks.
Method: documentation only; no commands were run.
