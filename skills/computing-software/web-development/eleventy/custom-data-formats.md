---
id: computing-software.web-development.eleventy.custom-data-formats
name: custom-data-formats
category: computing-software
field: web-development
product: eleventy
tags: [adddataextension, yaml-data, toml-data, json5, data-file-formats]
level: practitioner
status: docs-checked
description: "Teach Eleventy new data file formats such as YAML, TOML or JSON5 with addDataExtension, options like read and encoding, and file priority order."
sources:
  - https://www.11ty.dev/docs/data-custom/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Eleventy reads JavaScript and JSON data files natively. Add any text format with `addDataExtension`. The callback receives file contents and (v2.0.0+) the file path, and returns data.

```js
import YAML from "yaml";
import toml from "@iarna/toml";

export default function (eleventyConfig) {
  eleventyConfig.addDataExtension("yaml", (contents) => YAML.parse(contents));
  eleventyConfig.addDataExtension("toml", (contents) => toml.parse(contents));
}
```

Install the parser package yourself (`npm install yaml`). Pass a comma-separated list of extensions (v2.0.0+), e.g. `"png,jpeg"`.

Options form:

```js
eleventyConfig.addDataExtension("png,jpeg", {
  parser: async (file) => ({ exif: await exifr.parse(file) }),
  read: false,        // default true: parser gets contents
  encoding: "utf8",   // default; null gives a Buffer
});
```

With `read: false` the parser receives a file path. A `my-post.jpeg` beside `my-post.md` then exposes `exif` in the post.

Priority: custom formats rank below both JavaScript and JSON. Among custom formats, later `addDataExtension` calls win over earlier ones. For `my-first-blog-post.md` the search order is `.11tydata.js`, `.11tydata.json`, `.11tydata.yaml`, `.11tydata.toml`, `.json`, `.yaml`, `.toml`.

## Checked

2026-11-04. Confirmed against the Eleventy page Custom Data File Formats: addDataExtension with contents and filePath, comma-separated extensions (v2.0.0), the options form with parser, read (default true) and encoding (default utf8, null for a Buffer), the yaml, @iarna/toml and exifr examples, lower priority than JavaScript and JSON, later registrations win, and the 7-step search order. Removed the unconfirmed 0.10.0+ gate and corrected the canary version gates to v2.0.0.

Method: documentation only; no commands were run.
