---
id: computing-software.game-programming.unreal-engine.automation-tests-spec-and-functional
name: automation-tests-spec-and-functional
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-packaging, unreal-automation-test, automation-spec, functional-testing, session-frontend, implement-simple-automation-test, ci-testing, game-programming]
level: practitioner
status: docs-checked
description: "Write Unreal automation tests: framework test types, BDD-style Automation Specs (Describe, It, BeforeEach, Latent), Functional Test actors, and running them in Test Automation."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-spec-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automation tests: specs and functional tests

**Goal:** automated checks for game logic and in-level behaviour using Epic's Automation Test Framework.

## Framework (Automation Test Framework page)
- Test types: Unit (API-level), Feature (system-level), Smoke (a speed promise: all Smoke tests are intended to complete
  within 1 second; run at startup and selected by default in the UI), Content Stress, Screenshot Comparison.
- Built directly in C++, not associated with the UObject environment, and relies on engine systems, so Epic says it is
  not ideal for pure unit testing (see Low-Level Tests).
- Interfaces built on it: Automation Spec, Automation Driver, Functional Testing, Screenshot Comparison Tool, FBX Test
  Builder, Editor testing with Blueprint or Python, CQTest.
- Design guidelines: do not assume game or editor state (tests can run out of order or in parallel across machines),
  leave files on disk as you found them, assume the previous run left a bad state.
- Run: enable at least one automation test plugin (Edit > Plugins, Testing filter, restart), then
  Window > Test Automation; in the Sessions Frontend Automation tab enable Editor, Project, System under Test Name and
  click Start Tests.

## Automation Spec (BDD)
- Define with `DEFINE_SPEC(Name, "MyGame.Path", Flags)` or, to add members, `BEGIN_DEFINE_SPEC` / `END_DEFINE_SPEC`. The
  page's flags are `EAutomationTestFlags::ProductFilter | EAutomationTestFlags::ApplicationContextMask`. Implement
  `Define()` rather than `RunTest`.
- Suggested (not required): file name `.spec.cpp` without "Test" in it.
- `Describe(Description, lambda)` scopes expectations and can nest; it runs once while defining, it is not a test.
  `It(...)` defines one expectation and becomes one individually runnable test; the page suggests descriptions
  starting with "should".
- `BeforeEach` / `AfterEach` run around each `It` in their `Describe` scope, in definition order; use `AfterEach` only
  for clean-up.
- `EAsyncExecution` overloads (TaskGraph, ThreadPool, Thread) run a block on that executor while keeping sequence.
- Latent: `LatentBeforeEach`, `LatentIt`, `LatentAfterEach` take a `const FDoneDelegate& Done`; the sequence does not
  continue until `Done.Execute()` is called. Can combine with `EAsyncExecution`.
- Parameterised tests: call `It` in a loop with a unique description and capture the data in the lambda.
  `Redefine()` re-runs `Define()`. `xDescribe`, `xBeforeEach`, `xIt`, `xAfterEach` disable blocks.
- Mature example named on the page: `AutomationDriver.spec.cpp` under `Engine/Plugins/Tests/AutomationDriverTests`.

## Functional tests (Functional Testing page)
- Place a Functional Test Actor in a Level, script it from the Level Script, or subclass `AFunctionalTest` in code or
  Blueprint (recommended for complex or repeated tests).
- Functions: `PrepareTest` (first to run; start multi-frame setup here), `IsReady` (called every tick after PrepareTest
  until the test starts; default true), `OnTestStart` (bind your test and call `FinishTest`), `OnTestFinished` (clean up).
- Support: `OnAdditionalTestFinishedMessageRequest`, `RegisterAutoDestroyActor`, `LogMessage` (category
  `LogFunctionalTest`), `Observation Point`, `Enabled`.
- Ground Truth Data (`UGroundTruthData`, needs the Functional Test Editor plugin) stores an expected result Object for
  comparison; its `ResetGroundTruth` variable resets it.

## Checked
Date: 2026-11-07. Read in full: Automation Test Framework page, Automation Spec page (code blocks included) and
Functional Testing page, unversioned en-us pages with no engine version stated.
Removed as not on those pages: `IMPLEMENT_SIMPLE_AUTOMATION_TEST` example and its flag list, `WITH_DEV_AUTOMATION_TESTS`,
the whole command-line block (`UnrealEditor-Cmd.exe`, `-ExecCmds`, `-NullRHI`, `-ReportExportPath`, `-TestExit`), report
file names, the `/Game/Tests/` map convention and `Project.Functional Tests.<Map>.<Actor>` naming, "time limit property",
the Gauntlet cross-reference detail, and the Verify checklist. CLI/CI running is not covered by the cited pages; look up
the Automation System User Guide for it.
Method: documentation only; no commands were run.
