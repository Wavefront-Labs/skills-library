---
id: computing-software.web-development.eleventy.watch-targets
name: watch-targets
category: computing-software
field: web-development
product: eleventy
tags: [watch-targets, addwatchtarget, watchignores, chokidar, wsl-polling]
level: practitioner
status: docs-checked
description: "Control what Eleventy watches: addWatchTarget, resetConfig, watchIgnores, JavaScript dependency watching, throttle delay and chokidar polling."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/watch-serve.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--watch` rebuilds on save without a server; `--serve` adds a hot-reloading dev server (Eleventy Dev Server, bundled since 2.0.0; Browsersync before that).

```js
export default function (eleventyConfig) {
  // external dependencies Eleventy cannot see (0.10.0+)
  eleventyConfig.addWatchTarget("./src/scss/");
  // reset the config when these change (3.0.0+)
  eleventyConfig.addWatchTarget("./_config/**", { resetConfig: true });
}
```

Globs go through chokidar and picomatch, so both `**/*.(png|jpeg)` and `**/*.{png,jpeg}` work. Config dependencies found via `require` or `import` already reset the config.

**Ignore watching** (2.0.0-canary.18+) has its own Set, separate from the template `ignores`:

```js
eleventyConfig.watchIgnores.add("README.md");
eleventyConfig.watchIgnores.delete("README.md");
```

It starts with `**/node_modules/**`. `.gitignore` entries are also ignored unless `setUseGitIgnore` is off.

**JavaScript dependencies** of JS templates, JS data files and the config are watched by default (0.7.0+); disable with `setWatchJavaScriptDependencies(false)`.

**Delay** rebuilds: `setWatchThrottleWaitTime(100)` in ms (default 0), useful alongside other task runners.

**chokidar options:** `setChokidarConfig({ usePolling: true, interval: 500 })`. On WSL with a project outside `~`, polling is likely needed.

To reload the browser without an Eleventy build, use the dev server's `watch` option.

## Checked

2026-11-08. Confirmed against the Eleventy docs Watch and Serve page (markdown source): watch versus serve, the dev server and Browsersync history, addWatchTarget (0.10.0) and resetConfig (3.0.0), glob syntax, watchIgnores (2.0.0-canary.18) and its default entry, gitignore handling, JavaScript dependency watching (0.7.0), throttle (0.11.0), chokidar config and the WSL note. Nothing removed. The page also notes that JavaScript dependency watching covers more extensions in 4.0.0-alpha.11, not covered here.

Method: documentation only; no commands were run.
