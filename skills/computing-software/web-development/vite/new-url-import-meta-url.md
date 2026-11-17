---
id: computing-software.web-development.vite.new-url-import-meta-url
name: new-url-import-meta-url
category: computing-software
field: web-development
product: vite
tags: [new-url-pattern, import-meta-url, dynamic-asset-url]
level: practitioner
status: docs-checked
description: "Resolve asset URLs with new URL(path, import.meta.url): dynamic template literals, why the string must be static, and why it fails under SSR."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/assets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Combine `import.meta.url` with the native URL constructor to get an asset's resolved URL relative to the current module:

```js
const imgUrl = new URL('./img.png', import.meta.url).href
```

Template literals work, but do not include files in subdirectories:

```js
function getImageUrl(name) {
  return new URL(`./dir/${name}.png`, import.meta.url).href
}
```

In dev, Vite does not need to process this. In the build, URLs are transformed to survive bundling and hashing.

Gotchas:
- The URL string must be static so it can be analyzed. `new URL(imagePath, import.meta.url)` is left as-is and can fail at runtime if `build.target` does not support `import.meta.url`.
- Does not work with SSR: `import.meta.url` differs between browsers and Node.js, and the server bundle cannot know the client host URL.

## Checked

Date: 2026-11-07

Read assets.md in full (new URL(url, import.meta.url) section). Confirmed the .href example, template literal form, static-string requirement and build.target warning, and the SSR warning. Trimmed "only for files one directory deep" to the page wording: the template literal form does not include files in subdirectories.

Method: documentation only; no commands were run.
