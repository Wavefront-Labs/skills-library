---
id: computing-software.software-engineering.wails.frontend-script-injection
name: frontend-script-injection
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, frontend, script-injection, wails-options, ipc, runtime]
level: practitioner
status: docs-checked
description: "Control how Wails injects ipc.js and runtime.js into index.html using the wails-options meta tag."
sources: [https://wails.io/docs/guides/frontend]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide whether Wails auto-injects its scripts or you include them yourself.

## Default behaviour
When Wails serves `index.html` it injects two script entries into the `<body>` tag: `/wails/ipc.js` (installs the bindings) and `/wails/runtime.js` (installs the runtime).

## Override with a meta tag
```html
<meta name="wails-options" content="[options]" />
```

| Value | Effect |
| --- | --- |
| noautoinjectruntime | Disable auto-injection of `/wails/runtime.js` |
| noautoinjectipc | Disable auto-injection of `/wails/ipc.js` |
| noautoinject | Disable all auto-injection |

Multiple options are comma separated (for example `noautoinjectipc,noautoinjectruntime`).

## Manual equivalent
With `noautoinject` set, add the scripts yourself, before your own script:

```html
<head>
  <meta name="wails-options" content="noautoinject" />
  <link rel="stylesheet" href="/main.css" />
</head>
<body>
  ...
  <script src="/wails/ipc.js"></script>
  <script src="/wails/runtime.js"></script>
  <script src="/main.js"></script>
</body>
```

The page says this behaves the same as the autoinjected version. The Create React App dev flow uses exactly this (see `computing-software.software-engineering.wails.dev-server-and-frontend-build-hooks`).

## Gaps
The page does not say when you would need it beyond customisation; the CRA reason is on the application development page.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Frontend" guide (Script Injection).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
