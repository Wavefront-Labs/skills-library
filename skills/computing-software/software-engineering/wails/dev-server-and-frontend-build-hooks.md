---
id: computing-software.software-engineering.wails.dev-server-and-frontend-build-hooks
name: dev-server-and-frontend-build-hooks
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, wails-dev, wails-json, create-react-app, dev-server, hot-reload]
level: practitioner
status: docs-checked
description: "Understand what wails dev and wails build do with the frontend, the debounce setting, and how to run an external watcher such as Create React App."
sources: [https://wails.io/docs/guides/application-development]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure how Wails builds, watches and reloads the frontend.

## Assets and wails.json
Wails v2 only needs an `embed.FS` of your assets; how you produce it is up to you. On `wails build` it reads two `wails.json` keys:

- `frontend:install` - run in the `frontend` directory to install node modules
- `frontend:build` - run in the `frontend` directory to build the frontend

If neither key is present, Wails does nothing with the frontend.

## Built-in dev server (wails dev)
`wails dev` watches the project directory. If a changed file is an application file (default `.go`, set with `-e`), the app is rebuilt and relaunched. If a changed file is in the assets, a reload is issued after a short wait. Reloads are debounced: the timer resets on each trigger; default `100ms`. Change it with the `-debounce` flag; the value is saved to your project config as the new default.

## External dev server
Frameworks with their own live-reload server cannot use the Wails Go bindings. The page recommends running a watcher script that rebuilds into the build directory Wails watches (the default svelte template uses rollup).

### Create React App
Add to `wails.json`:

```json
  "frontend:dev:watcher": "yarn start",
  "frontend:dev:serverUrl": "http://localhost:3000",
```

`frontend:dev:watcher` starts the CRA server (typically port 3000); `frontend:dev:serverUrl` makes Wails load assets from it. Because the watcher stops Wails injecting its scripts, add to `index.html`:

```html
<head>
	<meta name="wails-options" content="noautoinject" />
	<script src="/wails/ipc.js"></script>
	<script src="/wails/runtime.js"></script>
</head>
```

Then run `wails dev`. A browser can reach the app so React dev tools work on an unminified build. `wails dev -s` skips Wails' own frontend build, which is unnecessary here.

See also `computing-software.software-engineering.wails.frontend-script-injection` and `computing-software.software-engineering.wails.manual-build-steps`.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Application Development" guide.

Corrected or removed: Removed the "Option one" framing (the page gives no option two) and the "by default" qualifier; the page simply recommends a watcher script.

Method: documentation only; no commands were run.
