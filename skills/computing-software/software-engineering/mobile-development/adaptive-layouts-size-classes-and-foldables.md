---
id: computing-software.software-engineering.mobile-development.adaptive-layouts-size-classes-and-foldables
name: adaptive-layouts-size-classes-and-foldables
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, adaptive-layout, size-classes, window-size-classes, foldables, tablets, list-detail, navigationsuitescaffold, ipad]
level: practitioner
status: docs-checked
description: "Build adaptive Android UIs for phones, tablets, foldables and multi-window: window size classes, canonical layouts (list-detail, supporting pane), fold postures."
sources: ["https://developer.android.com/develop/ui/compose/layouts/adaptive", "https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes", "https://developer.android.com/guide/topics/large-screens/learn-about-foldables"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Adaptive layouts (tablets, foldables, size classes)

**Goal:** one app whose layout responds to the available **window** size and posture, not to the
device model, so it works on tablets, foldables, desktop windows and split screen.

## Think in window size, not device
Window size classes are not determined by the device screen and are not meant for `isTablet` logic. Split screen,
resizable ChromeOS windows and foldables all change the space available, and the class can change while the app
runs (orientation, multitasking, folding). Adaptive apps replace layout components and show or hide content rather than
just stretching: a bottom navigation bar on phones and a navigation rail on large screens, one pane versus a two-pane
list-detail layout.

## Android window size classes
Width and height are classified separately; width is usually the more relevant.
| Width class | Breakpoint |
|---|---|
| Compact | < 600dp |
| Medium | 600dp to < 840dp |
| Expanded | 840dp to < 1200dp |
| Large | 1200dp to < 1600dp |
| Extra-large | >= 1600dp |

Height classes: compact < 480dp, medium 480dp to < 900dp, expanded >= 900dp. Consider height too for landscape phones
and open flippables, where width is typically medium but height compact, so two panes are impractical.
```kotlin
val windowSizeClass = currentWindowAdaptiveInfo().windowSizeClass
// add supportLargeAndXLargeWidth = true to get the large and extra-large breakpoints
```
`currentWindowAdaptiveInfo()` comes from the `androidx.compose.material3.adaptive` library. Pass the window size class
down as state to nested composables. Test at compact, medium and expanded widths; if you have a compact layout,
optimise for expanded first, then decide what medium needs.

Material 3 adaptive components: `NavigationSuiteScaffold` (switches between navigation bar and rail by window size
class and posture), `ListDetailPaneScaffold` (list-detail canonical layout) and `SupportingPaneScaffold`
(supporting pane canonical layout).

## Foldables
- Fold state is `FLAT` (fully open) or `HALF_OPENED`. Half opened gives tabletop posture (horizontal fold) or book
  posture (vertical fold).
- Split content into two areas when half opened: top and bottom in tabletop, left and right in book. Controls near the
  fold are hard to reach and text over the fold can be unreadable, so keep dialogs and pop-up menus off the fold.
- On Android 12 (API level 31) and later, all apps run in multi-window mode on large screens regardless of
  configuration; down to Android 7.0 (API level 24) the app must be configured resizable.

## Input and testing
- Users connect keyboards, trackpads, mice and styluses to large screens. The Keyboard Shortcuts Helper lists app
  shortcuts published via the `onProvideKeyboardShortcuts()` window callback.
- The Desktop emulator tests free-form windowing, mouse hover and keyboard shortcuts.

## Verify
- [ ] Screenshots/tests at compact, medium and expanded widths.
- [ ] Resizing a window live keeps state and switches layouts smoothly.
- [ ] Foldable postures tested in an emulator.

## Checked
2026-11-08. Confirmed against the Android Developers pages Adaptive layouts (Compose), Use window size classes and Learn about foldables: breakpoints, class definitions, `currentWindowAdaptiveInfo`, scaffold names, fold states and postures, multi-window API levels, input and emulator notes. Removed: the iOS section and Apple HIG source (page not readable), the sample ListDetailPaneScaffold navigator code, `GridCells.Adaptive(180.dp)`, the "do not lock orientation" and "state must survive" bullets, the typical-layout table column, content-width rules and `DeviceConfigurationOverride` (not on the pages read).
Method: documentation only; no commands were run.
