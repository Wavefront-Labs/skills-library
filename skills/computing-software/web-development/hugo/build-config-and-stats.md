---
id: computing-software.web-development.hugo.build-config-and-stats
name: build-config-and-stats
category: computing-software
field: web-development
product: hugo
tags: [build-config, build-stats, hugo-stats-json, cachebusters, clean-destination-dir]
level: advanced
status: docs-checked
description: "Configure the build section: hugo_stats.json build stats, cache busters for CSS rebuilds, cleanDestinationDir with keepDirs and keepFiles, and useResourceCacheWhen."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Top-level `build` settings: `buildStats`, `cachebusters`, `cleanDestinationDir`, `noJSConfigInAssets` (stops writing `jsconfig.json` to `assets`) and `useResourceCacheWhen` (`never`, `fallback` or `always`; default `fallback`).

**Build stats.** `build.buildStats.enable = true` writes `hugo_stats.json` to the project root, listing `class` attributes, `id` attributes and tags of rendered HTML, for removing unused CSS. `disableIDs`, `disableTags` and `disableClasses` exclude parts. Put it under `config/production`. The parser can produce inconsequential false positives, and during partial server builds old values persist until you restart or run `hugo build`.

**Cache busters** expire resource cache keys when a watched source changes:

```toml
[[build.cachebusters]]
  source = 'assets/notwatching/hugo_stats\.json'
  target = 'css'
```

`source` is a regular expression on files relative to a virtual component directory; `target` matches cache keys and can use groups such as `$1`.

**Cleaning `public`.** `build.cleanDestinationDir.enable` (new in 0.167.0) removes every file without a corresponding static file, including manually added ones such as `CNAME` or `_redirects`. Preserve with glob lists `keepDirs` and `keepFiles`; a custom value replaces the default, so include the defaults to keep them. Override per build with `--cleanDestinationDir`.

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure build: the top-level keys, `useResourceCacheWhen` values and default, the build stats behaviour and caveats, cache buster `source` and `target` semantics, and the `cleanDestinationDir` enable, `keepDirs` and `keepFiles` rules including the 0.167.0 note. Nothing removed.

Method: documentation only; no commands were run.
