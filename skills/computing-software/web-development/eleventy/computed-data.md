---
id: computing-software.web-development.eleventy.computed-data
name: computed-data
category: computing-software
field: web-development
product: eleventy
tags: [eleventycomputed, computed-data, dependency-graph, navigation-data]
level: practitioner
status: docs-checked
description: "Derive Eleventy data from other data with eleventyComputed in JavaScript or template strings, and declare dependencies that auto-detection misses."
sources:
  - https://www.11ty.dev/docs/data-computed/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`eleventyComputed` injects data based on other data values. It is computed right before render, so it cannot change special template-configuration keys such as `layout`, `pagination` or `tags`. `permalink` is the exception: it works.

Put it anywhere in the cascade: front matter, any data file, or `_data/eleventyComputed.js` for the whole site.

```js
export default {
  eleventyComputed: {
    eleventyNavigation: {
      key: (data) => data.title,
      parent: (data) => data.parent,
    },
    myAsync: async (data) => await someAsyncThing(),
  },
};
```

Functions need JavaScript front matter or a JS data file. In YAML/JSON use a template string matching the template's syntax (slower):

```yaml
eleventyComputed:
  eleventyNavigation:
    key: "{{ title }}"
```

Rules: read other computed values as `data.propName`, not `data.eleventyComputed.propName`. Key order does not matter, circular references are reported, nested objects deep merge, and you can reuse and override a key (`key: "This Is {{ key }}"`).

If a dependency is only used inside conditional logic, auto-detection can miss it. Declare it by accessing it in the callback (`data.myValue;`). Check detected variables in debug output.

## Checked

2026-11-04. Confirmed against the Eleventy page Computed Data: computed right before render, special keys such as layout, pagination and tags cannot be changed, permalink works, placement anywhere in the cascade including _data/eleventyComputed.js, JavaScript functions needing JS front matter or data files, template strings for YAML/JSON (slower), data.propName for computed dependencies, key order, circular reference reporting, deep merge, reuse and override of a key, declaring dependencies by accessing them, debug output. Removed the unconfirmed 0.11.0+ version gate.

Method: documentation only; no commands were run.
