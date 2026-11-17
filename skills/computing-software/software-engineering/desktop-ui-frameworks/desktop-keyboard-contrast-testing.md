---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-keyboard-contrast-testing
name: desktop-keyboard-contrast-testing
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-keyboard-contrast-testing, desktop-accessibility, accessibility, uia, a11y, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Test keyboard-only use, high contrast and screen reader flows."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32
  - https://doc.qt.io/qt-6/accessible.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Accessibility keyboard, contrast and testing

**Goal:** meet WCAG basics in desktop apps.

```text
Checklist: every action reachable by Tab/Enter/Space/Esc; visible focus ring; 4.5:1 text contrast
Respect system settings: SystemParameters.HighContrast (WPF), QPalette/ QStyleHints::colorScheme (Qt 6.5, confirm), prefers-color-scheme/forced-colors (web)
Tools: Accessibility Insights for Windows, Narrator (Win+Ctrl+Enter), NVDA, VoiceOver (Cmd+F5)
Test: no mouse for 10 minutes of normal tasks
```

**Gotcha:** Custom-drawn controls bypass built-in accessibility, so implement the framework's automation peer or accessible interface.

## Verify
- A screen reader user completes the main task unaided.
