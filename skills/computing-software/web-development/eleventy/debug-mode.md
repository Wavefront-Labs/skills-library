---
id: computing-software.web-development.eleventy.debug-mode
name: debug-mode
category: computing-software
field: web-development
product: eleventy
tags: [debug-mode, debug-env, dryrun, log-filter, troubleshooting]
level: intro
status: docs-checked
description: "Troubleshoot an Eleventy build with the DEBUG environment variable on each OS, pair it with --dryrun and inspect values with the log filter."
sources:
  - https://www.11ty.dev/docs/debugging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Eleventy uses the `debug` package. With `DEBUG` set it prints the directories used for data, includes, input and output, the search globs, and the templates found.

- macOS/Linux: `DEBUG=Eleventy* npx @11ty/eleventy`
- Windows cmd.exe: `set DEBUG=Eleventy* & npx @11ty/eleventy`
- PowerShell: `$env:DEBUG="Eleventy*"; npx @11ty/eleventy`
- Cross platform: `npm install cross-env`, then an npm script:

```json
{ "scripts": { "debug": "cross-env DEBUG=Eleventy* npx @11ty/eleventy" } }
```

`npm run debug` now works.

Tips:

- Add `--dryrun` to run without writing files.
- `DEBUG=*` shows messages from every dependency; `DEBUG=Eleventy*` limits to Eleventy.
- `DEBUG=Eleventy:Benchmark*` analyses build performance (see the performance analysis skill).
- Inspect a single variable inside a template with the global `log` filter, which `console.log`s the value.

## Checked

2026-11-04. Confirmed against the Eleventy Debug Mode page: the debug package, what DEBUG prints, the macOS/Linux, cross-env, cmd.exe and PowerShell commands, the npm run debug script, --dryrun, DEBUG=* versus DEBUG=Eleventy*, the performance analysis pointer and the global log filter. Removed the unconfirmed 0.3.0+ and 0.11.0+ version gates.

Method: documentation only; no commands were run.
