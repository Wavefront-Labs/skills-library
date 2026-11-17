---
id: computing-software.web-development.eleventy.programmatic-api
name: programmatic-api
category: computing-software
field: web-development
product: eleventy
tags: [programmatic-api, eleventy-class, tojson, tondjson, node-script]
level: advanced
status: docs-checked
description: "Run Eleventy from a Node script: write to disk, get results as JSON or NDJSON, set input and output directories and pass quietMode, configPath or config."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/programmatic.md
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/_includes/snippets/programmatic/fullopts.njk
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available since 1.0.0. Install Eleventy locally, then in `my-node-script.js`:

```js
import Eleventy from "@11ty/eleventy";

let elev = new Eleventy();
await elev.write();
```

Run with `node my-node-script.js`. In CommonJS, load it inside an async function: `const { Eleventy } = await import("@11ty/eleventy");`.

**Without writing files:** `await elev.toJSON()` returns all results; `toNDJSON()` gives newline-delimited output. To add data cascade values to each JSON entry, add lodash-style selectors to `eleventyConfig.dataFilterSelectors`.

**Directories:** first argument is input, second is output.

```js
let elev = new Eleventy(".", "_site");
```

**Options object** (third argument):

```js
let elev = new Eleventy(".", "_site", {
  quietMode: true,            // --quiet
  configPath: ".eleventy.js", // --config
  config: function (eleventyConfig) {
    // custom Configuration API calls, e.g. eleventyConfig.addGlobalData
  },
});
```

The options list is a work in progress in the docs; the `Eleventy` class source is the reference.

## Checked

2026-11-08. Confirmed against the Eleventy docs Programmatic API page and its code snippets (markdown sources): 1.0.0 availability, write, toJSON and toNDJSON, dataFilterSelectors, input and output arguments, and the quietMode, configPath and config options in the example. Removed the claim that process.env.ELEVENTY_SOURCE is script, which neither the page nor its snippets state.

Method: documentation only; no commands were run.
