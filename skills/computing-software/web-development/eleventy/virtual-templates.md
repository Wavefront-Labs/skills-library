---
id: computing-software.web-development.eleventy.virtual-templates
name: virtual-templates
category: computing-software
field: web-development
product: eleventy
tags: [virtual-templates, addtemplate, config-templates, plugin-templates]
level: advanced
status: docs-checked
description: "Define Eleventy templates and layouts inside the config file or a plugin with addTemplate, including front matter, data and JavaScript shapes."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/virtual-templates.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Virtual templates (3.0.0-alpha.15+) are processed like files but live in the config file or a plugin. The RSS plugin offers one to add feeds.

```js
eleventyConfig.addTemplate(virtualPath, content, data = {});
```

- `virtualPath`: decides the template language and data cascade; relative to the input directory.
- `content`: usually a string (front matter allowed if the language supports it), or JavaScript for an `11ty.js` template.
- `data`: a data object tied to the template; functionally the same as front matter but more ergonomic.

Markdown content with an HTML layout:

```js
export default function (eleventyConfig) {
  eleventyConfig.addTemplate("virtual.md", `# Hello`, {
    layout: "virtual.html",
  });
  // Works with layouts too
  eleventyConfig.addTemplate("_includes/virtual.html", `<!-- Layout -->{{ content }}`);
}
```

JavaScript:

```js
eleventyConfig.addTemplate("virtual.11ty.js", function (data) {
  return `<h1>Hello</h1>`;
});
```

Any of the JavaScript template shapes supported by `11ty.js` files work here.

## Checked

2026-11-08. Confirmed against the Eleventy docs Virtual Templates page (markdown source): the 3.0.0-alpha.15 version note, the RSS plugin mention, the addTemplate signature and parameter meanings, and both examples. Nothing removed.

Method: documentation only; no commands were run.
