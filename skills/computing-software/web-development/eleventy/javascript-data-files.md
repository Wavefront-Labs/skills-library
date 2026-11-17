---
id: computing-software.web-development.eleventy.javascript-data-files
name: javascript-data-files
category: computing-software
field: web-development
product: eleventy
tags: [javascript-data, async-data, process-env, build-time-data]
level: practitioner
status: docs-checked
description: "Export data from JavaScript files in Eleventy, return async functions, receive configData, and expose environment variables to templates."
sources:
  - https://www.11ty.dev/docs/data-js/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JavaScript data files work for both global data (`*.js` in `_data`) and template/directory data (`*.11tydata.js`). They run arbitrary code at build time.

```js
export default ["user1", "user2"];
```

If you export a function, Eleventy uses its return value. The return value is awaited, so promises and `async function` work:

```js
export default async function () {
  let user1 = await fetchUserData("user1");
  return [user1];
}
```

From 1.0.0 a callback function receives the global data already processed via `addGlobalData`, plus the `eleventy` variable:

```js
export default function (configData) {
  return configData.eleventy.env.source === "cli"
    ? "I am on the command line"
    : "I am running programmatically via a script";
}
```

For remote APIs use the Eleventy Fetch plugin to request and cache.

Exposing an environment variable, saved as `_data/myProject.js`:

```js
export default function () {
  return { environment: process.env.MY_ENVIRONMENT || "development" };
}
```

Templates then read `myProject.environment`.

## Checked

2026-11-04. Confirmed against the Eleventy JavaScript Data Files page: applies to global *.js data and *.11tydata.js files, default export of data, function return values, awaited promises and async functions, Eleventy Fetch for remote APIs, configData argument with addGlobalData data and the eleventy variable (v1.0.0), and the process.env myProject.js example. Nothing removed.

Method: documentation only; no commands were run.
