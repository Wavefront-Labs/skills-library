---
id: computing-software.game-programming.godot.web-export
name: web-export
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-export, godot-web-export, html5, webassembly, sharedarraybuffer, cross-origin-isolation, game-programming]
level: practitioner
status: docs-checked
description: "Export Godot 4 games to the web: thread vs no-thread builds, cross-origin isolation headers, renderer limits, audio unlock, file size, and hosting on itch.io or your server."
sources: ["https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html", "https://docs.godotengine.org/en/stable/tutorials/platform/web/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web export

**Goal:** a browser build that loads fast, runs on major browsers and hosts correctly.

## Constraints (Godot 4)
- Renderer: Godot 4 can only target WebGL 2.0, using the **Compatibility** method; Forward+ and Mobile are
  not supported on the web. Develop web projects on Compatibility from the start.
- C# projects using Godot 4 currently cannot be exported to the web (see the blog post linked from the
  export page). GDExtensions need the **Extension Support** export option and a web build.
- `user://` persistence uses IndexedDB: users must allow cookies (third-party cookies inside an iframe;
  private browsing prevents persistence). Low-level networking is not implemented; only the HTTP
  classes, WebSocket (client) and WebRTC work.
- The browser pauses the game (no `_process`) while its tab is not the active tab, which can disconnect
  networked games.

## Threads and headers
- **Thread Support** (export option): enabled builds need `SharedArrayBuffer`, which requires the page to be
  **cross-origin isolated**:
  ```
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Embedder-Policy: require-corp
  ```
- Since Godot 4.3 a single-threaded export is supported: it needs no special headers and is more
  compatible with stores such as itch.io, Poki and CrazyGames, but it cannot use threads and is less
  performant. **Extension Support** also requires the cross-origin isolation headers.
- The Progressive Web App export option can make a service worker ensure the headers are always present
  (**Enable Cross Origin Isolation Headers**, which can be unchecked), so threaded exports work on hosts where
  you cannot set headers. Service worker caching can show a stale build until it is unregistered.

## Audio
Some browsers restrict audio autoplay: ask the player to click, tap or press a key first (for example on
a splash screen). Since 4.3 web exports play audio as Web Audio samples by default: no AudioEffects,
no reverb or doppler, no procedural audio, and positional audio may misbehave. Set Audio > General >
Default Playback Type.web to Stream to use Godot's own audio system, at higher latency (especially
without thread support).

## Size and loading
- Serve `.wasm` as `application/wasm` (another MIME type can prevent start-up optimisations) and use
  server-side compression for `.pck` and `.wasm`: gzip shrinks the wasm to about a quarter, and Brotli
  precompression saves more. GitHub Pages compresses on the fly (gzip); itch.io and GitLab Pages do not.
- Custom export templates with unused modules disabled can shrink the WebAssembly payload significantly.
- The **Custom HTML shell** export option replaces the generated HTML page (branding, loading bar).

## Testing locally
With a runnable web template installed, the editor shows a button between Stop scene and Play edited Scene
that opens the game in the default browser. To test an exported folder, use the Godot repository's
`platform/web/serve.py` (`python serve.py --root .` from the folder with `index.html`; not for production).
Many browser features need a secure context (HTTPS, localhost usually exempt).

## Verify
- [ ] Runs in Chrome, Firefox and Safari (desktop and mobile) with audio after first click.
- [ ] Hosted build serves compressed wasm and correct headers (DevTools network tab).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: WebGL 2.0 only via Compatibility; C# projects cannot be exported to the web with Godot 4; single-thread export since 4.3 and why threads need cross-origin isolation (`Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Embedder-Policy: require-corp`); Extension Support also needs the headers; PWA option and Enable Cross Origin Isolation Headers; Web Audio sample playback default since 4.3 and its limitations, Default Playback Type.web; `.wasm` MIME type, gzip to about a quarter of the size, Brotli, which hosts compress on the fly; Custom HTML shell; the editor run-in-browser button and `serve.py`; limitations on `user://` persistence, networking and background tabs. Removed the unconfirmed wasm size, itch.io checkbox, texture-compression and `http.server` claims.

Method: documentation only; no commands were run.
