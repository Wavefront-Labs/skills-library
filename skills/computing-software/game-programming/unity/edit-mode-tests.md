---
id: computing-software.game-programming.unity.edit-mode-tests
name: edit-mode-tests
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-test-framework, edit-mode-tests, nunit, test-runner, unit-testing, testcase, game-programming]
level: practitioner
status: docs-checked
description: "Unity Test Framework 1.4 Edit Mode tests: assembly definition conditions, Test versus UnityTest, Edit versus Play Mode, NUnit attribute reference and known UnityTest limitations."
sources: ["https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/edit-mode-vs-play-mode-tests.html", "https://docs.nunit.org/articles/nunit/writing-tests/attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edit Mode tests

**Goal:** set up Edit Mode tests in the Unity Test Framework (UTF) and choose the right attributes.

## What UTF is
- Tests code in Edit Mode, Play Mode and on target platforms (Standalone, Android, iOS...). It is the
  toolset formerly known as Unity Test Runner, now a package (`com.unity.test-framework`, shipped with the
  Editor and included in projects created with Unity 2019.2 or later). It uses a Unity integration of
  NUnit; the 1.4 index page states NUnit 3.5. The package is compatible with Editor 2019.2 and later.

## Edit Mode tests
- Also called Editor tests: run only in the Unity Editor and can access Editor code as well as game code.
  Page says it is possible to test Editor extensions using the `UnityTest` attribute; test code runs in
  the `EditorApplication.update` callback loop. A test can also control entering and exiting Play Mode.
- They should meet one of: an assembly definition referencing `nunit.framework.dll` with only the Editor
  as target platform (`"includePlatforms": ["Editor"]`), or (legacy) tests placed in the project's `Editor`
  folder.
- Test assemblies can reference `UnityEngine.TestRunner` and `UnityEditor.TestRunner` in their Assembly
  Definition References; the latter is only available in Edit Mode.

## Play Mode tests (for contrast)
Run standalone in a Player or inside the Editor. With `UnityTest` they run as coroutines. Need an
assembly definition referencing `nunit.framework.dll`, test scripts in the folder with the `.asmdef`, and a
reference to the assembly under test.

## Attribute choice
Use the NUnit `Test` attribute instead of `UnityTest`, unless you need to yield special instructions in
Edit Mode, or need to skip a frame or wait for some time in Play Mode.

## NUnit attributes (reference table, selected)
Marked in the table: `Test`, `TestCase` (method with parameters, inline arguments), `TestCaseSource`,
`TestFixture`, `SetUp` (before each test), `TearDown` (after each test), `OneTimeSetUp` (once before any
child tests), `OneTimeTearDown`, `Category`, `Ignore` ("shouldn't be run for some reason"), `Explicit`,
`Values`, `ValueSource`, `Range`, `Random`, `Combinatorial`, `Pairwise`, `Sequential`, `Repeat`, `Retry`,
`Timeout`, `MaxTime`. Source files need `using NUnit.Framework;` and a reference to `nunit.framework.dll`.

## Known limitations (page lists them for 1.3.x)
`UnityTest` does not support WSA, parameterized tests (except `ValueSource`) or `Repeat`; nested test
fixtures cannot run from the Editor UI; `Retry` in Play Mode tests throws `InvalidCastException`.

## Checked
Date: 2026-11-07

Read in full: the UTF 1.4 "About" page, the "Edit Mode vs. Play Mode tests" page and the NUnit
attributes table page (one-line descriptions only; the individual attribute pages were not opened).

Removed because the pages do not confirm it: the Test Runner menu path and "Create EditMode Test
Assembly Folder", the generated `.asmdef` content (`overrideReferences`), the DamageCalculator samples,
what fits or does not fit Edit Mode (physics, coroutines), `ScriptableObject.CreateInstance` and
`DestroyImmediate`, the AssetDatabase data-validation test, the command line `-runTests` invocation,
`LogAssert.Expect` and "unexpected error logs fail tests", and the Verify list. The 1.4 index page still
says "version 1.3.x" for known limitations; kept as stated.

Method: documentation only; no commands were run.
