---
id: computing-software.game-programming.game-engine-architecture.assertions-and-verify-macros
name: assertions-and-verify-macros
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, engine-support, assertions, verify-macro, ensure, static-assert, debugging, game-programming]
level: practitioner
status: draft
description: "Use assertions in game engines: assert vs verify vs ensure semantics, debug-break macros, side effects in shipping builds, static_assert, and reporting without crashing."
sources: ["https://www.gameenginebook.com/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/asserts-in-unreal-engine", "https://en.cppreference.com/w/cpp/language/static_assert"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assertions and verify macros

## Three kinds (Unreal names, common across engines)
| Macro | Debug/dev | Shipping | Use |
|---|---|---|---|
| `check(expr)` / `ASSERT` | halts (break + crash report) | compiled out (expr NOT evaluated) | invariants that must hold; continuing would corrupt state |
| `verify(expr)` | halts | expr still evaluated, no check | when the expression has a needed side effect |
| `ensure(expr)` | logs callstack, breaks once in debugger, continues; returns the bool | expr evaluated and returned, no report | recoverable "this should not happen" |

```cpp
#if ENABLE_ASSERTS
  #define ASSERT(e) do { if (!(e)) { if (AssertFailed(#e, __FILE__, __LINE__)) DEBUG_BREAK(); } } while (0)
#else
  #define ASSERT(e) do { (void)sizeof(e); } while (0)     // not evaluated, but still type-checked
#endif
#define DEBUG_BREAK() __debugbreak()                       // MSVC; __builtin_trap()/raise(SIGTRAP) elsewhere

if (!ensure(Target != nullptr)) return;                    // ensure pattern: report and recover
```

## Rules
- **No side effects in `check`/`ASSERT`:** `check(Inventory.Remove(Item))` removes nothing in
  shipping. Use `verify` or split the call from the check.
- Prefer `ensure` (report + recover) for gameplay data issues so playtests don't crash on designer
  data; reserve hard asserts for memory/invariant corruption.
- Make the handler useful: expression text, file:line, message with values (`checkf(i < n,
  TEXT("index %d of %d"), i, n)`), callstack, and an "ignore this assert" option in debug UI.
- Report each failing ensure once per session to telemetry/crash reporter (dedupe by location).
- `static_assert` for compile-time facts: struct sizes for network/serialization, enum counts matching
  tables, alignment (`static_assert(sizeof(Packet) == 32)`).
- Assert at boundaries (function preconditions, after deserialisation), not after every line.

## Unity / C#
`UnityEngine.Assertions.Assert` calls are stripped unless `UNITY_ASSERTIONS` is defined (on in editor
and development builds). `Debug.Assert` is `[Conditional("UNITY_ASSERTIONS")]`. Set
`Assert.raiseExceptions = true` to make failures throw in tests.

## Verify
- [ ] A static-analysis or review rule flags function calls with side effects inside `check`/`ASSERT`.
- [ ] An `ensure` failure in a playtest build reaches the crash/telemetry backend once, game continues.
