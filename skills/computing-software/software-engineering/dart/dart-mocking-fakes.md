---
id: computing-software.software-engineering.dart.dart-mocking-fakes
name: dart-mocking-fakes
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-testing, mocking-fakes]
level: practitioner
status: docs-checked
description: "Use fakes or mocktail/mockito for dependencies and verify interactions."
sources: ["https://pub.dev/packages/mocktail", "https://pub.dev/packages/mockito", "https://pub.dev/packages/fake_async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mocking with mocktail and mockito
- mocktail needs no manual mocks or code generation: `class MockCat extends Mock implements Cat {}`; stub with `when(() => cat.sound()).thenReturn('meow')` (the call is wrapped in a closure), `thenAnswer((_) => ...)` or `thenThrow(...)`; `verify(() => cat.likes('fish')).called(1)`.
- Argument matchers in mocktail: `any()` for positional arguments, `any(named: 'isHungry')` for named ones, `any(that: matcher)` for a custom matcher; call `registerFallbackValue(FakeFood())` for custom types used with `any()`.
- mockito 5 uses code generation: annotate with `@GenerateNiceMocks([MockSpec<Cat>()])`, add `build_runner` to `dev_dependencies`, and run `dart run build_runner build`. Its stubs are not closures: `when(cat.sound()).thenReturn('Purr')`. Use `thenAnswer` to stub methods returning a `Future` or `Stream`; stubbing and verifying only work on the generated mock instance, not the real class.
- `fake_async` provides `fakeAsync((async) { ... })` to control timers and microtasks without real waiting; `DateTime.now()` and `Stopwatch` are controlled only if created through the `clock` package (`clock.now()`, `clock.stopwatch()`).
- Prefer hand-written fakes for simple interfaces and verify behaviour more than call counts (judgement, not from these pages).

Verify: the test fails when the dependency is not called.

## Checked

Checked 2026-11-08 against the pub.dev package pages of mocktail, mockito and fake_async (README text read). Removed: the claim that `registerFallbackValue` is needed for every `any()` (narrowed to custom types).

Method: documentation only; no commands were run.
