---
id: computing-software.software-engineering.mobile-development.react-native-devtools-and-debugging
name: react-native-devtools-and-debugging
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, debugging, react-native-devtools, dev-menu, logbox, performance-monitor, console-errors, warnings, fast-refresh, profiler, components-inspector, devtools, mobile-debugging, error-handling]
level: practitioner
status: docs-checked
description: "Debug React Native with React Native DevTools (Console, Sources, Network, Performance, Memory, Components, Profiler), the Dev Menu, LogBox filtering and release-build limits."
sources: ["https://reactnative.dev/docs/debugging", "https://reactnative.dev/docs/react-native-devtools"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React Native DevTools and debugging

**Goal:** reach the right debugging surface for the problem - JS execution, component tree, render
performance, network, or log noise - instead of defaulting to `console.log` everywhere.

## React Native DevTools
"React Native DevTools" is the built-in debugger: "It allows you to inspect and understand how your
JavaScript code is running, similar to a web browser." Open it with **"Open DevTools" in the Dev
Menu**, or **press `j` from the CLI**. It is based on the Chrome DevTools frontend and is "designed
for debugging React app concerns, and not to replace native tools": for the platform layers (for
example a Native Module) use the debugging tools in Android Studio and Xcode.

Panels described in the docs:
- **Console**: view and filter messages, evaluate JavaScript, inspect objects; Live Expressions,
  Preserve Logs, `Ctrl + L` clears.
- **Sources and breakpoints**: view source files and set breakpoints (conditional breakpoints and
  logpoints exist); a `debugger;` statement reaches the device via Fast Refresh.
- **Network** (since 0.83): requests made through `fetch()`, `XMLHttpRequest` and `<Image>` are
  recorded automatically while DevTools is open. Not supported at launch: WebSocket events, network
  response mocking, simulated throttling. Response previews are cached in an on-device buffer of at
  most 100MB, evicting oldest first. Apps using Expo continue to see a separate "Expo Network" panel.
- **Performance** (since 0.83): record a session showing JavaScript execution, React Performance
  tracks, network events and custom User Timings on one timeline.
- **Memory**: heap snapshots and memory usage of your JavaScript over time.
- **Components** and **Profiler**: the React DevTools features, to inspect and edit the component
  tree at runtime and record render and commit timings. "Highlight updates when components render"
  is in View Settings.

DevTools can disconnect (app closed or rebuilt, native crash, Metro quit, device unplugged); a
"Debugging connection was closed" dialog offers "Reconnect DevTools".

## The Dev Menu
Open by shaking the device, or with the keyboard shortcuts:

| Platform | Shortcut |
|---|---|
| iOS Simulator | `Ctrl + Cmd + Z` (or Device > Shake) |
| Android emulator (macOS) | `Cmd + M` |
| Android emulator (Windows/Linux) | `Ctrl + M` |
| Android | `adb shell input keyevent 82` |

## LogBox
An in-app tool that displays when your app logs warnings or errors. A fatal error such as a
JavaScript syntax error opens LogBox with the location; it cannot be dismissed until fixed and then
dismisses automatically "either via Fast Refresh or after a manual reload". Console errors show as
on-screen notifications with a red badge and a count; warnings (yellow badge) show a banner without
details, prompting you to open React Native DevTools.

When DevTools is open, "all errors except fatal errors will be hidden to LogBox"; the docs
recommend the Console panel in DevTools as the source of truth, "due to various LogBox options which
can hide or adjust the level of certain logs".

```ts
import { LogBox } from 'react-native';
LogBox.ignoreLogs([
  'Warning: componentWillReceiveProps has been renamed',   // exact message
  /GraphQL error: .*/,                                      // substring or regex match
]);
LogBox.ignoreAllLogs();   // docs suggest e.g. product demos
```
`ignoreLogs` is described as useful for noisy warnings or ones that cannot be fixed, for example in
a third-party dependency. LogBox treats certain React errors as warnings; advanced users can change
this with `LogBoxData.setWarningFilter()`.

## Performance Monitor
Select "Perf Monitor" in the Dev Menu for an in-app performance overlay on Android and iOS. The
docs call it "a guide" and recommend the native tooling in Android Studio and Xcode for accurate
performance measurements (see the `android-studio-profiler-and-xcode-instruments` skill).

## Release builds
"Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release
(production) builds." Anything you can only reproduce through the Dev Menu needs another path
before release. Use crash reporting for production.

## Verify
- [ ] `j` (or Dev Menu -> Open DevTools) brings up React Native DevTools with the Components and
      Profiler panels available.
- [ ] Ignored LogBox patterns are reviewed, not left as blanket `ignoreAllLogs()`.
- [ ] The app behaves in a release build with no Dev Menu dependency left in any flow.

## Checked
2026-11-08. Confirmed against the reactnative.dev Debugging Basics and React Native DevTools pages
(both last updated 2026-10-27): DevTools description and ways to open it, panels and tips, Network
and Performance "since 0.83" notes and limits, 100MB preview buffer, reconnect behaviour, Dev Menu
shortcuts, LogBox behaviour and API, Perf Monitor recommendation, release-build statement. Removed
because the pages do not state them: Fast Refresh preserve and reload rules, the Flipper remark,
frame-rate contents of the Perf Monitor, regex-drift advice and the listed failure modes.
Method: documentation only; no commands were run.
