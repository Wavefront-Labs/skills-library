---
id: computing-software.software-engineering.mobile-development.theming-dark-mode-and-material-3
name: theming-dark-mode-and-material-3
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, material-design, dark-mode, material-3, dynamic-color, design-tokens, jetpack-compose, swiftui, theming]
level: practitioner
status: docs-checked
description: "Theme mobile apps with Material 3 in Compose (color schemes, dynamic color, typography) and semantic colors in SwiftUI, supporting dark mode, contrast and brand tokens."
sources: ["https://m3.material.io/foundations/design-tokens/overview", "https://developer.android.com/develop/ui/compose/designsystems/material3", "https://developer.android.com/develop/ui/views/theming/darktheme", "https://developer.apple.com/design/human-interface-guidelines/dark-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Theming, dark mode and Material 3

**Goal:** one source of design tokens that drives light, dark and high-contrast appearances, so no
screen hard-codes colours and dark mode is not an afterthought.

## Principle: semantic tokens, not raw colours
Components reference roles (`primary`, `surface`, `onSurface`, `error`, `outline`), never hex
values. Brand palettes map to roles per appearance. This is what makes dark mode, dynamic colour
and rebrands cheap.

## Compose Material 3
```kotlin
private val LightColors = lightColorScheme(primary = Brand40, onPrimary = Color.White, surface = Neutral99, ...)
private val DarkColors  = darkColorScheme(primary = Brand80, onPrimary = Brand20, surface = Neutral10, ...)

@Composable
fun AppTheme(darkTheme: Boolean = isSystemInDarkTheme(), dynamicColor: Boolean = true, content: @Composable () -> Unit) {
    val colors = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
            if (darkTheme) dynamicDarkColorScheme(LocalContext.current) else dynamicLightColorScheme(LocalContext.current)
        darkTheme -> DarkColors
        else -> LightColors
    }
    MaterialTheme(colorScheme = colors, typography = AppTypography, shapes = AppShapes, content = content)
}
```
- Generate schemes from a brand seed colour with the **Material Theme Builder** (exports Compose and
  XML code with tonal palettes and contrast variants).
- Dynamic colour is available on Android 12 and above; fall back to a custom light or dark scheme below that.
  Offer it or not by brand policy, but keep brand-critical elements (logo) fixed.
- Use `MaterialTheme.colorScheme.*` and `MaterialTheme.typography.*` in components; extend with a
  `CompositionLocal` (`LocalExtendedColors`) for app-specific roles (success, warning) instead of
  ad-hoc colours.
- `Surface`/`Scaffold` set `LocalContentColor` so text and icons get the right `on*` colour automatically.
- Views/XML: inherit from a DayNight theme (for example `Theme.MaterialComponents.DayNight`).

## Dark mode on Android
- Follow the system (`isSystemInDarkTheme()`) and optionally offer an in-app override with the DayNight modes
  `MODE_NIGHT_NO`, `MODE_NIGHT_YES` and `MODE_NIGHT_FOLLOW_SYSTEM`. On API 31 and above use
  `UiModeManager#setApplicationNightMode`; on API 30 and below use `AppCompatDelegate.setDefaultNightMode()`
  (AppCompat 1.1.0 and later recreates started activities).
- Do not hard-code grey backgrounds; use theme colour roles.
- Force Dark (Android 10) is a quick fallback for apps without a real dark theme; prefer a real dark theme.

## SwiftUI / iOS
- Use semantic system colours and **asset catalog colours** with Any/Dark (and High Contrast) appearances
  instead of hard-coded values; see Apple's Human Interface Guidelines (Dark Mode).
- `@Environment(\.colorScheme)` for rare manual branches; `.preferredColorScheme(.dark)` for an in-app override.
- Dynamic Type: use text styles (`.font(.body)`), not fixed sizes.

## Contrast and accessibility
- Check contrast in both appearances against WCAG. Use `on*` colours on their matching role (`onPrimary` on
  `primary`): Material's tonal system is designed for accessible contrast; custom colours are not.
- Support iOS "Increase Contrast" via high-contrast asset variants.

## Checked
2026-11-01. Confirmed against developer.android.com pages (Material Design 3 in Compose, Dark theme): Material Theme
Builder, isSystemInDarkTheme, dynamic colour on Android 12+, on-colour pairing, DayNight themes, night-mode
constants, UiModeManager vs AppCompatDelegate by API level, Force Dark on Android 10. Removed: edge-to-edge
targetSdk claim, Theme.Material3.DayNight name, surfaceContainer note, WCAG ratios, Android 14 contrast levels,
Xcode 15 symbol note, SwiftUI API claims (Apple pages not checked).
Method: documentation only; no commands were run.

## Verify
- [ ] No hard-coded colours in components (lint: search for `Color(0x` / hex literals outside the theme).
- [ ] Screenshot tests (Paparazzi/Roborazzi, swift-snapshot-testing) cover light and dark.
- [ ] Contrast checked with Accessibility Scanner / Xcode Accessibility Inspector.
