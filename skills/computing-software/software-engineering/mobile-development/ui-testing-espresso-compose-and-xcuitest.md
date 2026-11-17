---
id: computing-software.software-engineering.mobile-development.ui-testing-espresso-compose-and-xcuitest
name: ui-testing-espresso-compose-and-xcuitest
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, espresso, xcuitest, compose-testing, ui-testing, screenshot-testing, maestro, android, ios]
level: practitioner
status: draft
description: "Write reliable mobile UI tests: Compose test rules and semantics, Espresso idling, XCUITest identifiers and launch arguments, screenshot tests, flake control."
sources: ["https://developer.android.com/develop/ui/compose/testing", "https://developer.android.com/training/testing/espresso", "https://developer.apple.com/documentation/xctest/user_interface_tests", "https://maestro.mobile.dev/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UI testing (Espresso / Compose tests / XCUITest)

**Goal:** a small, fast, non-flaky set of UI tests covering critical flows, backed by many more unit
and screenshot tests.

## Pyramid for mobile
Most logic in ViewModel/unit tests (JVM / XCTest, milliseconds). Component tests of screens with
fake data (Compose tests on Robolectric, SwiftUI previews/snapshots). A handful of end-to-end flows
(login, purchase, core task) on devices or emulators.

## Compose UI tests
```kotlin
@get:Rule val rule = createComposeRule()   // createAndroidComposeRule<MainActivity>() for an Activity

@Test fun submitDisabledUntilValid() {
    rule.setContent { AppTheme { SignupScreen(state = SignupState(), onSubmit = {}) } }
    rule.onNodeWithText("Sign up").assertIsNotEnabled()
    rule.onNodeWithTag("email").performTextInput("a@b.com")
    rule.onNodeWithText("Sign up").assertIsEnabled().performClick()
}
```
- Finders use the **semantics tree** (what accessibility services see): text, content description,
  `Modifier.testTag("email")`. Good semantics make tests and accessibility better together.
- Compose test rules synchronise with recomposition and animations automatically; for async work
  use `rule.waitUntil(timeoutMillis = 5_000) { .. }` or register idling resources, never `Thread.sleep`.
- `rule.mainClock.autoAdvance = false` and `advanceTimeBy` to test animations deterministically.
- Runs on the JVM with Robolectric (`@RunWith(AndroidJUnit4::class)` + Robolectric) for speed, or
  as instrumented tests on devices.
- `printToLog("TAG")` dumps the semantics tree when a finder fails.

## Espresso (Views)
```kotlin
onView(withId(R.id.email)).perform(typeText("a@b.com"), closeSoftKeyboard())
onView(withText("Sign up")).check(matches(isEnabled())).perform(click())
```
- Espresso waits for the main thread and AsyncTask pool to idle; anything else (coroutines on IO,
  OkHttp) needs an `IdlingResource` (or OkHttp3IdlingResource), or tests race.
- Disable animations on test devices: `adb shell settings put global animator_duration_scale 0`
  (also window/transition scales), or `testOptions { animationsDisabled = true }` in Gradle.
- Orchestrator (`execution 'ANDROIDX_TEST_ORCHESTRATOR'`, `clearPackageData`) isolates tests.

## XCUITest
```swift
func testLogin() {
    let app = XCUIApplication()
    app.launchArguments += ["-uiTesting", "-resetState"]
    app.launchEnvironment["API_BASE_URL"] = "http://localhost:8080"
    app.launch()
    app.textFields["login.email"].tap()
    app.textFields["login.email"].typeText("a@b.com")
    app.buttons["login.submit"].tap()
    XCTAssertTrue(app.staticTexts["home.title"].waitForExistence(timeout: 5))
}
```
- Set `.accessibilityIdentifier("login.submit")` on elements: stable across localisation,
  unlike labels.
- XCUITest drives the app out of process; inject test configuration via launch arguments and
  environment, and stub the network (local mock server) rather than hitting real backends.
- `waitForExistence` / `XCTNSPredicateExpectation` instead of sleeps; `addUIInterruptionMonitor` or
  pre-granted permissions (`xcrun simctl privacy booted grant photos <bundle-id>`) for system alerts.
- Swift Testing (`@Test`) covers unit tests; UI tests still use XCTest.

## Screenshot tests
Paparazzi or Roborazzi (Android, JVM, no device) and swift-snapshot-testing (iOS) catch visual
regressions across themes, font scales and locales cheaply. Record goldens on CI-matching
environments to avoid pixel noise.

## Cross-platform E2E
Maestro (YAML flows, works with native, React Native, Flutter), Appium, Detox (React Native).
Run E2E on Firebase Test Lab, BrowserStack, or emulator/simulator farms in CI.

## Flake control
- No sleeps; explicit waits on conditions. Deterministic data via fakes and test servers.
- Retry failed tests at most once and track flake rate; quarantine flaky tests rather than ignoring
  failures.
- Fresh app state per test (orchestrator clear data, `-resetState` launch argument).

## Verify
- [ ] Critical flows covered by E2E tests running on every merge.
- [ ] Test IDs/tags/identifiers used instead of localised strings.
- [ ] Flake rate measured and under target (for example < 1%).
