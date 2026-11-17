---
id: computing-software.software-engineering.wails.frontend-dev-environment-tips
name: frontend-dev-environment-tips
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, angular, vscode, vetur, nixos, mouse-buttons, overscroll, webview]
level: practitioner
status: docs-checked
description: "Small Wails frontend fixes: Angular dev mode, Vetur in VS Code, NixOS Wayland font-size bug, detecting back/forward mouse buttons, and disabling overscroll bounce."
sources: [https://wails.io/docs/guides/angular, https://wails.io/docs/guides/vscode, https://wails.io/docs/guides/nixos-font, https://wails.io/docs/guides/mouse-buttons, https://wails.io/docs/guides/overscroll]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Frontend and editor environment tips for Wails

Goal: apply the short, known fixes for common frontend/editor friction in a Wails project.

## Angular dev mode

There is no Angular template, but Angular works. In `wails.json`:
```json
  "frontend:build": "npx ng build",
  "frontend:install": "npm install",
  "frontend:dev:watcher": "npx ng serve",
  "frontend:dev:serverUrl": "http://localhost:4200",
```
Also add to the `<head>` of Angular's `index.html`:
```html
<meta name="wails-options" content="noautoinject" />
<script src="/wails/ipc.js"></script>
<script src="/wails/runtime.js"></script>
```

## Vetur in VS Code

Vetur errors because it expects the Vue project at the repo root. Create `vetur.config.js` in the project root with `projects: [{ root: './frontend', package: './package.json', tsconfig: './tsconfig.json', snippetFolder: './.vscode/vetur/snippets', globalComponents: ['./src/components/**/*.vue'] }]` (plus optional `settings` such as `"vetur.useWorkspaceDependencies": true`). Then give `frontend/tsconfig.json` compilerOptions (`module: system`, `noImplicitAny`, `removeComments`, `preserveConstEnums`, `sourceMap`, `outFile`, `allowJs`), `exclude` of `node_modules` and `**/*.spec.ts`, and `include` of `src/**/*` and `wailsjs/**/*.ts`.

## NixOS/Wayland: font-size has no effect

Add to the devShell:
```shell
shellHook = with pkgs; ''
  export XDG_DATA_DIRS=${gsettings-desktop-schemas}/share/gsettings-schemas/${gsettings-desktop-schemas.name}:${gtk3}/share/gsettings-schemas/${gtk3.name}:$XDG_DATA_DIRS;
  export GIO_MODULE_DIR="${pkgs.glib-networking}/lib/gio/modules/";
'';
```

## Detecting mouse buttons

The Wails runtime intercepts clicks (frameless resize and window move), and `window.onclick` does not report buttons correctly. Listen for `mousedown` and read `event.button`: 0 left, 1 middle, 2 right, 3 back, 4 forward.
```javascript
window.addEventListener("mousedown", (e) => { if (e.button === 3) { /* back */ } });
```

## Disable overscroll bounce

```css
html { height: 100%; overflow: hidden; }
```

## Related

See `computing-software.software-engineering.wails.frontend-routing` for router choice.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: Angular, Visual Studio Code, NixOS FontSize, Mouse Buttons and Overscroll guides.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
