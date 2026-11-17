---
id: computing-software.web-development.eleventy.create-plugin
name: create-plugin
category: computing-software
field: web-development
product: eleventy
tags: [plugins, add-plugin, plugin-options, version-check, feature-testing]
level: practitioner
status: docs-checked
description: "Use and write Eleventy plugins: addPlugin with options, async plugins, immediate execution, namespacing, feature testing, versionCheck and npm conventions."
sources:
  - https://www.11ty.dev/docs/create-plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A plugin is a function passed to `addPlugin`; it gets the same `eleventyConfig` as your config file.

```js
import pluginRss from "@11ty/eleventy-plugin-rss";
export default function (eleventyConfig) {
  eleventyConfig.addPlugin(pluginRss, { /* plugin-specific options */ });
}
```

Install from npm (`npm install @11ty/eleventy-plugin-rss --save`). A plugin can be inline, in the same file, a local import, or a package.

- **Async** (3.0.0+): `await eleventyConfig.addPlugin(async function (eleventyConfig) {...})`.
- **Timing:** plugins run in a second stage after your config finishes. `{ immediate: true }` (3.0.0+) runs it at once.
- **Options:** optional second argument, received as `pluginOptions`.
- **Namespace** (apps only, not plugins): `eleventyConfig.namespace("myPrefix_", () => {...})` prefixes filters, tags, shortcodes, collections, transforms.
- **Custom arguments:** export `{ initArguments, configFunction }` instead of a function; prefer the plain function.

**Feature test:** `if (!("addTemplate" in eleventyConfig)) console.log(...)`.

**Version check:** `eleventyConfig.versionCheck(">=3.0")` throws on mismatch; wrap in try/catch and log a warning. Uses semver ranges. Do not upper-bound the version.

**Distribute:** add `"eleventy-plugin"` to package.json `keywords`, name the package `eleventy-plugin-*`, and PR it to the community plugin list. These conventions are not hard requirements.

## Checked

2026-11-04. Confirmed against the Eleventy page Create or use Plugins (the cited plugins index page does not hold these claims, so the source was replaced): addPlugin with inline, same-file, local and npm plugins, npm install, optional second options argument, async plugins (v3.0.0, must await), namespace (application feature only), immediate option (v3.0.0) and the second-stage timing, initArguments and configFunction, feature testing with addTemplate, versionCheck with semver ranges and no upper bounds, and the distribution conventions. Corrected the async and immediate version gates from alpha tags to 3.0.0.

Method: documentation only; no commands were run.
