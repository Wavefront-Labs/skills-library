---
id: computing-software.web-development.eleventy.configuration-events
name: configuration-events
category: computing-software
field: web-development
product: eleventy
tags: [configuration-events, eleventy-before, eleventy-after, beforewatch, event-emitter]
level: advanced
status: docs-checked
description: "Run code at points in an Eleventy build with eleventyConfig.on: before, after, beforeConfig, beforeWatch, contentMap, event arguments and emitter mode."
sources:
  - https://www.11ty.dev/docs/events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Attach handlers in the config file with `eleventyConfig.on(name, callback)`. Async callbacks are supported (1.0+). Callbacks run in parallel; for sequential use `eleventyConfig.setEventEmitterMode("sequential")`.

- `eleventy.before` (1.0.0+, was `beforeBuild`): before every build, including each `--watch`/`--serve` rebuild.
- `eleventy.after` (1.0.0+, was `afterBuild`): after every build.
- `eleventy.beforeConfig` (3.0.0+): before the config initializes; an escape hatch when the top-level callback cannot be async, e.g. to `await import("@11ty/eleventy")` and add a plugin.
- `eleventy.beforeWatch` (1.0.0+): only on watch/serve re-runs; receives the array of `changedFiles`.
- `eleventy.contentMap` (2.0.0): receives `{ inputPathToUrl, urlToInputPath }` maps; it feeds the i18n plugin.

```js
eleventyConfig.on("eleventy.after", async ({ directories, results, runMode, outputMode }) => {
  // run after the build
});
```

Arguments for before/after (2.0.0+):

- `directories`: normalized `input`, `inputFile`, `inputGlob`, `data`, `includes`, `layouts`, `output` (best with a named `config` export). `dir` is deprecated.
- `outputMode`: `fs` (default), `json` or `ndjson` (from `--to`)
- `runMode`: `build` (default), `watch` or `serve`
- `results` (after only): array of `{ inputPath, outputPath, url, content }`

## Checked

2026-11-04. Confirmed against the Eleventy Events page: async callbacks from 1.0, eleventy.before and eleventy.after (v1.0.0, replacing beforeBuild and afterBuild, run on each watch/serve rebuild), event arguments (v2.0.0) with directories, deprecated dir, outputMode fs/json/ndjson, runMode build/watch/serve and results entries, eleventy.beforeConfig (v3.0.0), eleventy.beforeWatch with changedFiles (v1.0.0, re-runs only), eleventy.contentMap (v2.0.0, i18n), parallel callbacks and setEventEmitterMode("sequential"). Corrected the beforeConfig version from 3.0.0-alpha.3 to v3.0.0.

Method: documentation only; no commands were run.
