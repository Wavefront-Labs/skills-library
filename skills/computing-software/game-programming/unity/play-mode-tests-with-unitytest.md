---
id: computing-software.game-programming.unity.play-mode-tests-with-unitytest
name: play-mode-tests-with-unitytest
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-testing, unitytest, play-mode, edit-mode, test-framework, assembly-definition, game-programming]
level: practitioner
status: docs-checked
description: "Unity Test Framework Play Mode tests: when to use UnityTest coroutines versus plain NUnit Test, yield instructions, and assembly definition requirements."
sources: ["https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/edit-mode-vs-play-mode-tests.html", "https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-attribute-unitytest.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Play Mode tests with UnityTest

**Goal:** automated tests that run real frames (physics, coroutines) for game code.

## Edit Mode versus Play Mode
- Edit Mode tests run only in the Unity Editor, have access to Editor code as well as game code, and run in the
  `EditorApplication.update` callback loop. They need an assembly definition referencing `nunit.framework.dll` with only
  the Editor as include platform (`"includePlatforms": ["Editor"]`), or (legacy) live in the project's Editor folder.
- Play Mode tests run standalone in a Player or inside the Editor. With the `UnityTest` attribute they run as coroutines.
  They need an assembly definition referencing `nunit.framework.dll`, test scripts in the folder with the `.asmdef`, and a
  reference to the assembly that holds the code under test (`"references"`), with `TestAssemblies` in
  `optionalUnityReferences`.
- Test assemblies can reference `UnityEngine.TestRunner` and `UnityEditor.TestRunner`; the latter is Edit Mode only.

## When to use UnityTest
Use the NUnit `Test` attribute instead of `UnityTest` unless you need to yield special instructions in Edit Mode, or need
to skip a frame or wait a certain time in Play Mode.

`UnityTest` is an alternative to `Test` that lets a test yield instructions back to the framework; the run continues when
the instruction completes. `yield return null` skips a frame.

## Play Mode yields
A Play Mode `UnityTest` runs as a coroutine attached to a MonoBehaviour, so the usual coroutine yield instructions work:
- `WaitForFixedUpdate`: for changes expected in the next cycle of physics calculations.
- `WaitForSeconds`: pauses for a fixed time. Be careful about creating long-running tests.

```csharp
[UnityTest]
public IEnumerator GameObject_WithRigidBody_WillBeAffectedByPhysics()
{
    var go = new GameObject();
    go.AddComponent<Rigidbody>();
    var originalPosition = go.transform.position.y;

    yield return new WaitForFixedUpdate();

    Assert.AreNotEqual(originalPosition, go.transform.position.y);
}
```

## Edit Mode yields
An Edit Mode `UnityTest` can yield `null` to skip a frame while a background task finishes, or give commands to the
Editor such as a domain reload or entering Play Mode.

## Verify
- [ ] Tests that never need to wait use `[Test]`, not `[UnityTest]`.
- [ ] The test assembly references the assembly under test.

## Checked
Date: 2026-11-09. Read in full: Test Framework 1.4 "Edit Mode vs. Play Mode tests" and "UnityTest attribute".
Removed as not on those pages: the `UnitySetUp` scene-loading sample, `LogAssert` behaviour, `Time.timeScale`, async `Task`
tests and their version claim, the polling helper, fixed physics step and seeding advice, `[Category]`/`[Timeout]` use,
Enter Play Mode Options statics advice, and Build Settings scene lists.
Method: docs-checked 2026-11-09 against the two Test Framework pages named above.
