---
id: computing-software.game-programming.unity.unitysetup-teardown-and-test-scenes
name: unitysetup-teardown-and-test-scenes
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-testing, unitysetup, unityteardown, iprebuildsetup, ipostbuildcleanup, test-framework, game-programming]
level: practitioner
status: docs-checked
description: "Unity Test Framework setup and cleanup: UnitySetUp/UnityTearDown order, domain reload behaviour, and IPrebuildSetup/IPostBuildCleanup build-time hooks."
sources: ["https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-actions-outside-tests.html", "https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-setup-and-cleanup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UnitySetUp, UnityTearDown and build-time setup

**Goal:** tests that start from a known state and clean up after themselves, with the hooks in the right order.

## Setup and teardown attributes
NUnit's `SetUp` and `TearDown` avoid duplicated code. The Unity Test Framework extends them with `[UnitySetUp]` and
`[UnityTearDown]`, which can yield commands and skip frames in the same way as `[UnityTest]`.

## Action execution order (same for `Test` and `UnityTest`)
1. Attributes implementing `IApplyToContext`.
2. `OuterUnityTestAction` attributes: `BeforeTest`.
3. `UnitySetUp` methods in the test class.
4. Attributes implementing `IWrapSetUpTearDown`.
5. Methods with `[SetUp]`.
6. Action attributes: `BeforeTest`.
7. Attributes implementing `IWrapTestMethod`.
8. The test itself.
9. Action attributes: `AfterTest`.
10. Methods with `[TearDown]`.
11. `UnityTearDown` methods in the test class.
12. `OuterUnityTestAction`: `AfterTest`.

## Domain reloads in Edit Mode tests
Edit Mode tests can yield instructions that cause a domain reload (entering or exiting Play Mode). After a reload,
non-Unity actions (such as `OneTimeSetUp` and `SetUp`) are re-run before the code that started the reload continues. Unity
actions (such as `UnitySetUp`) are not re-run; if the Unity action itself started the reload, the rest of that
`UnitySetUp` method runs after it.

## Build-time setup and cleanup
For changes to Unity or the file system before building the tests, and clean-up afterwards:
- Implement `IPrebuildSetup` (`void Setup()`) and `IPostBuildCleanup` (`void Cleanup()`) on a test class, or
- apply the `PrebuildSetup` / `PostBuildCleanup` attribute on a test class, a test, or the test assembly, naming a class that
  implements the interface, for example `[PrebuildSetup("MyTestSceneSetup")]`.
- Setups run in a deterministic order: attribute-defined setups first, then test classes implementing the interface, in
  alphabetical order within their namespace (the same as test order).
- The attributes run if the test or test class is in the current run (all tests, or a filter that includes it). If
  several tests reference the same setup or cleanup, it runs once.
- Cleanup runs right away for a standalone test run, but only after the related tests run in the Unity Editor.
- Use `#if UNITY_EDITOR` to access Editor-only APIs when the setup lives in a Play Mode assembly.

## Verify
- [ ] Setup that must survive a domain reload is in a non-Unity `SetUp`, which is re-run.
- [ ] Build-time asset changes are reverted in `IPostBuildCleanup.Cleanup`.

## Checked
Date: 2026-11-09. Read in full: Test Framework 1.4 "Actions outside of tests" and "Setup and cleanup at build time".
Removed as not on those pages: the scene-loading examples (`SceneManager.LoadSceneAsync`,
`EditorSceneManager.LoadSceneInPlayMode`), the claim that the runner creates a fresh scene per test while
`DontDestroyOnLoad` objects survive, `[UnityPlatform]`/`[RequiresPlayMode]`, `[OneTimeSetUp]` per-fixture description,
`LogAssert` failure behaviour, time-based test advice, and the random-order and Hierarchy checks.
Method: docs-checked 2026-11-09 against the two Test Framework pages named above.
