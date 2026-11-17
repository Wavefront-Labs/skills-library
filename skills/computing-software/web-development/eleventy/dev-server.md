---
id: computing-software.web-development.eleventy.dev-server
name: dev-server
category: computing-software
field: web-development
product: eleventy
tags: [dev-server, setserveroptions, live-reload, onrequest, browsersync]
level: practitioner
status: docs-checked
description: "Configure Eleventy Dev Server with setServerOptions: port, live reload, extra watch globs, https, 404 page, onRequest handlers and Browsersync fallback."
sources:
  - https://www.11ty.dev/docs/dev-server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Eleventy Dev Server (2.0.0+) is the bundled hot-reloading server for `--serve`. Configure it with `setServerOptions`; defaults:

```js
eleventyConfig.setServerOptions({
  liveReload: true,   // inject live reload snippet
  domDiff: true,      // DOM diffing instead of page reloads where possible
  port: 8080,         // increments up to 10 times if in use
  watch: [],          // extra files/globs that trigger server updates
  showAllHosts: false,
  https: {},          // { key: "./localhost.key", cert: "./localhost.cert" } for HTTP/2
  encoding: "utf-8",
  showVersion: false,
  indexFileName: "index.html", // Dev Server 2.0+
  onRequest: {},               // Dev Server 2.0+
});
```

`watch: ["_site/**/*.css"]` suits a separate bundler writing into the output folder. A root `404.html` in the output folder is served for missing content.

**onRequest** (Eleventy v3.0.0 / Dev Server 2.0.0): keys are URL Pattern API pathnames. A callback gets `{ url, pattern, patternGroups }`. Any falsy value except `""` falls back to static files; `""` renders an empty page; an object `{ status, headers, body }` is a response.

```js
onRequest: {
  "/foo/:name": ({ patternGroups }) => ({ status: 200, headers: { "Content-Type": "text/html" }, body: "Hello." }),
}
```

Pair with `process.env.ELEVENTY_RUN_MODE === "serve"` to alter only serve mode.

**Back to Browsersync:** `npm install @11ty/eleventy-server-browsersync`, then `setServerOptions({ module: "@11ty/eleventy-server-browsersync", port: 8080, ... })`. `setBrowserSyncConfig` is a no-op since v2.

## Checked

2026-11-04. Confirmed against the Eleventy Dev Server page: bundled since v2.0.0, the setServerOptions defaults (liveReload, domDiff, port 8080 with up to 10 increments, watch, showAllHosts, https, encoding, showVersion, indexFileName and onRequest from Dev Server 2.0), root 404.html support, onRequest semantics (URL Pattern keys, falsy fallback except empty string, response object, ELEVENTY_RUN_MODE), the Browsersync fallback package and the v2 no-op for setBrowserSyncConfig. Corrected the onRequest version gate from 3.0.0-alpha.7 to v3.0.0.

Method: documentation only; no commands were run.
