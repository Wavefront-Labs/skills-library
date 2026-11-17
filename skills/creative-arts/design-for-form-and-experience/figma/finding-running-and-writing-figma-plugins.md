---
id: creative-arts.design-for-form-and-experience.figma.finding-running-and-writing-figma-plugins
name: finding-running-and-writing-figma-plugins
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [plugin-api, figma-plugins, plugin-development, manifest-json, figma]
level: practitioner
status: docs-checked
description: "Start a Figma plugin: manifest fields and valid values, scaffolding a new plugin, showing a UI iframe and messaging between plugin code and UI."
sources:
  - https://developers.figma.com/docs/plugins/manifest/
  - https://developers.figma.com/docs/plugins/creating-ui/
  - https://developers.figma.com/docs/plugins/plugin-quickstart-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing Figma plugins

## Scaffold

In the Figma desktop app: **Plugins > Development > New plugin**, choose **Figma design**, name it, select **Custom UI** and **Save as**. The quickstart builds a TypeScript plugin with `code.ts`, `tsconfig.json` and `package.json`, and a manifest whose `main` points to the compiled JavaScript file. Run it from **Plugins > Development > (plugin name)**.

## manifest.json

- `name`: the name shown in the menu. `id`: the plugin ID to publish updates to; Figma assigns it. `api`: the Figma API version used; the docs recommend updating to the latest whenever possible.
- `main`: relative path of the plugin's JavaScript. `ui`: optional HTML file path (or a map of files) used by `figma.showUI`.
- `editorType` (required): `figma` (design mode), `figjam`, `dev`, `slides` or `buzz`. The combination `["figjam", "dev"]` is unsupported.
- `documentAccess`: required for all new plugins, and the value must be `dynamic-page`.
- `networkAccess` (optional): `allowedDomains` is a required list of strings. `["none"]` means the plugin cannot reach any external network resource. A reasoning field is required when `allowedDomains` includes `"*"` or local development servers. `devAllowedDomains` lists domains permitted only during development.

## UI and messaging

- Set `"ui": "ui.html"` in the manifest and call `figma.showUI(__html__)`; the HTML appears in an `<iframe>` inside Figma.
- UI to plugin: `parent.postMessage({ pluginMessage: ... }, '*')`; the plugin receives it with `figma.ui.onmessage`. `pluginMessage` is required in the UI call.
- Plugin to UI: `figma.ui.postMessage(...)`; the UI reads `event.data.pluginMessage`. Messages sent before the iframe loads are queued.
- Structured data can be sent but methods and prototype behaviour are lost; `Blob`, `ArrayBuffer` and typed arrays other than `Uint8Array` are not currently supported.
- If the iframe navigates to a custom URL, messages need a `pluginId`; for sensitive data use `'https://www.figma.com'` as the target origin.
- Use the `themeColors` option and CSS variables to follow light and dark themes.

## Practice

- Vet any community plugin before running it: publisher, permissions requested and what network access it declares.
- Declare the narrowest `networkAccess` you can; never store secrets in the plugin.

## Verify

- [ ] Manifest has name, id, api, main, editorType and documentAccess.
- [ ] Network access lists only the domains needed, or `none`.
- [ ] UI and plugin code exchange a test message in both directions.

## Checked

2026-11-01. Confirmed against the Figma developer docs pages above: manifest fields, editorType values, documentAccess requirement, networkAccess rules, showUI and messaging calls, data type limits, scaffold menu path and files. Removed as not confirmed: the Community plugin finding steps (Resources panel, Quick actions, categories and named plugins), Enterprise restrictions, the plugin API code sample, `showUI` size options, network calls happening in the UI, import-from-manifest and console menu paths, publishing steps and performance advice. The old manifest example lacked `documentAccess`, now required for new plugins.
Method: documentation only; no commands were run.
