---
id: computing-software.web-development.eleventy.javascript-templates
name: javascript-templates
category: computing-software
field: web-development
product: eleventy
tags: [javascript-templates, 11ty-js, render-method, data-method, template-functions]
level: practitioner
status: docs-checked
description: "Write .11ty.js templates: strings, functions, async and class templates with data and render, permalinks, JavaScript template functions and the arrow function trap."
sources:
  - https://www.11ty.dev/docs/languages/javascript/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Extensions: `.11ty.js`, `.11ty.cjs` (0.11.0+), `.11ty.mjs` (3.0.0+). Front matter is not supported; use a `data` export.

**Raw values** (string, Buffer, Promise) get no data access. **Functions** receive `data` and may be async:

```js
export default ({ name }) => `<p>${name}</p>`;
```

**Classes** need a `render(data)` method (may be async). Optional `data()` (also `async data()` or `get data()`) acts as front matter and wins in the data cascade:

```js
class Test {
  data() { return { name: "Ted", layout: "teds-rad-layout" }; }
  render({ name }) { return `<p>${name}</p>`; }
}
export default Test;
```

**Permalinks:** `permalink` may be a string or a function `(data) => ...`. Universal filters are on `this`: `permalink: function (data) { return `/${this.slug(data.title)}/`; }`.

**Markdown preprocessing:** `templateEngineOverride: "11ty.js,md"`. Other engines such as `njk,md` are not supported here; use the Render plugin.

**Template functions:** `eleventyConfig.addJavaScriptFunction("myFunction", fn)`; call as `this.myFunction(...)`, with `await` for async ones. Universal filters, shortcodes and paired shortcodes are also exposed on `this`. Non-arrow functions can read `this.page` (0.11.0+).

**Warning:** arrow functions have no `this`, so using template functions in one throws.

## Checked

2026-11-04. Confirmed against the Eleventy JavaScript page: the .11ty.js, .11ty.cjs (0.11.0) and .11ty.mjs (3.0.0) extensions, no front matter, raw values without data access, function and async function templates, class render and data (async or getter) methods acting as front matter, permalink strings and functions with this.slug, templateEngineOverride 11ty.js,md and the Render plugin workaround, addJavaScriptFunction with async use, universal filters and shortcodes on this, this.page (0.11.0) and the arrow function warning. Nothing removed.

Method: documentation only; no commands were run.
