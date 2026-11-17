---
id: computing-software.software-engineering.mobile-development.kotlin-multiplatform-shared-logic
name: kotlin-multiplatform-shared-logic
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, cross-platform-mobile, kotlin-multiplatform, kmp, expect-actual, compose-multiplatform, skie]
level: practitioner
status: draft
description: "Share business logic between Android and iOS with Kotlin Multiplatform: source sets, expect/actual, iOS framework export and Swift interop, shared libraries, and adoption strategy."
sources:
  - https://kotlinlang.org/docs/multiplatform.html
  - https://kotlinlang.org/docs/multiplatform-expect-actual.html
  - https://kotlinlang.org/docs/native-objc-interop.html
  - https://www.jetbrains.com/compose-multiplatform/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kotlin Multiplatform for shared logic

**Goal:** one tested implementation of networking, data and domain logic used by native Android and iOS UIs, without forcing iOS developers into an awkward API.

## 1. Project structure
```kotlin
// shared/build.gradle.kts
kotlin {
    androidTarget()
    listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach {
        it.binaries.framework { baseName = "Shared"; isStatic = true }
    }
    sourceSets {
        commonMain.dependencies {
            implementation(libs.ktor.client.core)
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.sqldelight.runtime)
        }
        androidMain.dependencies { implementation(libs.ktor.client.okhttp) }
        iosMain.dependencies { implementation(libs.ktor.client.darwin) }
        commonTest.dependencies { implementation(kotlin("test")) }
    }
}
```
Default hierarchy template gives `iosMain` shared across iOS targets automatically.

## 2. expect/actual for platform APIs
```kotlin
// commonMain
expect fun platformName(): String
interface SecureStore { fun put(k: String, v: String); fun get(k: String): String? }

// androidMain
actual fun platformName() = "Android ${android.os.Build.VERSION.SDK_INT}"
// iosMain
actual fun platformName() = UIDevice.currentDevice.systemName + " " + UIDevice.currentDevice.systemVersion
```
Prefer interfaces + dependency injection for larger platform services (keystore/keychain, file paths); keep `expect/actual` for small functions and types.

## 3. What to share
Good: API clients and models, validation, business rules, caching/repositories (SQLDelight, Room KMP, DataStore), analytics event definitions, feature-flag evaluation. Optional: UI with Compose Multiplatform (stable for iOS since 1.8), or keep SwiftUI/Compose native UIs and share ViewModels.

## 4. Swift interop
Kotlin exports an Objective-C framework to Swift, which loses some features:
- `suspend` functions become completion handlers / async (with limitations); `Flow` is not directly consumable.
- Sealed classes become class hierarchies (no exhaustive `switch`), default arguments are lost, generics are limited.
Fixes: **SKIE** (Touchlab) generates Swift-friendly wrappers (async/await, AsyncSequence for Flow, exhaustive enums); KMP-NativeCoroutines; or Kotlin's Swift export (experimental). Design the public shared API with iOS consumers in mind.

## 5. Distribution to iOS
- Direct integration: Xcode build phase runs `./gradlew :shared:embedAndSignAppleFrameworkForXcode`.
- Separate repos: publish an XCFramework (`assembleSharedXCFramework`) via Swift Package Manager (KMMBridge automates this) so iOS developers do not need the JVM toolchain.

## 6. Adoption
Start with one non-UI module (e.g. API client and models), measure, expand. Keep iOS engineers involved in API design and code review; shared code that only Android engineers understand stalls.

## Gotchas
- Kotlin/Native memory model is the new one (default since 1.7.20): objects can be shared across threads; old `freeze()` advice is obsolete.
- iOS build times grow with framework size; use static frameworks and only export needed modules (`export(...)`).
- Crash reports from Kotlin/Native need symbol files (dSYMs include Kotlin frames) and CrashKiOS/Crashlytics integration.
- Library availability: check klibs.io / multiplatform support before choosing a dependency.

## Verify
- `./gradlew :shared:allTests` runs common tests on JVM and iOS simulator, both apps consume the same version of the shared module in CI, and Swift call sites use async/await without manual callback wrappers.
