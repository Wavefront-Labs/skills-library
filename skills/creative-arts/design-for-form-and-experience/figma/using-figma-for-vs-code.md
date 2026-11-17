---
id: creative-arts.design-for-form-and-experience.figma.using-figma-for-vs-code
name: using-figma-for-vs-code
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-vscode, figma-for-vs-code, vs-code-extension, dev-mode-vscode, code-connect, design-in-editor]
level: practitioner
status: docs-checked
description: "Use Figma for VS Code to open designs from Dev Mode, view code snippets, assets and component properties, and handle comments and dev resources in the editor."
sources:
  - https://help.figma.com/hc/en-us/articles/15023121296151-Figma-for-VS-Code
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Figma for VS Code

Figma publishes an extension for Visual Studio Code so developers can inspect designs without leaving the editor. The Help Center page is old, so menu paths may have changed; check it if a step does not match.

## Setup
1. Install **Figma for VS Code** from the Visual Studio Marketplace; sign in to Figma when you first open it.
2. It is available on all paid plans and requires a **Full or Dev seat**.
3. Open a design from Dev Mode with **Open in VS Code**, or from VS Code via Figma in the activity bar and a file under Files.

## Use
- **Code tab:** code snippets and related information such as modes and styles.
- **Assets tab:** download and export assets for the selected layer.
- **Component tab:** properties of a selected component.
- **Comments:** comment notifications appear in real time under Notifications in the primary sidebar; click one to view and add a comment from VS Code.
- **Dev resources tab:** development links; a link with a matching implementation in your codebase opens the file in VS Code rather than the browser.
- To map components to repository code, see `creative-arts.design-for-form-and-experience.design-systems.connecting-figma-to-code-with-code-connect` (not covered by this Help page).

## Gotchas
- Generated snippets are suggestions; use your design-system components and tokens, not copied hex values.

## Verify
- [ ] You can open a Dev Mode selection in the editor.
- [ ] Code uses tokens, not copied hex values.

## Checked
2026-11-01. Confirmed against the Figma for VS Code Help Center article: install source, sign-in, plans and seats, Open in VS Code, Code, Assets, Component and Dev resources tabs, comment notifications. Removed (not on the page): Ready for dev tracking in the extension, file-update notifications, jump-to-source via mapped components, variable code-syntax display, and the Marketplace source (not read).
Method: documentation only; no commands were run.
