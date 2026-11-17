---
id: computing-software.software-engineering.mobile-development.app-size-reduction-r8-and-app-thinning
name: app-size-reduction-r8-and-app-thinning
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-performance, app-size, r8, app-thinning, proguard, android-app-bundle]
level: practitioner
status: draft
description: "Shrink mobile apps: R8 code and resource shrinking with keep rules, App Bundles and dynamic features, iOS app thinning and size reports, and asset/dependency audits."
sources:
  - https://developer.android.com/topic/performance/app-optimization/enable-app-optimization
  - https://developer.android.com/topic/performance/reduce-apk-size
  - https://developer.apple.com/documentation/xcode/reducing-your-app-s-size
  - https://developer.android.com/guide/app-bundle
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# App size reduction: R8 and app thinning

**Goal:** smaller downloads (better install conversion, especially on cellular and emerging markets) without breaking reflection-based code.

## 1. Measure
- Android: Play Console "App size" per device config; locally `bundletool get-size total --apks=app.apks`; Android Studio APK Analyzer (dex, resources, native libs).
- iOS: App Store Connect App Thinning size report; locally Archive -> Distribute -> "App Thinning: All compatible device variants" -> `App Thinning Size Report.txt`.

## 2. Android: R8
```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true            // R8: shrink, optimise, obfuscate code
            isShrinkResources = true          // remove unreferenced resources
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}
```
Keep rules for reflection, serialization and JNI:
```
-keep class com.acme.api.dto.** { *; }          # Gson/Moshi reflection models (or use codegen adapters)
-keepclassmembers class * { @com.squareup.moshi.Json <fields>; }
```
Most libraries ship consumer rules. Upload `mapping.txt` to Play Console (done automatically with bundles) to deobfuscate crash stack traces. Test the **release** build in QA: R8 issues appear only there (ClassNotFound, missing fields in JSON).

## 3. Android: App Bundles and delivery
- AAB lets Play serve per-device APKs (ABI, density, language splits): typically 15-35% smaller than a universal APK.
- Play Feature Delivery (dynamic feature modules) for large rarely used features; Play Asset Delivery for game assets.
- Native libs: ship only needed ABIs; `useLegacyPackaging = false` keeps them uncompressed and page-aligned (smaller install, required 16 KB alignment on newer devices).

## 4. iOS: app thinning and build settings
- The App Store slices per device (architecture, asset scale) automatically; use asset catalogs so images thin correctly.
- On-demand resources for large optional content.
- Build settings: Optimization Level `-Os` or `-Osize` for Swift where speed is not critical, `Dead Code Stripping = YES`, strip debug symbols on copy (keep dSYMs for crash reporting), `Asset Catalog compression`.
- Avoid embedding several large Swift packages that duplicate functionality; static vs dynamic frameworks affects launch time and size.

## 5. Assets and dependencies (both)
- Images: WebP/AVIF (Android), HEIC/asset catalogs (iOS), vector drawables/SF Symbols/PDF vectors instead of multiple PNG densities.
- Remove unused languages from dependencies (`androidResources { localeFilters += listOf("en", "de") }` in recent AGP; `resourceConfigurations` before).
- Audit dependencies: one image loader, one networking stack, one JSON library; replace heavy SDKs (analytics, ads) or load lazily.
- Fonts: subset and prefer system fonts.

## Gotchas
- `isShrinkResources` removes resources referenced only by dynamic name (`getIdentifier`); keep them via `res/raw/keep.xml` (`tools:keep`).
- Download size vs install size differ; stores show both. The Play Store warns above 200 MB download (cellular prompt).
- Size regressions creep in release by release; track size in CI (e.g. post a diff on each PR with `bundletool` / the thinning report).

## Verify
- Release builds pass the full UI test suite with R8 enabled, and the measured download size per device config dropped versus the baseline report.
