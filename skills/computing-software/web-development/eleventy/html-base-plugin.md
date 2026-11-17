---
id: computing-software.web-development.eleventy.html-base-plugin
name: html-base-plugin
category: computing-software
field: web-development
product: eleventy
tags: [html-base, path-prefix, htmlbaseurl, transformwithhtmlbase, subdirectory-deploy]
level: practitioner
status: docs-checked
description: "Apply a path prefix to all URLs in HTML output at build time with the bundled HTML Base plugin and its htmlBaseUrl, transformWithHtmlBase filters."
sources:
  - https://www.11ty.dev/docs/plugins/html-base/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bundled since v2.0.0; no install. It is a build-time stand-in for the HTML `<base>` element, implemented as an Eleventy transform. It rewrites URLs in `a[href]`, `video[src]`, `audio[src]`, `source`, `img[src]`, `[srcset]` and more (via posthtml-urls) in `.html` output, so you no longer need the `url` filter on every link.

Path prefix comes from `--pathprefix` or `pathPrefix` in the config return object.

```js
import { HtmlBasePlugin } from "@11ty/eleventy";
export default function (eleventyConfig) {
  eleventyConfig.addPlugin(HtmlBasePlugin);
}
```

Nothing else is needed for HTML templates.

**Filters** for URLs the transform does not reach, such as an HTML comment:

- `htmlBaseUrl`: transform one URL string. A second argument overrides `baseHref`. With a full URL as base, relative paths are modified using the current page URL.
- `transformWithHtmlBase`: transform a block of HTML with the same rules. Needs an async-friendly language (Nunjucks, Liquid, JavaScript). The RSS plugin uses it to make content absolute.
- `addPathPrefixToFullUrl`: external full URLs pass through `htmlBaseUrl` unchanged; this filter forces the prefix on.

The native `<base>` element is an alternative, but some find it unreliable in edge cases.

## Checked

2026-11-04. Confirmed against the Eleventy HTML <base> plugin page: added in v2.0.0 and bundled, build-time transform of a[href], video[src], audio[src], source, img[src], [srcset] and more via posthtml-urls, --pathprefix and pathPrefix, the HtmlBasePlugin import, htmlBaseUrl (baseHref override, relative paths resolved against the page URL for full-URL bases), transformWithHtmlBase (async-friendly languages, used by the RSS plugin), addPathPrefixToFullUrl, and the native <base> note. Corrected the version gate from 2.0.0-canary.15.

Method: documentation only; no commands were run.
