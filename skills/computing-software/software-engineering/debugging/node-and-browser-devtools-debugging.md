---
id: computing-software.software-engineering.debugging.node-and-browser-devtools-debugging
name: node-and-browser-devtools-debugging
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, javascript, chrome-devtools, node-debugging, source-maps, inspector]
level: practitioner
status: docs-checked
description: "Debug Node.js and browser JavaScript with the V8 inspector and Chrome DevTools: --inspect flags, breakpoint types, scope/watch, source maps."
sources: ["https://nodejs.org/en/learn/getting-started/debugging", "https://developer.chrome.com/docs/devtools/javascript", "https://developer.chrome.com/docs/devtools/javascript/source-maps", "https://code.visualstudio.com/docs/nodejs/nodejs-debugging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js and browser DevTools debugging

## Node.js inspector
```
node --inspect app.js                 # listen for a debug client on 127.0.0.1:9229 (default)
node --inspect-brk app.js             # same, and break before user code starts
node --inspect-wait app.js            # same, and wait for a debugger to attach
node --inspect=[host:port] app.js     # choose address and port
node inspect app.js                   # minimal CLI debugger
```
- Each process gets a unique UUID; clients connect to a URL like `ws://127.0.0.1:9229/<uuid>`.
- SIGUSR1 starts the inspector on a running process (Node.js 8+; not available on Windows).
  `--disable-sigusr1` turns that off.
- Chrome or Edge: open `chrome://inspect` (`edge://inspect`), check Configure lists your host and port, and
  the app appears under Remote Target. Alternatively open `http://localhost:<port>/json/list` and use the
  `devtoolsFrontendUrl` value.
- **Security:** the debugger has full access to the Node.js environment. Binding to a public IP or `0.0.0.0`
  lets any reachable client run arbitrary code; any local application can reach a loopback inspector too.
  For remote debugging the guide recommends an ssh tunnel (for example `ssh -L 9221:localhost:9229 user@host`)
  rather than a public listener. Node verifies the `Host` header is an IP or `localhost`, so connecting by
  hostname fails; use the IP or a tunnel.
- VS Code: Auto Attach (command `Toggle Auto Attach`; "smart" mode skips `node_modules` scripts except
  runners such as mocha or ts-node) and the JavaScript Debug Terminal debug processes you start from the
  Integrated Terminal. A `launch.json` configuration uses `"type": "node"`.

## Browser (Chrome DevTools)
The Sources panel has the file tree (Page tab), the Code Editor and the Debugger section.
- Breakpoint types: line-of-code, Event Listener Breakpoints (for example Mouse > click), conditional,
  caught or uncaught exceptions, and XHR breakpoints (URL contains a substring you give).
- While paused: step into / step over, the Scope tab (local, global, closure variables; double-click a value
  to edit), Watch expressions (any JavaScript expression), and the Console to test fixes in scope.
- Editing code in DevTools fixes only the code running in your browser, not the server copy.

## Source maps
DevTools runs the minified code but shows your authored files; breakpoints, errors and logs map back.
- Use a preprocessor that emits source maps (Babel, TypeScript, terser, Webpack, Vite, esbuild, Parcel are listed)
  and a server that can serve them.
- Settings > Preferences > Sources: check **JavaScript source maps** (and CSS source maps if wanted).
- DevTools reports when it finds the `//# sourceMappingURL` comment in a deployed file.
- `//# sourceURL=/path/to/source.file` names `eval()` code and inline scripts so they show as files.

## Checked
2026-11-09. Confirmed against the Node.js "Debugging Node.js" guide (flags, default address, UUID URL,
SIGUSR1, security, chrome://inspect, ssh tunnel), Chrome "Debug JavaScript" and "Source maps" pages, and the
VS Code Node.js debugging page (Auto Attach, Debug Terminal, `"type": "node"`). Removed as not in the pages:
Jest and Vitest inspector recipes, tsx and `--enable-source-maps`, DOM breakpoints, ignore list, overrides,
async stack and Network/Console utility lists, and advice on serving source maps in production.
Method: documentation only; no commands were run.
