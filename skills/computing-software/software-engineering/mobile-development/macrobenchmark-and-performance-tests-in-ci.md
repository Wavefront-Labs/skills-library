---
id: computing-software.software-engineering.mobile-development.macrobenchmark-and-performance-tests-in-ci
name: macrobenchmark-and-performance-tests-in-ci
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, macrobenchmark, jetpack-benchmark, baseline-profiles, xctest-metrics, performance-testing, ci, startup-time, frame-timing]
level: advanced
status: docs-checked
description: "Measure Android startup and scrolling with Jetpack Macrobenchmark, generate baseline profiles, and run performance regression tests in CI on real devices."
sources: ["https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview", "https://developer.android.com/topic/performance/baselineprofiles/overview", "https://developer.android.com/topic/performance/benchmarking/benchmarking-in-ci"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macrobenchmark and performance tests in CI

**Goal:** catch startup, scrolling and navigation regressions before release with repeatable,
automated measurements.

## Jetpack Macrobenchmark (Android)
Macrobenchmark needs a `com.android.test` module separate from the app code. Android Studio has a Benchmark module
template (New > Module) that creates it with a sample startup benchmark. `MacrobenchmarkRule.measureRepeated` needs at
least `packageName`, `metrics` and `iterations`.
```kotlin
@LargeTest
@RunWith(AndroidJUnit4::class)
class ComposeScrollBenchmark {
    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun scrollLazyColumn() = benchmarkRule.measureRepeated(
        packageName = "com.example.compose.app",
        metrics = listOf(FrameTimingMetric()),
        iterations = 5,
        startupMode = StartupMode.WARM,
        setupBlock = { pressHome() }
    ) {
        startActivityAndWait()
        val lazyColumn = device.findObject(By.res("my_lazy_column"))
        lazyColumn.setGestureMargin(device.displayWidth / 5)
        lazyColumn.fling(Direction.DOWN)
    }
}
```
- Available metrics: `StartupTimingMetric`, `FrameTimingMetric`, `TraceSectionMetric`.
- To let UI Automator find Compose nodes, set `testTagAsResourceId = true` on the semantics modifier of the
  top-level Compose element.
- The target app must be profileable (the module wizard adds the `<profileable>` tag) and include ProfilerInstaller
  1.3 or later. Configure it as close to release as possible: non-debuggable, preferably minified. Make a `benchmark`
  build type with `initWith(getByName("release"))` signed with the debug key, and select the `benchmark` variant for
  both the app and the Macrobenchmark module.
- Multi-module apps need `matchingFallbacks += listOf("release")` in the `benchmark` build type; product flavors need
  `missingDimensionStrategy` or the same flavors declared in the Macrobenchmark module.
- `CompilationMode` controls pre-compilation (`Full`, `Partial`, `None`, `Ignore`). The default installs a Baseline
  Profile if one exists, on Android 7 (API level 24) and later.
- `StartupMode` is `COLD`, `WARM` or `HOT`. With `COLD` the process is killed between `setupBlock` and `measureBlock`.
- Use Android 14 (API level 34) or later to persist state; earlier versions need the APK reinstalled per compile.
- A debuggable or non-profileable app, an emulator or a low-battery device makes Macrobenchmark return an error
  (suppressible with the `androidx.benchmark.suppressErrors` argument).
- Each measured iteration captures a system trace, openable from the Test Results pane in Android Studio.
- Run all benchmarks of a module with `./gradlew :macrobenchmark:connectedCheck`.

## Baseline profiles
Generate with a `BaselineProfileRule` test:
```kotlin
@get:Rule val baselineProfileRule = BaselineProfileRule()
@Test fun generate() = baselineProfileRule.collect(packageName = PACKAGE_NAME) { /* critical user journeys */ }
```
`./gradlew app:generateBaselineProfile` generates the profile (release build type only on older AGP; fixed in AGP 8.1).
The page says Baseline Profiles improve code execution speed by about 30% from first launch. Profile rules live in
files such as `baseline-prof.txt`; AGP 8.0 or later (apps) lets you declare multiple files in variant-aware
directories such as `src/free/generated/baselineProfiles/`. Check that the generated text profile is not obfuscated.
Compare `CompilationMode.None()` with the default to measure the profile's value.

## Running in CI
- Use physical devices (for example Firebase Test Lab); emulators give numbers tied to the host, not users.
- Benchmark results are fuzzy, not pass or fail: graph timings over time to see change and noise.
- Macrobenchmark needs the target APK and test APK built separately: `:app:assemble[VariantName]` and
  `:macrobenchmark:assemble[VariantName]`. Install with `adb install`; Macrobenchmark uses the regular
  `androidx.test.runner.AndroidJUnitRunner`.
- Results are JSON plus one Perfetto trace per measured iteration. Gradle copies them to
  `build/outputs/connected_android_test_additional_output/debugAndroidTest/connected/`; with raw `adb` pull them from
  the app's external media directory (the library logs the path to Logcat).
- `./gradlew lockClocks` locks CPU clocks on rooted devices, but the page says it is only necessary for microbenchmarks.

## Verify
- [ ] Benchmarks run on a non-debuggable, profileable build on a physical device.
- [ ] Baseline profile committed and its improvement measured.
- [ ] CI tracks results over time and flags regressions.

## Checked
2026-11-08. Confirmed against the Android Developers pages Write a Macrobenchmark, Baseline Profiles overview and Benchmark in Continuous Integration: module and build-type setup, metrics list, CompilationMode and StartupMode, API 34 note, configuration errors, generate command, about 30% figure, output paths, separate APK builds, lockClocks scope. Removed: iOS XCTest section (Apple page not readable), PowerMetric/MemoryUsageMetric, BaselineProfileMode.Require, the 20-40% figure, `reportFullyDrawn` detail, the claim that lockClocks applies to Macrobenchmark, and the statistical regression guidance.
Method: documentation only; no commands were run.
