---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-ui-automation-names-roles
name: desktop-ui-automation-names-roles
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-ui-automation-names-roles, desktop-accessibility, accessibility, uia, a11y, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Give every control an accessible name and role so screen readers and UIA tests work."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32
  - https://doc.qt.io/qt-6/accessible.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# UI Automation names and roles

**Goal:** usable with Narrator and NVDA.

```xml
<!-- WPF -->
<Button AutomationProperties.Name="Save document" AutomationProperties.HelpText="Saves to disk"/>
<TextBox AutomationProperties.LabeledBy="{Binding ElementName=NameLabel}"/>
// Qt: button->setAccessibleName(tr("Save document")); QML: Accessible.name: qsTr("Save")
// Electron/web: aria-label, role, labels; Tauri uses the system WebView so same web rules
```

**Gotcha:** Icon-only buttons have no name by default; screen readers announce them as button.

## Verify
- Inspect.exe or Accessibility Insights shows a name and role for each control.
