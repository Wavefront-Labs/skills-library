---
id: computing-software.web-development.eleventy.front-matter-data
name: front-matter-data
category: computing-software
field: web-development
product: eleventy
tags: [front-matter, yaml, json-front-matter, js-front-matter, gray-matter]
level: practitioner
status: docs-checked
description: "Write Eleventy front matter in YAML, JSON or JavaScript, change the default format, and know which keys may contain variables."
sources:
  - https://www.11ty.dev/docs/data-frontmatter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Front matter sits between `---` fences at the top of a template. Leaf template front matter beats layout front matter. Layouts can also hold front matter variables you use in the local template.

Only `permalink` and `eleventyComputed` front matter values can contain variables and shortcodes like template bodies. For other keys, set them through `eleventyComputed`.

Eleventy uses the `gray-matter` package: `yaml` (default), `json` and `js` formats work out of the box.

```md
---json
{ "title": "My page title" }
---
```

JavaScript front matter (v3.0.0+) exports top-level variables and functions to the template. It is async friendly:

```md
---js
const title = "My page title";
function currentDate() {
  return (new Date()).toLocaleString();
}
---
<h1>{{ title }}</h1>
<p>Published on {{ currentDate() }}</p>
```

That example works in Nunjucks but not Liquid, which does not allow function execution in output. `js` front matter also accepts an object literal `{ title: "...", currentDate: function() {} }`.

Change the project-wide default format with `eleventyConfig.setFrontMatterParsingOptions({ language: "js" })` or add formats such as TOML through the front matter customisation API.

## Checked

2026-11-04. Confirmed against the Eleventy Front Matter Data page: leaf template precedence, only permalink and eleventyComputed values accepting variables, gray-matter with yaml (default), json and js formats, setFrontMatterParsingOptions, JavaScript front matter (v3.0.0), the Liquid function-call limitation, the object-literal form and the TOML customisation pointer. Corrected the JS front matter version gate from 3.0.0-alpha.18 and removed the unconfirmed 0.9.0+ gate.

Method: documentation only; no commands were run.
