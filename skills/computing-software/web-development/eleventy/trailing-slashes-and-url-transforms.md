---
id: computing-software.web-development.eleventy.trailing-slashes-and-url-transforms
name: trailing-slashes-and-url-transforms
category: computing-software
field: web-development
product: eleventy
tags: [trailing-slash, addurltransform, missing-file-extension, vercel, resource-html]
level: advanced
status: docs-checked
description: "Control trailing slashes and file extensions in Eleventy permalinks, allow extensionless output, and rewrite page.url with addUrlTransform."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/permalinks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trailing slashes are the default (`/resource/index.html`, URL `/resource/`) as the most reliable across hosts.

A permalink `/resource` with no file name and no trailing slash errors: it would write a file with no extension. `/resource/` and `/resource/index.html` are fine. To allow it (3.0.0-beta.2+, e.g. Netlify `_redirects`) set `eleventyAllowMissingExtension: true` in the cascade, or globally:

```js
eleventyConfig.configureErrorReporting({ allowMissingExtensions: true });
```

**`/resource`-style URLs** (not recommended; works on GitHub Pages, Netlify, Cloudflare Pages, Render, Azure Static Web Apps, not Vercel):

```js
eleventyConfig.addGlobalData("permalink", () => {
  return (data) => `${data.page.filePathStem}.${data.page.outputFileExtension}`;
});
eleventyConfig.addUrlTransform((page) => {
  if (page.url.endsWith(".html")) {
    return page.url.slice(0, -1 * ".html".length);
  }
});
```

On Vercel, strip the slash with an URL transform (`page.url !== "/" && page.url.endsWith("/")`) and set `"trailingSlash": false` in `vercel.json`.

`addUrlTransform` changes `page.url` without moving the file. Returning undefined skips it. Use it to map `about.en.html` and `about.es.html` to one `/about/` URL; choose the file with server-side redirects.

## Checked

2026-11-08. Confirmed against the Eleventy docs Permalinks page (markdown source): trailing-slash default, the extensionless-permalink error and eleventyAllowMissingExtension (3.0.0-beta.2), configureErrorReporting, the resource-style config and its host list, the Vercel variant with trailingSlash false, and the about.en.html URL transform example. Nothing removed.

Method: documentation only; no commands were run.
