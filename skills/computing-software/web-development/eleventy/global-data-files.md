---
id: computing-software.web-development.eleventy.global-data-files
name: global-data-files
category: computing-software
field: web-development
product: eleventy
tags: [global-data, data-directory, json-data, data-folders]
level: intro
status: docs-checked
description: "Expose data to every Eleventy template with JSON and JavaScript files in the _data directory, including how folders shape the key names."
sources:
  - https://www.11ty.dev/docs/data-global/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global data is available to every template. Put `*.json` and `*.js` files in the global data folder inside the input directory. Its name is `dir.data`, default `_data`.

The file name becomes the key. `_data/userList.json` containing `["user1", "user2"]` is available as `userList`.

Folders add a level to the key path. Moving it to `_data/users/userList.json` gives:

```js
{ users: { userList: ["user1", "user2"] } }
```

Use `module.exports` values from `*.js` files for programmatic data (see JavaScript data files).

Computed data in this directory must be in a file named `eleventyComputed.js`.

Global data is the lowest-priority source in the data cascade. Another way to add global data to every template is `eleventyConfig.addGlobalData` (1.0.0+).

Change the folder with `eleventyConfig.setDataDirectory("lore")` or `dir.data`; it must be inside the input directory.

## Checked

2026-11-04. Confirmed against the Eleventy Global Data Files page and the Configuration page (for setDataDirectory and dir.data): *.json and *.js files in the data folder inside the input directory, default _data, file name as key, folders adding a key level, eleventyComputed.js for computed data, lowest cascade priority, addGlobalData (v1.0.0). Removed the unconfirmed ES module export wording.

Method: documentation only; no commands were run.
