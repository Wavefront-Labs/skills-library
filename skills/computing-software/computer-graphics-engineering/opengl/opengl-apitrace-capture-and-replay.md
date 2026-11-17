---
id: computing-software.computer-graphics-engineering.opengl.opengl-apitrace-capture-and-replay
name: opengl-apitrace-capture-and-replay
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-debug-output, apitrace, gl-call-trace, qapitrace, regression-testing]
level: practitioner
status: docs-checked
description: "Trace every OpenGL call with apitrace, replay and inspect state per call in qapitrace, trim traces and diff images for driver/regression bugs."
sources: ["https://github.com/apitrace/apitrace/blob/master/docs/USAGE.markdown", "https://apitrace.github.io/", "https://github.com/apitrace/apitrace/blob/master/docs/BUGS.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apitrace for OpenGL

apitrace records the full call stream of an app (GL, GLES, EGL, D3D9-11) into a `.trace` file
that replays without the app. Use it when RenderDoc can't capture (compatibility profile, old
GL, GLES on desktop) or to hand a driver vendor a reproducible bug.

## 1. Capture
```sh
apitrace trace --api gl ./myapp args           # writes myapp.trace in the current directory (--output sets the name)
apitrace trace --api egl ./myapp                # EGL/GLES
# --api takes gl, egl, d3d7, d3d8, d3d9 or dxgi; D3D10 and later need dxgi
```
Traces get large (every texture upload is stored). Capture a short run and cut the frames you
need afterwards (step 4).

## 2. Replay and inspect
```sh
apitrace replay myapp.trace                     # plays back in a window
apitrace replay --sb myapp.trace                # single-buffered visual; see apitrace replay --help for more options
qapitrace myapp.trace                           # GUI: frames > calls > state, textures, FBOs, shaders
apitrace dump --calls=1000-1200 myapp.trace     # text dump of a call set
```
qapitrace shows the trace's calls and the state at each call, and can show a backtrace tab for
calls when the trace was captured with backtraces enabled (see the apitrace USAGE page).

## 3. Image regression
```sh
apitrace dump-images -o ref/ myapp.trace                                # reference snapshots
apitrace dump-images -o new/ myapp.trace                                # snapshots on the driver under test
apitrace diff-images --output summary.html ref/ new/                    # html report of differences
apitrace replay -D 12345 myapp.trace > 12345.json                       # state at call 12345 as JSON
apitrace diff-state 12345.json 67890.json                               # compare two state dumps
```
Run the same trace on two drivers/GPUs to prove a driver regression independent of app code.

## 4. Trim for a minimal repro
```sh
apitrace trim --calls=0-5000 --calls=98000-98450 myapp.trace -o small.trace
```
`trim` takes call sets; check `apitrace trim --help` for how it handles dependent calls such as
object creation, and verify the trimmed trace still reproduces before filing.

## Gotchas
- Known tracing problems and workarounds are listed in apitrace's BUGS page; use `apitrace trace --verbose --debug` when a capture misbehaves.
- Traces contain all asset data: treat them as confidential when sending to vendors.

## Verify
- [ ] `apitrace replay` shows the same frame as the live app.
- [ ] Trimmed trace reproduces the bug on its own and is small enough to attach to a bug report.

## Checked

- Date: 2026-11-02.
- Confirmed against: apitrace USAGE page (trace --api values and -a, --output, dump --calls, replay, --sb, qapitrace, dump-images -o, diff-images --output, replay -D with diff-state on JSON, trim --calls) and BUGS page (trace --verbose --debug).
- Removed: `replay -b`, `--snapshot`/`--snapshot-prefix`, `trim --frames`, `--auto`, the `--verbose` glGetError flagging, the lookup-state wording and the mapped-buffer and macOS replay gotchas; none appear in the fetched pages. The image-regression and trim commands were corrected to the documented forms.

Method: documentation only; no commands were run.
