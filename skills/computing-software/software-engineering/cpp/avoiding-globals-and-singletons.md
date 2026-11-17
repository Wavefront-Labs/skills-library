---
id: computing-software.software-engineering.cpp.avoiding-globals-and-singletons
name: avoiding-globals-and-singletons
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-interfaces, cpp-if-globals, global-state, singleton, static-initialization-order, dependency-injection, magic-statics, avoid-globals-singletons]
level: practitioner
status: docs-checked
description: "Replace global state and singletons in C++ with injected dependencies, and tame the static initialization order fiasco with function-local statics and constinit."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#i2-avoid-non-const-global-variables", "https://en.cppreference.com/w/cpp/language/siof", "https://en.cppreference.com/w/cpp/language/storage_duration", "https://en.cppreference.com/w/cpp/language/constinit", "https://en.cppreference.com/w/cpp/language/inline"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding globals and singletons

Core Guidelines I.2 (avoid non-const globals) and I.3 (avoid singletons). Non-const globals hide dependencies and make them subject to unpredictable changes (I.2), and a pointer or reference to mutable data is a potential data race. Singletons are "complicated global objects in disguise" (I.3).

## Inject instead
```cpp
class Logger { public: virtual void write(std::string_view) = 0; virtual ~Logger() = default; };

class Service {
  Logger& log_;                                  // dependency visible in the constructor
public:
  explicit Service(Logger& log) : log_(log) {}
  void run() { log_.write("start"); }
};
// production: Service s{file_logger};  test: Service s{capturing_logger};
```

## When a global is unavoidable
- **Constants**: `inline constexpr int kMax = 64;` (C++17 inline variable, one definition across TUs).
- **Lazy singleton**: a function-local static is initialised thread-safely on first call (C++11 "magic statics") and avoids the static initialization order fiasco between translation units:
```cpp
Config& config() { static Config c = load(); return c; }
```
- **Guaranteed compile-time init**: `constinit` (C++20) on namespace-scope variables rejects dynamic initialisation: `constinit std::atomic<int> counter{0};`.
- If destroying the object needs synchronisation, I.3 shows a deliberately leaked pointer (`static auto p = new X{3}; return *p;`), but it is error-prone: use it only for multi-threaded code whose object must be destroyed and whose destructor needs synchronising.

## Gotchas
- Order of initialisation across translation units is ambiguous (the static initialization order fiasco): a global in one file relying on a global from another can crash. Within one translation unit, objects are initialised top to bottom.
- Thread-safe initialisation does not make later access thread-safe; guard mutation with a mutex or use `std::atomic`.
- `thread_local` is still global state: there is a distinct object per thread.
- Singletons with `getInstance()` are hard to mock; if you keep one, expose it behind an interface and inject it.

## Verify
- [ ] A review (the I.2 enforcement rule) finds no non-const variables at namespace scope, and no global pointers or references to non-const data, outside approved files.

## Checked
2026-11-09. Confirmed on the C++ Core Guidelines (I.2, I.3), cppreference storage duration, constinit and inline specifier pages: static initialisation order fiasco, constinit guaranteeing constant initialisation, inline variables and function-local statics being initialised once on first use. Removed as not on those pages: reverse destruction order claims, thread_local cost figures, nm and gtest_shuffle advice, and zero-initialised memory claims.
Method: documentation only; no commands were run.
